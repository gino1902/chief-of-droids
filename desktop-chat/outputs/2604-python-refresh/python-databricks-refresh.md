# Python for Databricks — Refresher (2026)

Dense, expert-level. No hand-holding. Python 3.11/3.12 per your DBR runtime.

---

## 0. Mental model

Python in Databricks = three surfaces:

1. **Notebooks** (interactive) — a `spark` SparkSession and `dbutils` are injected globally.
2. **Jobs / Workflows** (batch) — same code, no interactivity; `dbutils` still works except for UI bits (`widgets.get` works, `notebook.run` works, `widgets.text` in batch is no-op).
3. **Databricks Connect** (local) — you run Python on your laptop, Spark executes on the cluster. Same DataFrame API, no `dbutils.fs.*` as-is (use Files API / SDK instead).

PySpark is the dominant API. Pandas runs driver-side only and should be used for small, final-mile transforms or for `pandas_udf` / `applyInPandas` patterns.

---

## 1. Modern Python essentials you should be fluent in

### Type hints (cheap insurance in notebooks too)

```python
def enrich(rows: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
    ...

from collections.abc import Iterable, Mapping, Callable
# Prefer these over typing.List/Dict since 3.9
```

Union is `X | Y` (3.10+). `Optional[X]` = `X | None`. `Any` is an escape hatch; `object` is the stricter one.

### Dataclasses vs Pydantic vs TypedDict

```python
from dataclasses import dataclass, field

@dataclass(slots=True, frozen=True)
class OrderLine:
    sku: str
    qty: int
    price: float
    tags: list[str] = field(default_factory=list)
```

- `dataclass` — stdlib, zero-cost, great for internal models.
- `pydantic v2` — when data crosses an API/IO boundary and you want validation + coercion. Use at REST/job-param boundaries.
- `TypedDict` — structural typing for dict-shaped data (common with Spark `Row.asDict()` or JSON).

### Structural pattern matching (3.10+)

```python
def route(event: dict) -> str:
    match event:
        case {"type": "insert", "table": t}:          return f"ingest:{t}"
        case {"type": "delete", "id": int(i)}:        return f"gc:{i}"
        case {"type": "merge", **rest} if rest:       return "merge"
        case _:                                       return "unknown"
```

Real use in Databricks: dispatching on event types inside `foreachBatch`, parsing webhook payloads, handling Unity Catalog audit events.

### Comprehensions, generators, walrus

```python
# Comprehension — eager
paths = [f"/Volumes/main/raw/{d}" for d in days]

# Generator — lazy, stream through without allocating
def chunks(it, n):
    buf = []
    for x in it:
        buf.append(x)
        if len(buf) == n:
            yield buf
            buf = []
    if buf: yield buf

# Walrus
while (line := stream.readline()):
    handle(line)
```

Use generators whenever you pipe through big sequences on the driver (e.g. paginating Databricks API responses).

### Context managers and `with`

```python
from contextlib import contextmanager

@contextmanager
def spark_conf(**kw):
    prev = {k: spark.conf.get(k, None) for k in kw}
    for k, v in kw.items(): spark.conf.set(k, v)
    try: yield
    finally:
        for k, v in prev.items():
            if v is None: spark.conf.unset(k)
            else: spark.conf.set(k, v)

with spark_conf(**{"spark.sql.shuffle.partitions": "16"}):
    df.write.saveAsTable("...")
```

### Decorators (you'll meet them via `@pandas_udf`, `@F.udf`, MLflow)

```python
from functools import wraps, lru_cache

def timed(fn):
    @wraps(fn)
    def inner(*a, **kw):
        import time; t = time.perf_counter()
        try: return fn(*a, **kw)
        finally: print(f"{fn.__name__}: {time.perf_counter()-t:.2f}s")
    return inner
```

`@lru_cache` is free memoization for pure driver-side functions. Useless inside Spark transforms (each task has its own process).

### Stdlib worth remembering

- `pathlib.Path` — over `os.path`.
- `itertools` — `chain`, `groupby`, `batched` (3.12+), `islice`.
- `functools` — `reduce`, `partial`, `cache`, `lru_cache`.
- `collections` — `defaultdict`, `Counter`, `deque`.
- `datetime` + `zoneinfo` — timezone-aware always. Never naive datetimes when writing to Delta.
- `json`, `csv` — for driver-side edge work only, never for bulk IO.

