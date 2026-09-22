"""
PySpark Session Management and Bridge Service
Provides an optimized local SparkSession with Arrow and memory tuning.
"""

import sys
import os
from pyspark.sql import SparkSession

class SparkManager:
    _instance = None
    _spark = None

    @classmethod
    def get_spark(cls) -> SparkSession:
        if cls._spark is None:
            # Set python executable for worker and driver
            os.environ['PYSPARK_PYTHON'] = sys.executable
            os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

            # Windows Hadoop / Winutils configuration
            hadoop_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "hadoop_bin"))
            if os.path.exists(hadoop_dir):
                os.environ['HADOOP_HOME'] = hadoop_dir
                os.environ['hadoop.home.dir'] = hadoop_dir
                os.environ['PATH'] = os.path.join(hadoop_dir, "bin") + ";" + r"C:\Windows\System32" + ";" + os.environ.get('PATH', '')

            cls._spark = (
                SparkSession.builder
                .appName("NYCTaxiRealTimeAnalytics")
                .master("local[1]")
                .config("spark.driver.memory", "2g")
                .config("spark.sql.shuffle.partitions", "2")
                .config("spark.default.parallelism", "2")
                .config("spark.sql.execution.arrow.pyspark.enabled", "false")
                .config("spark.sql.adaptive.enabled", "false")
                .config("spark.ui.enabled", "false")
                .getOrCreate()
            )
            cls._spark.sparkContext.setLogLevel("ERROR")
        return cls._spark

    @classmethod
    def is_available(cls) -> bool:
        try:
            spark = cls.get_spark()
            return spark is not None and not spark.sparkContext._jsc.sc().isStopped()
        except Exception:
            return False

