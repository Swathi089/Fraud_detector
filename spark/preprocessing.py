"""
spark/preprocessing.py
=======================
Data preprocessing module for the Fraud Detection System.
Handles missing values, scaling, encoding, and feature engineering using PySpark.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, count, isnan, stddev, mean, min as spark_min, max as spark_max
from pyspark.sql.types import NumericType
from pyspark.ml.feature import StandardScaler, VectorAssembler, StringIndexer
from pyspark.ml import Pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def preprocess(df: DataFrame, options: dict = None) -> DataFrame:
    """
    Main preprocessing function that applies all preprocessing steps.

    Args:
        df (DataFrame): Input Spark DataFrame
        options (dict): Optional configuration dictionary

    Returns:
        DataFrame: Preprocessed DataFrame
    """
    logger.info("Starting data preprocessing")

    # Apply preprocessing steps
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = validate_data(df)

    if options and options.get("scale", True):
        df = scale_numerical_features(df)

    if options and options.get("encode", True):
        df = encode_categorical_features(df)

    logger.info("Preprocessing completed")
    return df


def handle_missing_values(df: DataFrame) -> DataFrame:
    """
    Handle missing values in the dataset.
    - For numerical columns: fill with median
    - For categorical columns: fill with mode or 'Unknown'

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: DataFrame with missing values handled
    """
    logger.info("Handling missing values")

    # Count missing values before
    total_missing = df.select(
        [count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in df.columns])
    logger.info(
        f"Missing values count before: {total_missing.collect()[0].asDict()}")

    # Get column types
    numerical_cols = [c for c in df.columns if isinstance(
        df.schema[c].dataType, NumericType)]
    categorical_cols = [c for c in df.columns if c not in numerical_cols]

    # Fill missing values for numerical columns with median
    for col_name in numerical_cols:
        median_value = df.approxQuantile(col_name, [0.5], 0.01)[0]
        if median_value is not None:
            df = df.fillna({col_name: median_value})
            logger.info(
                f"Filled missing values in {col_name} with median: {median_value}")

    # Fill missing values for categorical columns with 'Unknown'
    for col_name in categorical_cols:
        df = df.fillna({col_name: "Unknown"})
        logger.info(f"Filled missing values in {col_name} with 'Unknown'")

    return df


def remove_duplicates(df: DataFrame) -> DataFrame:
    """
    Remove duplicate rows from the DataFrame.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: DataFrame with duplicates removed
    """
    logger.info("Removing duplicate rows")

    initial_count = df.count()
    df = df.dropDuplicates()
    final_count = df.count()

    duplicates_removed = initial_count - final_count
    logger.info(f"Removed {duplicates_removed} duplicate rows")

    return df


def validate_data(df: DataFrame) -> DataFrame:
    """
    Validate and clean data.
    - Remove rows with invalid values
    - Filter out negative values for certain columns (e.g., Amount, Time)

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: Validated DataFrame
    """
    logger.info("Validating data")

    initial_count = df.count()

    # Validate Amount column if exists
    if "Amount" in df.columns:
        df = df.filter(col("Amount") >= 0)
        logger.info("Filtered negative Amount values")

    # Validate Time column if exists
    if "Time" in df.columns:
        df = df.filter(col("Time") >= 0)
        logger.info("Filtered negative Time values")

    # Validate Class column if exists (should be 0 or 1)
    if "Class" in df.columns:
        df = df.filter(col("Class").isin([0, 1]))
        logger.info("Filtered invalid Class values")

    final_count = df.count()
    invalid_removed = initial_count - final_count
    logger.info(f"Removed {invalid_removed} invalid rows")

    return df


def scale_numerical_features(df: DataFrame, exclude_cols: list = None) -> DataFrame:
    """
    Scale numerical features using StandardScaler.

    Args:
        df (DataFrame): Input DataFrame
        exclude_cols (list): Columns to exclude from scaling

    Returns:
        DataFrame: DataFrame with scaled numerical features
    """
    logger.info("Scaling numerical features")

    if exclude_cols is None:
        exclude_cols = ["Class", "Time"]

    # Get numerical columns to scale
    numerical_cols = [c for c in df.columns
                      if isinstance(df.schema[c].dataType, NumericType)
                      and c not in exclude_cols]

    if not numerical_cols:
        logger.info("No numerical columns to scale")
        return df

    # Create feature vector
    assembler = VectorAssembler(
        inputCols=numerical_cols, outputCol="features_unscaled")
    df = assembler.transform(df)

    # Apply StandardScaler
    scaler = StandardScaler(inputCol="features_unscaled",
                            outputCol="features", withStd=True, withMean=True)
    scaler_model = scaler.fit(df)
    df = scaler_model.transform(df)

    # Drop intermediate columns
    df = df.drop("features_unscaled")

    logger.info(f"Scaled {len(numerical_cols)} numerical columns")

    return df


def encode_categorical_features(df: DataFrame, exclude_cols: list = None) -> DataFrame:
    """
    Encode categorical features using StringIndexer.

    Args:
        df (DataFrame): Input DataFrame
        exclude_cols (list): Columns to exclude from encoding

    Returns:
        DataFrame: DataFrame with encoded categorical features
    """
    logger.info("Encoding categorical features")

    if exclude_cols is None:
        exclude_cols = ["Class"]

    # Get categorical columns to encode
    categorical_cols = [c for c in df.columns
                        if not isinstance(df.schema[c].dataType, NumericType)
                        and c not in exclude_cols]

    if not categorical_cols:
        logger.info("No categorical columns to encode")
        return df

    # Create indexers
    indexers = [StringIndexer(inputCol=c, outputCol=c + "_indexed", handleInvalid="keep")
                for c in categorical_cols]

    # Create pipeline
    pipeline = Pipeline(stages=indexers)
    model = pipeline.fit(df)
    df = model.transform(df)

    logger.info(f"Encoded {len(categorical_cols)} categorical columns")

    return df


def get_data_summary(df: DataFrame) -> dict:
    """
    Get summary statistics of the dataset.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        dict: Summary statistics
    """
    logger.info("Generating data summary")

    # Basic stats
    total_rows = df.count()
    total_cols = len(df.columns)

    # Numerical summary
    numerical_cols = [c for c in df.columns if isinstance(
        df.schema[c].dataType, NumericType)]
    numerical_summary = df.select(numerical_cols).describe().collect()

    # Missing values
    missing_counts = df.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c)
                               for c in df.columns]).collect()[0].asDict()

    summary = {
        "total_rows": total_rows,
        "total_columns": total_cols,
        "numerical_columns": numerical_cols,
        "missing_values": missing_counts,
        "numerical_summary": {row.asDict()["summary"]: row.asDict() for row in numerical_summary}
    }

    logger.info(f"Data summary: {total_rows} rows, {total_cols} columns")

    return summary