---

## 2. PySpark DataFrame API — the core you live in

### SparkSession

In notebooks `spark` exists. Elsewhere:

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
```

With Databricks Connect:

```python
from databricks.connect import DatabricksSession
spark = DatabricksSession.builder.getOrCreate()  # picks up your profile
```

### Reading and writing (Delta-first)

```python
# Read
df = spark.read.table("main.sales.orders")
df = spark.read.format("delta").load("/Volumes/main/sales/orders")
df = spark.read.option("header", True).csv("/Volumes/main/raw/*.csv")
df = spark.read.json(...)
df = spark.read.parquet(...)

# Write
(df.write
   .format("delta")
   .mode("overwrite")         # or "append", "errorifexists", "ignore"
   .option("overwriteSchema", "true")
   .partitionBy("event_date")
   .saveAsTable("main.sales.orders_clean"))
```

Prefer `saveAsTable` with Unity Catalog three-level names (`catalog.schema.table`) over raw paths. Use `path` option only for external tables.

### Transformations

```python
from pyspark.sql import functions as F, Window as W

out = (
    df
    .where(F.col("status") == "paid")
    .withColumn("amount_eur", F.col("amount") * F.col("fx_rate"))
    .withColumn("event_date", F.to_date("event_ts"))
    .groupBy("customer_id", "event_date")
    .agg(
        F.sum("amount_eur").alias("total"),
        F.countDistinct("order_id").alias("orders"),
    )
)
```

Key column builders:

- `F.col("x")`, `F.lit(0)`, `F.expr("x + y")`
- `F.when(cond, a).when(cond2, b).otherwise(c)`
- `F.coalesce(a, b, c)`
- Casts: `F.col("x").cast("decimal(18,4)")`
- Strings: `F.lower`, `F.regexp_extract`, `F.split`, `F.concat_ws`
- Dates: `F.to_date`, `F.date_trunc`, `F.date_add`, `F.datediff`
- Nulls: `F.col("x").isNull()`, `F.col("x").isNotNull()`

### Joins

```python
j = a.join(b, on="customer_id", how="left")
j = a.join(b, a.cid == b.customer_id, "inner")
# Broadcast small side explicitly when you know it fits
j = a.join(F.broadcast(small), "k", "left")
```

### Window functions

```python
w = W.partitionBy("customer_id").orderBy(F.col("event_ts").desc())
latest = df.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")
```

Also: `rank`, `dense_rank`, `lag`, `lead`, `sum().over(w)`, `avg().over(w.rowsBetween(-6,0))`.

### Explicit schemas — when CSV/JSON lies

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

schema = StructType([
    StructField("id", IntegerType(), nullable=False),
    StructField("name", StringType()),
    StructField("ts", TimestampType()),
])
df = spark.read.schema(schema).json("/Volumes/.../events/*.json")
```

### Lazy evaluation — the #1 trap

Transformations are lazy. Actions trigger execution: `count`, `collect`, `take`, `show`, `write.*`, `toPandas`.

- `df.collect()` pulls the whole DataFrame to the driver. Dangerous. Use `take(n)` or write to table.
- `df.show(n)` triggers a small action. Fine.
- `df.explain(True)` shows the physical plan. **Use it.** Knowing how to read plans separates people who guess at perf from people who know.

---

## 3. Spark SQL ↔ DataFrame — use both

```python
df.createOrReplaceTempView("orders_v")
agg = spark.sql("""
    select customer_id, sum(amount) total
    from orders_v
    where event_date >= date_sub(current_date(), 7)
    group by 1
""")
```

Parameterized SQL (modern, safe against injection):

```python
spark.sql(
    "select * from {tbl} where event_date >= :d",
    tbl=spark.table("main.sales.orders"),
    args={"d": "2026-01-01"},
)
```

DataFrame API vs SQL: pick whichever reads more cleanly at that step. Catalyst produces the same plan.

---

## 4. UDFs — know the hierarchy

**Order of preference** (always pick the highest that solves the problem):

1. **Native Spark functions** (`pyspark.sql.functions`) — JVM-native, fully optimized.
2. **Spark SQL expressions** via `F.expr(...)` — same thing, different syntax.
3. **Pandas UDFs** (`@pandas_udf`) — vectorized, Arrow-based, per-batch pandas Series in/out.
4. **Arrow-optimized Python UDFs** — modern row UDFs using Arrow (much faster than legacy).
5. **Legacy Python UDFs** (`@F.udf`) — row-at-a-time, serialization tax, slowest. Last resort.

