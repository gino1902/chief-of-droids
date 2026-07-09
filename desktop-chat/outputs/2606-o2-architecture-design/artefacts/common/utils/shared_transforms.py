"""Shared pure functions imported by pipelines across bundles.

Synced into each bundle's workspace path via sync.paths (ADR-003). Keep this module
free of pipeline decorators so it stays unit-testable on its own. Conformed entity
and metric definitions live in the silver bundle (ADR-001); this holds only generic
helpers.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def with_provenance(df: DataFrame, source_path_col: str = "_metadata.file_path") -> DataFrame:
    """Add ingest timestamp and source-file provenance columns (ADR-008)."""
    return df.withColumn("_ingested_at", F.current_timestamp()).withColumn(
        "_source_file", F.col(source_path_col)
    )
