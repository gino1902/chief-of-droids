"""Unit test for the provenance helper (ADR-007). Runs on the CI agent, no cluster."""

from pyspark.sql import SparkSession

from utils.shared_transforms import with_provenance


def test_with_provenance_adds_columns():
    spark = SparkSession.builder.master("local[1]").getOrCreate()
    df = spark.createDataFrame([("a",)], ["payload"])
    out = with_provenance(df, source_path_col="payload")
    assert "_ingested_at" in out.columns
    assert "_source_file" in out.columns