```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def zscore(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std(ddof=0)

df = df.withColumn("amount_z", zscore("amount").over(W.partitionBy("sku")))
```

`applyInPandas` (group-wise, pandas DataFrame in/out) — when you need a pandas-shaped chunk per key:

```python
def fit_group(pdf: pd.DataFrame) -> pd.DataFrame:
    # fit a small model on pdf, return enriched rows
    pdf["pred"] = ...
    return pdf

out = df.groupBy("sku").applyInPandas(fit_group, schema="sku string, ts timestamp, pred double")
```

`mapInPandas` — when you want a streaming-ish pandas pipeline without grouping.

---

## 5. Delta Lake from Python

```python
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "main.sales.orders")

# MERGE (upsert)
(dt.alias("t")
   .merge(updates.alias("s"), "t.order_id = s.order_id")
   .whenMatchedUpdateAll()
   .whenNotMatchedInsertAll()
   .execute())

# Time travel
old = spark.read.option("versionAsOf", 12).table("main.sales.orders")
old = spark.read.option("timestampAsOf", "2026-04-01").table("main.sales.orders")

# Maintenance
spark.sql("OPTIMIZE main.sales.orders ZORDER BY (customer_id)")
spark.sql("VACUUM main.sales.orders RETAIN 168 HOURS")

# Change Data Feed (CDF)
cdc = (spark.read.format("delta")
       .option("readChangeFeed", "true")
       .option("startingVersion", 100)
       .table("main.sales.orders"))
# yields extra cols: _change_type, _commit_version, _commit_timestamp
```

Enable CDF at table creation: `TBLPROPERTIES (delta.enableChangeDataFeed = true)`.

Liquid Clustering (replaces ZORDER on new tables):

```sql
CREATE TABLE main.sales.orders (...)
USING DELTA
CLUSTER BY (customer_id, event_date);
```

---

## 6. Structured Streaming (Delta-first)

```python
stream = (
    spark.readStream.format("delta").table("main.raw.events")
         .withColumn("amount_eur", F.col("amount") * F.col("fx"))
)

query = (
    stream.writeStream
          .format("delta")
          .option("checkpointLocation", "/Volumes/main/chk/events_silver")
          .trigger(availableNow=True)     # or processingTime="30 seconds"
          .toTable("main.silver.events")
)
```

`foreachBatch` for per-microbatch logic (MERGE into Delta, call external APIs):

```python
def upsert(batch_df, batch_id):
    (DeltaTable.forName(spark, "main.silver.events").alias("t")
       .merge(batch_df.alias("s"), "t.id = s.id")
       .whenMatchedUpdateAll()
       .whenNotMatchedInsertAll()
       .execute())

stream.writeStream.foreachBatch(upsert).option("checkpointLocation", "...").start()
```

Triggers:
- `availableNow=True` — incremental batch; processes everything available, then stops. **The right default** for scheduled jobs.
- `processingTime="N seconds"` — continuous micro-batches. For always-on streams.
- `once=True` — deprecated; use `availableNow`.

---

## 7. `dbutils` — the notebook toolbelt

```python
# Widgets (parameterize notebooks / jobs)
dbutils.widgets.text("env", "dev")
dbutils.widgets.dropdown("region", "EU", ["EU", "US", "APAC"])
env = dbutils.widgets.get("env")

# Secrets (never hardcode)
token = dbutils.secrets.get("kv-scope", "external-api-token")

# Files (works on Volumes, DBFS, cloud URIs)
dbutils.fs.ls("/Volumes/main/raw/")
dbutils.fs.cp("src", "dst", recurse=True)
dbutils.fs.rm("path", recurse=True)

# Notebook orchestration (prefer Workflows/Jobs over this, but still useful)
dbutils.notebook.run("./child", timeout_seconds=600, arguments={"date": "2026-04-23"})
dbutils.notebook.exit("OK")   # return value to the caller
```

Outside notebooks (jobs/Connect) `dbutils` is limited. Replace `dbutils.fs.*` with the Files API via the SDK (see §9) or `open()` on `/Volumes/...` paths.

---

## 8. Unity Catalog from Python — the mental model

Three-level namespace: `catalog.schema.table`. Always use fully qualified names in production code; default catalog is a footgun.

