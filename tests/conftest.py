import pytest
import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark() -> SparkSession:
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    os.environ["PYSPARK_PIN_THREAD"] = "true"
    
    if os.name == "nt":
        hadoop_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hadoop_bin"))
        os.environ["HADOOP_HOME"] = hadoop_path
        os.environ["hadoop.home.dir"] = hadoop_path
        os.environ["PATH"] = os.path.join(hadoop_path, "bin") + os.pathsep + r"C:\Windows\System32" + os.pathsep + os.environ.get("PATH", "")

    spark_session = (
        SparkSession.builder.master("local[1]")
        .appName("nyc-taxi-tests")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.execution.pyspark.worker.setupTimeout", "120s")
        .config("spark.network.timeout", "800s")
        .config("spark.executor.heartbeatInterval", "60s")
        .getOrCreate()
    )
    yield spark_session
    spark_session.stop()

