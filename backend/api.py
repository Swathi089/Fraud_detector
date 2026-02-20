"""
backend/api.py
==============
Backend API module for the Fraud Detection System.
Provides functions for running Spark-based fraud analysis.
"""

from spark.fraud_analysis import analyze_fraud, flag_fraud_transactions
from spark.preprocessing import preprocess, get_data_summary
from spark.spark_session import get_spark, stop_spark
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col
import logging
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global Spark session
_spark = None


def get_spark_session():
    """
    Get or create a Spark session.

    Returns:
        SparkSession: Active Spark session
    """
    global _spark
    if _spark is None:
        _spark = get_spark()
    return _spark


def load_data(csv_path: str, options: dict = None) -> DataFrame:
    """
    Load data from CSV file into Spark DataFrame.

    Args:
        csv_path (str): Path to the CSV file
        options (dict): Additional options for loading

    Returns:
        DataFrame: Loaded Spark DataFrame
    """
    logger.info(f"Loading data from {csv_path}")

    spark = get_spark_session()

    # Default options
    load_options = {
        "header": True,
        "inferSchema": True
    }

    # Override with custom options
    if options:
        load_options.update(options)

    # Load CSV
    df = spark.read.csv(csv_path, **load_options)

    logger.info(f"Loaded {df.count()} rows with {len(df.columns)} columns")

    return df


def run_analysis(csv_path: str, preprocessing_options: dict = None) -> dict:
    """
    Run complete fraud analysis on the dataset.

    Args:
        csv_path (str): Path to the CSV file
        preprocessing_options (dict): Options for preprocessing

    Returns:
        dict: Analysis results including statistics, risk scores, etc.
    """
    logger.info("Starting complete fraud analysis")

    try:
        # Load data
        df = load_data(csv_path)

        # Preprocess data
        df_processed = preprocess(df, preprocessing_options)

        # Get data summary
        data_summary = get_data_summary(df_processed)

        # Analyze fraud
        analysis_results = analyze_fraud(df_processed)

        # Combine results
        results = {
            "data_summary": data_summary,
            "fraud_analysis": analysis_results,
            "status": "success",
            "message": "Analysis completed successfully"
        }

        logger.info("Analysis completed successfully")
        return results

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def run_preprocessing(csv_path: str, output_path: str = None) -> dict:
    """
    Run preprocessing on the dataset.

    Args:
        csv_path (str): Path to the input CSV file
        output_path (str): Path to save preprocessed data (optional)

    Returns:
        dict: Preprocessing results
    """
    logger.info("Starting preprocessing")

    try:
        # Load data
        df = load_data(csv_path)

        # Preprocess data
        df_processed = preprocess(df)

        # Get data summary
        summary = get_data_summary(df_processed)

        # Save if output path provided
        if output_path:
            df_processed.write.csv(output_path, header=True, mode="overwrite")
            logger.info(f"Preprocessed data saved to {output_path}")

        results = {
            "status": "success",
            "data_summary": summary,
            "message": "Preprocessing completed successfully"
        }

        logger.info("Preprocessing completed")
        return results

    except Exception as e:
        logger.error(f"Error during preprocessing: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def run_fraud_detection(csv_path: str, threshold: float = 70.0) -> dict:
    """
    Run fraud detection with risk scoring and flagging.

    Args:
        csv_path (str): Path to the CSV file
        threshold (float): Risk score threshold for fraud flagging

    Returns:
        dict: Fraud detection results
    """
    logger.info("Starting fraud detection")

    try:
        # Load and preprocess
        df = load_data(csv_path)
        df_processed = preprocess(df)

        # Analyze fraud
        analysis_results = analyze_fraud(df_processed)

        # Flag fraud transactions
        df_flagged = flag_fraud_transactions(df_processed, threshold)

        # Get flagging statistics
        flagged_count = df_flagged.filter(col("fraud_flag") == 1).count()

        results = {
            "status": "success",
            "analysis": analysis_results,
            "flagged_transactions": flagged_count,
            "threshold": threshold,
            "message": "Fraud detection completed successfully"
        }

        logger.info(
            f"Fraud detection completed. Flagged {flagged_count} transactions")
        return results

    except Exception as e:
        logger.error(f"Error during fraud detection: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def get_dataset_info(csv_path: str) -> dict:
    """
    Get information about the dataset.

    Args:
        csv_path (str): Path to the CSV file

    Returns:
        dict: Dataset information
    """
    logger.info("Getting dataset info")

    try:
        df = load_data(csv_path)

        info = {
            "row_count": df.count(),
            "column_count": len(df.columns),
            "columns": df.columns,
            "schema": df.schema.json()
        }

        logger.info(
            f"Dataset info: {info['row_count']} rows, {info['column_count']} columns")
        return info

    except Exception as e:
        logger.error(f"Error getting dataset info: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def cleanup():
    """
    Clean up resources (stop Spark session).
    """
    global _spark
    if _spark:
        stop_spark()
        _spark = None
        logger.info("Spark session stopped")