Volumes replace DBFS paths for file data: `/Volumes/<catalog>/<schema>/<volume>/...`. You can `open()` these like local files from within a cluster.

```python
with open("/Volumes/main/raw/config/rules.json") as f:
    rules = json.load(f)
```

---

## 9. Databricks SDK for Python

Given your REST API work, this is probably your main leverage point.

```bash
pip install databricks-sdk
```

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()   # picks up DATABRICKS_HOST + DATABRICKS_TOKEN, or profile, or runtime auth

# Jobs
for job in w.jobs.list():
    print(job.job_id, job.settings.name)

# SQL Statement Execution (what you'd use for external Python pulling from warehouse)
resp = w.statement_execution.execute_statement(
    warehouse_id="abc123",
    statement="select count(*) from main.sales.orders where event_date = :d",
    parameters=[{"name": "d", "value": "2026-04-23"}],
    wait_timeout="30s",
)

# Files API (upload/download from Volumes, no cluster required)
with open("local.parquet", "rb") as f:
    w.files.upload("/Volumes/main/raw/ingest/local.parquet", f, overwrite=True)

# Unity Catalog metadata
for t in w.tables.list(catalog_name="main", schema_name="sales"):
    print(t.full_name, t.table_type)
```

Auth resolution order: env vars → `.databrickscfg` profile (`DATABRICKS_CONFIG_PROFILE`) → Databricks CLI session → inside-cluster identity. Clean — you rarely pass credentials explicitly.

Inside a notebook, `WorkspaceClient()` uses the runtime identity automatically.

---

## 10. MLflow — the 10-minute tour

Autolog covers sklearn, xgboost, pytorch, TF, LangChain, etc.:

```python
import mlflow
mlflow.autolog()

from sklearn.ensemble import RandomForestClassifier
with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100).fit(X, y)
    mlflow.log_metric("auc", 0.87)
    mlflow.log_param("n_estimators", 100)
```

Register + serve via Unity Catalog (the modern path):

```python
mlflow.set_registry_uri("databricks-uc")
mlflow.sklearn.log_model(model, "model", registered_model_name="main.ml.churn_rf")
```

Load for inference:

```python
import mlflow.pyfunc
m = mlflow.pyfunc.load_model("models:/main.ml.churn_rf@prod")
preds = m.predict(features_df)
```

`pyfunc` is the universal flavor — load any registered model uniformly.

---

## 11. Performance patterns — what actually matters

**Read `df.explain(True)` and `df.explain("formatted")`.** Everything else flows from understanding the plan.

- **Partitioning / clustering**: use Liquid Clustering on new Delta tables. On legacy, `partitionBy` only on low-cardinality columns (typically date-ish); `ZORDER BY` for high-cardinality filter columns.
- **Broadcast joins**: `F.broadcast(small)` when small side < ~100MB. AQE broadcasts automatically when stats are good.
- **AQE** is on by default (3.x). Don't turn it off. It handles skew, coalesces shuffle partitions, converts joins.
- **`repartition(n, col)` vs `coalesce(n)`**: `repartition` does a full shuffle; `coalesce` only reduces without shuffling (faster but can skew).
- **Cache judiciously**: `df.cache()` / `df.persist(StorageLevel.MEMORY_AND_DISK)` only when a DF is reused multiple times in the same job. Always `.unpersist()` when done.
- **Avoid `collect()`, `toPandas()` on big DFs.** If you must, sample first.
- **Prefer native functions over UDFs.** If you write a UDF, make it a Pandas UDF.
- **Photon**: if your cluster has Photon on, most SQL-heavy workloads get 2-3x for free. Python UDFs break Photon acceleration for their stage — another reason to avoid them.

---

## 12. Testing & local dev

### Databricks Connect (remote Spark on your laptop)

```bash
pip install databricks-connect==<dbr-version>
```

```python
from databricks.connect import DatabricksSession
spark = DatabricksSession.builder.profile("DEFAULT").getOrCreate()
```

Runs your local Python, executes Spark on the cluster. Ideal for IDE-driven dev with real data.

### Unit tests

```python
# tests/test_transforms.py
import pytest
from pyspark.sql import SparkSession
from mymodule import enrich

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[2]").appName("tests").getOrCreate()

def test_enrich(spark):
    df = spark.createDataFrame([(1, "a", 10.0)], "id int, k string, v double")
    out = enrich(df).collect()
    assert out[0].v_scaled == 1.0
