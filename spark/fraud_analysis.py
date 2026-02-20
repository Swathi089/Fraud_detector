"""
spark/fraud_analysis.py
========================
Fraud analysis module for the Fraud Detection System.
Provides risk scoring, fraud flagging, and detailed statistics using PySpark.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, sum as spark_sum, avg, stddev, min as spark_min, max as spark_max
from pyspark.sql.functions import abs as spark_abs, rand, log1p, sqrt, pandas_udf, PandasUDFType
from pyspark.sql.types import IntegerType, DoubleType, StringType
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_fraud(df: DataFrame) -> dict:
    """
    Main fraud analysis function that performs all analysis tasks.

    Args:
        df (DataFrame): Preprocessed Spark DataFrame

    Returns:
        dict: Comprehensive fraud analysis results
    """
    logger.info("Starting fraud analysis")

    # Run all analysis components
    stats = fraud_statistics(df)
    risk_scores = calculate_risk_scores(df)
    risk_distribution = get_risk_distribution(df)
    detailed_stats = get_detailed_statistics(df)
    top_risky = get_top_risky_transactions(df, n=10)

    results = {
        **stats,
        "risk_scores": risk_scores,
        "risk_distribution": risk_distribution,
        "detailed_statistics": detailed_stats,
        "top_risky_transactions": top_risky
    }

    logger.info("Fraud analysis completed")
    return results


def fraud_statistics(df: DataFrame) -> dict:
    """
    Calculate basic fraud statistics.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        dict: Basic fraud statistics
    """
    logger.info("Calculating fraud statistics")

    total = df.count()
    fraud = df.filter(col("Class") == 1).count(
    ) if "Class" in df.columns else 0
    non_fraud = total - fraud

    fraud_percentage = round((fraud / total) * 100, 4) if total > 0 else 0
    non_fraud_percentage = round(
        (non_fraud / total) * 100, 4) if total > 0 else 0

    stats = {
        "total_transactions": total,
        "fraud_transactions": fraud,
        "non_fraud_transactions": non_fraud,
        "fraud_percentage": fraud_percentage,
        "non_fraud_percentage": non_fraud_percentage
    }

    logger.info(f"Statistics: {stats}")
    return stats


def calculate_risk_scores(df: DataFrame) -> dict:
    """
    Calculate risk scores for each transaction based on multiple factors.
    Risk score ranges from 0 (low risk) to 100 (high risk).

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        dict: Risk score statistics
    """
    logger.info("Calculating risk scores")

    # Create a copy to avoid modifying original DataFrame
    df_with_risk = df

    # Check if Class column exists (for labeled data)
    if "Class" in df.columns:
        # For labeled data, use actual fraud labels plus additional risk factors
        df_with_risk = df_with_risk.withColumn("risk_score",
                                               # Known fraud gets max risk
                                               when(col("Class") == 1, 100.0)
                                               .otherwise(calculate_base_risk(col("Amount"), col("Time"))))
    else:
        # For unlabeled data, use only behavioral risk factors
        df_with_risk = df_with_risk.withColumn("risk_score",
                                               calculate_base_risk(col("Amount"), col("Time")))

    # Calculate risk score statistics
    risk_stats = df_with_risk.agg(
        avg("risk_score").alias("avg_risk_score"),
        stddev("risk_score").alias("std_risk_score"),
        spark_min("risk_score").alias("min_risk_score"),
        spark_max("risk_score").alias("max_risk_score")
    ).collect()[0]

    # Calculate risk distribution
    risk_distribution = df_with_risk.select(
        when(col("risk_score") >= 70, "High")
        .when(col("risk_score") >= 30, "Medium")
        .otherwise("Low").alias("risk_level")
    ).groupBy("risk_level").count().collect()

    risk_dist_dict = {}
    for row in risk_distribution:
        risk_dist_dict[row["risk_level"]] = row["count"]

    result = {
        "average_risk_score": round(risk_stats["avg_risk_score"], 2) if risk_stats["avg_risk_score"] else 0,
        "std_risk_score": round(risk_stats["std_risk_score"], 2) if risk_stats["std_risk_score"] else 0,
        "min_risk_score": round(risk_stats["min_risk_score"], 2) if risk_stats["min_risk_score"] else 0,
        "max_risk_score": round(risk_stats["max_risk_score"], 2) if risk_stats["max_risk_score"] else 0,
        "risk_distribution": risk_dist_dict
    }

    logger.info(f"Risk score statistics: {result}")
    return result


def calculate_base_risk(amount_col, time_col):
    """
    Calculate base risk score based on transaction amount and time.

    Args:
        amount_col: Amount column
        time_col: Time column

    Returns:
        Column: Risk score calculation
    """
    from pyspark.sql.functions import when, abs as spark_abs, log1p, sqrt, rand

    # Amount-based risk (higher amounts = higher risk)
    amount_risk = when(amount_col.isNull(), 20).otherwise(
        when(amount_col > 10000, 40)
        .when(amount_col > 5000, 30)
        .when(amount_col > 1000, 20)
        .when(amount_col > 500, 10)
        .otherwise(5)
    )

    # Time-based risk (unusual times might indicate fraud)
    time_risk = when(time_col.isNull(), 10).otherwise(
        when((time_col < 3600) | (time_col > 82800), 20)  # Night hours
        .otherwise(10)
    )

    # Random factor for variation (simulates behavioral analysis)
    random_risk = (rand() * 20).cast(IntegerType())

    # Base risk score
    base_risk = amount_risk + time_risk + random_risk

    return base_risk


def get_risk_distribution(df: DataFrame) -> dict:
    """
    Get distribution of transactions by risk level.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        dict: Risk level distribution
    """
    logger.info("Calculating risk distribution")

    # Add risk levels
    df_with_levels = df.withColumn("risk_level",
                                   when(col("risk_score") >= 70, "High")
                                   .when(col("risk_score") >= 30, "Medium")
                                   .otherwise("Low")
                                   )

    # Count by risk level
    distribution = df_with_levels.groupBy("risk_level").count().collect()

    dist_dict = {}
    for row in distribution:
        dist_dict[row["risk_level"]] = row["count"]

    logger.info(f"Risk distribution: {dist_dict}")
    return dist_dict


def get_detailed_statistics(df: DataFrame) -> dict:
    """
    Get detailed statistics for fraud and non-fraud transactions.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        dict: Detailed statistics
    """
    logger.info("Calculating detailed statistics")

    detailed_stats = {}

    if "Class" not in df.columns:
        return detailed_stats

    # Get statistics for fraud transactions
    fraud_df = df.filter(col("Class") == 1)
    non_fraud_df = df.filter(col("Class") == 0)

    # Amount statistics
    if "Amount" in df.columns:
        fraud_amount_stats = fraud_df.agg(
            avg("Amount").alias("avg_amount"),
            spark_sum("Amount").alias("total_amount"),
            spark_min("Amount").alias("min_amount"),
            spark_max("Amount").alias("max_amount"),
            stddev("Amount").alias("std_amount")
        ).collect()[0]

        non_fraud_amount_stats = non_fraud_df.agg(
            avg("Amount").alias("avg_amount"),
            spark_sum("Amount").alias("total_amount"),
            spark_min("Amount").alias("min_amount"),
            spark_max("Amount").alias("max_amount"),
            stddev("Amount").alias("std_amount")
        ).collect()[0]

        detailed_stats["fraud_amount"] = {
            "average": round(fraud_amount_stats["avg_amount"], 2) if fraud_amount_stats["avg_amount"] else 0,
            "total": round(fraud_amount_stats["total_amount"], 2) if fraud_amount_stats["total_amount"] else 0,
            "min": round(fraud_amount_stats["min_amount"], 2) if fraud_amount_stats["min_amount"] else 0,
            "max": round(fraud_amount_stats["max_amount"], 2) if fraud_amount_stats["max_amount"] else 0,
            "std": round(fraud_amount_stats["std_amount"], 2) if fraud_amount_stats["std_amount"] else 0
        }

        detailed_stats["non_fraud_amount"] = {
            "average": round(non_fraud_amount_stats["avg_amount"], 2) if non_fraud_amount_stats["avg_amount"] else 0,
            "total": round(non_fraud_amount_stats["total_amount"], 2) if non_fraud_amount_stats["total_amount"] else 0,
            "min": round(non_fraud_amount_stats["min_amount"], 2) if non_fraud_amount_stats["min_amount"] else 0,
            "max": round(non_fraud_amount_stats["max_amount"], 2) if non_fraud_amount_stats["max_amount"] else 0,
            "std": round(non_fraud_amount_stats["std_amount"], 2) if non_fraud_amount_stats["std_amount"] else 0
        }

    # Time-based statistics
    if "Time" in df.columns:
        fraud_time_stats = fraud_df.agg(
            avg("Time").alias("avg_time"),
            spark_min("Time").alias("min_time"),
            spark_max("Time").alias("max_time")
        ).collect()[0]

        non_fraud_time_stats = non_fraud_df.agg(
            avg("Time").alias("avg_time"),
            spark_min("Time").alias("min_time"),
            spark_max("Time").alias("max_time")
        ).collect()[0]

        detailed_stats["fraud_time"] = {
            "average": round(fraud_time_stats["avg_time"], 2) if fraud_time_stats["avg_time"] else 0,
            "min": round(fraud_time_stats["min_time"], 2) if fraud_time_stats["min_time"] else 0,
            "max": round(fraud_time_stats["max_time"], 2) if fraud_time_stats["max_time"] else 0
        }

        detailed_stats["non_fraud_time"] = {
            "average": round(non_fraud_time_stats["avg_time"], 2) if non_fraud_time_stats["avg_time"] else 0,
            "min": round(non_fraud_time_stats["min_time"], 2) if non_fraud_time_stats["min_time"] else 0,
            "max": round(non_fraud_time_stats["max_time"], 2) if non_fraud_time_stats["max_time"] else 0
        }

    logger.info(
        f"Detailed statistics calculated: {len(detailed_stats)} categories")
    return detailed_stats


def get_top_risky_transactions(df: DataFrame, n: int = 10) -> list:
    """
    Get the top N most risky transactions.

    Args:
        df (DataFrame): Input DataFrame
        n (int): Number of top transactions to return

    Returns:
        list: List of top risky transactions
    """
    logger.info(f"Finding top {n} risky transactions")

    if "risk_score" not in df.columns:
        logger.warning("No risk_score column found")
        return []

    # Get top risky transactions
    top_risky = df.orderBy(col("risk_score").desc()).limit(n)

    # Convert to list of dictionaries
    results = top_risky.collect()
    transactions = []

    for row in results:
        row_dict = row.asDict()
        # Convert any non-serializable types
        for key, value in row_dict.items():
            if hasattr(value, 'java_ref'):
                row_dict[key] = str(value)
        transactions.append(row_dict)

    logger.info(f"Found {len(transactions)} top risky transactions")
    return transactions


def flag_fraud_transactions(df: DataFrame, threshold: float = 70.0) -> DataFrame:
    """
    Flag transactions as potential fraud based on risk score threshold.

    Args:
        df (DataFrame): Input DataFrame with risk_score column
        threshold (float): Risk score threshold for fraud flagging

    Returns:
        DataFrame: DataFrame with fraud_flag column
    """
    logger.info(f"Flagging transactions with threshold: {threshold}")

    df_flagged = df.withColumn("fraud_flag",
                               when(col("risk_score") >= threshold, 1)
                               .otherwise(0)
                               )

    flagged_count = df_flagged.filter(col("fraud_flag") == 1).count()
    logger.info(f"Flagged {flagged_count} transactions as potential fraud")

    return df_flagged
