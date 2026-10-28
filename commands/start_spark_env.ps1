# ============================================================
# Spark Learning Project
# Local Spark Development Environment
# ============================================================

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

$PROJECT_ROOT = "D:\Project\Python\spark-learning"

$PYTHON_EXE = "$PROJECT_ROOT\.venv\Scripts\python.exe"

$HADOOP_HOME_PATH = "$PROJECT_ROOT\hadoop"

$SPARK_CONF_PATH = "$PROJECT_ROOT\conf"

$HADOOP_BIN = "$HADOOP_HOME_PATH\bin"

$WINUTILS = "$HADOOP_BIN\winutils.exe"

$HIVE_SITE = "$SPARK_CONF_PATH\hive-site.xml"


# ------------------------------------------------------------
# 2. Set environment variables
# ------------------------------------------------------------

$env:HADOOP_HOME = $HADOOP_HOME_PATH

${env:hadoop.home.dir} = $HADOOP_HOME_PATH

$env:SPARK_CONF_DIR = $SPARK_CONF_PATH

$env:PYSPARK_PYTHON = $PYTHON_EXE

$env:PYSPARK_DRIVER_PYTHON = $PYTHON_EXE


# ------------------------------------------------------------
# 3. Add Hadoop bin to PATH
# ------------------------------------------------------------

if ($env:Path -notlike "*$HADOOP_BIN*") {
    $env:Path = "$HADOOP_BIN;$env:Path"
}


# ------------------------------------------------------------
# 4. Check Python
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================================"
Write-Host " Spark Learning Environment"
Write-Host "============================================================"
Write-Host ""

if (-not (Test-Path $PYTHON_EXE)) {
    Write-Host "[ERROR] Python not found:"
    Write-Host $PYTHON_EXE
    exit 1
}

Write-Host "[OK] Python"
Write-Host "     $PYTHON_EXE"


# ------------------------------------------------------------
# 5. Check Hadoop
# ------------------------------------------------------------

if (-not (Test-Path $HADOOP_HOME_PATH)) {
    Write-Host "[ERROR] Hadoop directory not found:"
    Write-Host $HADOOP_HOME_PATH
    exit 1
}

Write-Host "[OK] Hadoop"
Write-Host "     $HADOOP_HOME_PATH"


# ------------------------------------------------------------
# 6. Check winutils
# ------------------------------------------------------------

if (-not (Test-Path $WINUTILS)) {
    Write-Host "[ERROR] winutils.exe not found:"
    Write-Host $WINUTILS
    exit 1
}

Write-Host "[OK] winutils.exe"
Write-Host "     $WINUTILS"


# ------------------------------------------------------------
# 7. Check hive-site.xml
# ------------------------------------------------------------

if (-not (Test-Path $HIVE_SITE)) {
    Write-Host "[ERROR] hive-site.xml not found:"
    Write-Host $HIVE_SITE
    exit 1
}

Write-Host "[OK] hive-site.xml"
Write-Host "     $HIVE_SITE"


# ------------------------------------------------------------
# 8. Check winutils execution
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking winutils..."

if (Test-Path $WINUTILS) {
    Write-Host "[OK] winutils.exe exists and is ready."
}
else {
    Write-Host "[ERROR] winutils.exe cannot be found."
    exit 1
}

# ------------------------------------------------------------
# 9. Check PySpark version
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking PySpark..."

& $PYTHON_EXE -c "import pyspark; print('PySpark =', pyspark.__version__)"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] PySpark check failed."
    exit 1
}


# ------------------------------------------------------------
# 10. Check Hadoop client version
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking Hadoop client..."

& $PYTHON_EXE -c "from pyspark.sql import SparkSession; spark=SparkSession.builder.master('local[2]').appName('env-check').getOrCreate(); print('Hadoop =', spark._jvm.org.apache.hadoop.util.VersionInfo.getVersion()); spark.stop()"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Hadoop client check failed."
    exit 1
}


# ------------------------------------------------------------
# 11. Check Hive Metastore configuration
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking Hive Metastore configuration..."

$HiveSiteContent = Get-Content $HIVE_SITE -Raw

if ($HiveSiteContent -match "thrift://192\.168\.214\.129:9083") {
    Write-Host "[OK] Hive Metastore URI"
    Write-Host "     thrift://192.168.214.129:9083"
}
else {
    Write-Host "[WARN] Expected Hive Metastore URI was not found."
}


# ------------------------------------------------------------
# 12. Display environment
# ------------------------------------------------------------

Write-Host ""
Write-Host "---------------- Environment ----------------"

Write-Host "HADOOP_HOME     = $env:HADOOP_HOME"
Write-Host "SPARK_CONF_DIR  = $env:SPARK_CONF_DIR"
Write-Host "PYSPARK_PYTHON  = $env:PYSPARK_PYTHON"


# ------------------------------------------------------------
# 13. Finished
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================================"
Write-Host " Spark environment is ready."
Write-Host "============================================================"
Write-Host ""

Write-Host "Python:"
Write-Host "  $PYTHON_EXE"

Write-Host ""
Write-Host "You can now run your Spark program."
Write-Host ""