```

`chispa` gives ergonomic DataFrame assertions: `assert_df_equality`, `assert_column_equality`.

### Structure code to be testable

Write transform functions that take and return DataFrames, with no IO inside:

```python
def enrich(orders: DataFrame, fx: DataFrame) -> DataFrame:
    return orders.join(fx, "ccy").withColumn("amount_eur", F.col("amount") * F.col("rate"))

# IO at the edges
def run():
    enrich(spark.read.table("raw.orders"), spark.read.table("ref.fx")) \
        .write.mode("overwrite").saveAsTable("silver.orders")
```

---

## 13. Modern local tooling (2026)

You'll feel this mostly on your laptop / CI, not inside the cluster:

- **`uv`** — Rust-based, replaces `pip` + `pip-tools` + `venv` + `pyenv`. Project management, fast installs, lockfile.
  ```bash
  uv init my-pipeline
  uv add pyspark databricks-sdk pandas
  uv run python job.py
  ```
- **`ruff`** — lint + format, single tool, replaces flake8/isort/black. Blazingly fast.
- **`pyright`** or **`mypy`** — type checker. Pyright is faster and smarter; mypy is the classic.
- **`pre-commit`** — run ruff/pyright on every commit.
- **Asset Bundles** (Databricks-specific) — YAML-defined jobs/pipelines deployed via the Databricks CLI. Treat your notebooks + jobs as code, in git.

---

## 14. Gotchas / anti-patterns you'll hit

- **pandas DataFrame ≠ Spark DataFrame.** They look similar but are wholly different beasts. Mix them only at explicit boundaries.
- **`.collect()` on a DF you didn't count first.** You just pulled 40GB into the driver.
- **Writing a Python UDF that a built-in already covers.** Search `pyspark.sql.functions` first.
- **Forgetting to cast timestamps**: Spark's `to_timestamp` + `zoneinfo`-aware datetimes only. Mixing naive and aware will bite in Delta.
- **Schema drift on append writes.** Either pin schemas or enable schema evolution (`mergeSchema`, `autoMerge.enabled`) deliberately.
- **Using DBFS paths (`/dbfs/...`, `dbfs:/...`) for new work.** Use Volumes (`/Volumes/cat/sch/vol/...`).
- **Hardcoding secrets in notebooks.** Always `dbutils.secrets.get`.
- **Mutating global state in notebooks and forgetting during job promotion.** Write pure functions; test them.
- **Running `OPTIMIZE` inline in ingest jobs.** Schedule separately.
- **Not setting `checkpointLocation`** on streaming writes — or reusing one across different queries. One checkpoint dir per query, always.
- **`spark.read.csv` with no schema.** Spark will infer by scanning the file — slow and fragile. Pass a `schema`.

---

## 15. What to re-read when you're rusty on something specific

- **PySpark API reference** — `pyspark.sql.functions` and `pyspark.sql.DataFrame` docs are worth bookmarking; 80% of daily work lives there.
- **Delta Lake docs** — MERGE semantics, CDF, Liquid Clustering.
- **Databricks SDK for Python** docs — auth, Files API, Jobs API, Statement Execution.
- **AQE deep dive** on the Databricks blog — changes how you think about partitioning.

---

## TL;DR cheat sheet

| Need                          | Use                                                         |
|-------------------------------|-------------------------------------------------------------|
| Transform a table             | DataFrame API + `functions as F`                            |
| Upsert                        | `DeltaTable.merge`                                          |
| Periodic incremental job      | Structured Streaming with `trigger(availableNow=True)`      |
| Custom per-row logic          | Pandas UDF > Arrow UDF > Python UDF                         |
| Per-group custom logic        | `applyInPandas`                                             |
| Parameterize a notebook       | `dbutils.widgets`                                           |
| Secrets                       | `dbutils.secrets.get`                                       |
| File IO (new)                 | Volumes (`/Volumes/...`) + `open()` or SDK Files API        |
| Call Databricks from outside  | `databricks-sdk` `WorkspaceClient`                          |
| Query warehouse from Python   | SDK `statement_execution.execute_statement`                 |
| Test transforms locally       | Databricks Connect + pytest + chispa                        |
| Manage Python project locally | `uv` + `ruff` + `pyright`                                   |
| Deploy notebooks/jobs as code | Databricks Asset Bundles                                    |
