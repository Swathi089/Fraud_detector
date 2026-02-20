"""
spark/spark_session.py
=======================
Centralized Spark session management for the Fraud Detection System.
This module provides a singleton Spark session to ensure efficient resource usage.
"""

from pyspark.sql import SparkSession
from pyspark import SparkConf
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SparkSessionManager:
    """
    Manages Spark session creation and configuration.
    Implements singleton pattern to ensure only one Spark session exists.
    """

    _spark_session = None

    @classmethod
    def get_spark_session(cls, app_name="FraudDetection", master="local[*]"):
        """
        Get or create a Spark session.

        Args:
            app_name (str): Name of the Spark application
            master (str): Spark master URL (e.g., "local[*]", "spark://host:port")

        Returns:
            SparkSession: Active Spark session
        """
        if cls._spark_session is None:
            logger.info(f"Creating new Spark session: {app_name}")

            # Configure Spark settings
            conf = SparkConf()
            conf.set("spark.app.name", app_name)
            conf.set("spark.master", master)

            # Memory settings - adjust based on available resources
            conf.set("spark.driver.memory", "4g")
            conf.set("spark.executor.memory", "2g")
            conf.set("spark.sql.shuffle.partitions", "8")

            # Optimization settings
            conf.set("spark.sql.adaptive.enabled", "true")
            conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

            # Create Spark session
            cls._spark_session = SparkSession.builder \
                .config(conf=conf) \
                .getOrCreate()

            # Set log level
            cls._spark_session.sparkContext.setLogLevel("WARN")

            logger.info("Spark session created successfully")
        else:
            logger.info("Reusing existing Spark session")

        return cls._spark_session

    @classmethod
    def stop_spark_session(cls):
        """
        Stop the Spark session and release resources.
        """
        if cls._spark_session is not None:
            logger.info("Stopping Spark session")
            cls._spark_session.stop()
            cls._spark_session = None
            logger.info("Spark session stopped")


def get_spark():
    """
    Convenience function to get the Spark session.

    Returns:
        SparkSession: Active Spark session
    """
    return SparkSessionManager.get_spark_session()


def stop_spark():
    """
    Convenience function to stop the Spark session.
    """
    SparkSessionManager.stop_spark_session()
