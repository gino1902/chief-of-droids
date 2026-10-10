# Thin notebook entrypoints calling a wheel

Pattern for Azure Databricks Asset Bundles, medallion layer-first package layout.

## Wheel side, the testable part

```python
# src/o2_platform/bronze/source_1/ingest.py
from pyspark.sql import DataFrame, SparkSession


def read_stream(spark: SparkSession, landing_path: str, schema_path: str) -> DataFrame:
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", schema_path)
        .load(landing_path)
    )


def transform(df: DataFrame) -> DataFrame:
    from pyspark.sql import functions as F

    return df.withColumn("_ingested_at", F.current_timestamp()).withColumn(
        "_source_file", F.col("_metadata.file_path")
    )


def run(spark: SparkSession, landing_path: str, checkpoint_path: str,
        schema_path: str, target_table: str) -> None:
    (
        transform(read_stream(spark, landing_path, schema_path))
        .writeStream.option("checkpointLocation", checkpoint_path)
        .trigger(availableNow=True)
        .toTable(target_table)
    )
```

## Notebook side, parameter binding and one call

```python
# src/notebooks/bronze/source_1_ingest.py
# Databricks notebook source
from o2_platform.bronze.source_1 import ingest

dbutils.widgets.text("landing_path", "")
dbutils.widgets.text("checkpoint_path", "")
dbutils.widgets.text("schema_path", "")
dbutils.widgets.text("target_table", "")

ingest.run(
    spark,
    landing_path=dbutils.widgets.get("landing_path"),
    checkpoint_path=dbutils.widgets.get("checkpoint_path"),
    schema_path=dbutils.widgets.get("schema_path"),
    target_table=dbutils.widgets.get("target_table"),
)
```

## Bundle side, where the environment differences live

```yaml
# resources/job_bronze_source_1.yml
resources:
  jobs:
    bronze_source_1:
      name: bronze_source_1
      tasks:
        - task_key: ingest
          notebook_task:
            notebook_path: ../src/notebooks/bronze/source_1_ingest.py
            base_parameters:
              landing_path: ${var.landing_root}/source_1
              checkpoint_path: ${var.checkpoint_root}/bronze/source_1
              schema_path: ${var.checkpoint_root}/schemas/source_1
              target_table: ${var.catalog}.bronze.source_1_events
          libraries:
            - whl: ../dist/*.whl
```

## Unit test, never touches Databricks

```python
# tests/unit/bronze/test_source_1.py
def test_transform_adds_audit_columns(spark):
    df = spark.createDataFrame([("a",)], "id string")
    out = transform(df)
    assert "_ingested_at" in out.columns
```

## Notes

`transform` is separated from `read_stream` deliberately, because it is the only piece that is pure and therefore cheaply testable.

The notebook holds zero logic, so it needs no test.

With Lakeflow Declarative Pipelines the shape differs. The entrypoint is a pipeline source file using `@dp.table` decorators rather than a `notebook_task`, but the same rule holds, the decorated function body should be one call into the wheel.

> ⚠️ Unverified — LDP decorator module and import name have changed across releases. Check current docs before writing pipeline files.
