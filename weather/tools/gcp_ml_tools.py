"""
GCP ML Tools
============

Google Cloud Platform 機器學習工具，用於 Vertex AI 和 BigQuery ML。

使用前需設定:
    - GOOGLE_CLOUD_PROJECT 環境變數
    - 或 gcloud auth application-default login
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# GCP 依賴
try:
    from google.cloud import storage
    from google.cloud import bigquery
    HAS_GCP = True
except ImportError:
    HAS_GCP = False
    print("警告: google-cloud 套件未安裝，GCP 功能不可用")

try:
    from google.cloud import aiplatform
    HAS_VERTEX = True
except ImportError:
    HAS_VERTEX = False
    print("警告: google-cloud-aiplatform 未安裝，Vertex AI 功能不可用")


# 設定
GCP_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT', '')
GCP_LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')


def check_gcp_credentials() -> Dict[str, bool]:
    """
    檢查 GCP 認證狀態

    Returns:
        dict: 認證狀態
    """
    status = {
        "has_project": bool(GCP_PROJECT),
        "has_gcp_libs": HAS_GCP,
        "has_vertex_libs": HAS_VERTEX,
        "authenticated": False,
    }

    if HAS_GCP:
        try:
            client = storage.Client()
            status["authenticated"] = True
        except Exception:
            pass

    return status


def upload_to_gcs(
    df: pd.DataFrame,
    bucket_name: str,
    blob_path: str,
    project: Optional[str] = None
) -> str:
    """
    上傳 DataFrame 到 Google Cloud Storage

    Args:
        df: 要上傳的 DataFrame
        bucket_name: GCS bucket 名稱
        blob_path: 檔案路徑 (不含 gs://)
        project: GCP 專案 ID

    Returns:
        str: GCS URI (gs://bucket/path)
    """
    if not HAS_GCP:
        raise ImportError("google-cloud-storage not installed")

    project = project or GCP_PROJECT
    client = storage.Client(project=project)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    # 轉換為 CSV 並上傳
    csv_data = df.to_csv(index=False)
    blob.upload_from_string(csv_data, content_type='text/csv')

    gcs_uri = f"gs://{bucket_name}/{blob_path}"
    print(f"已上傳至 {gcs_uri}")

    return gcs_uri


def download_from_gcs(
    bucket_name: str,
    blob_path: str,
    local_path: str,
    project: Optional[str] = None
) -> str:
    """
    從 GCS 下載檔案

    Args:
        bucket_name: GCS bucket 名稱
        blob_path: 檔案路徑
        local_path: 本地儲存路徑
        project: GCP 專案 ID

    Returns:
        str: 本地檔案路徑
    """
    if not HAS_GCP:
        raise ImportError("google-cloud-storage not installed")

    project = project or GCP_PROJECT
    client = storage.Client(project=project)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    blob.download_to_filename(local_path)

    print(f"已下載至 {local_path}")
    return local_path


def create_bqml_model(
    query: str,
    project: Optional[str] = None
) -> Dict[str, Any]:
    """
    使用 BigQuery ML 建立模型

    Args:
        query: CREATE MODEL SQL 語句
        project: GCP 專案 ID

    Returns:
        dict: 模型資訊
    """
    if not HAS_GCP:
        raise ImportError("google-cloud-bigquery not installed")

    project = project or GCP_PROJECT
    client = bigquery.Client(project=project)

    # 執行 CREATE MODEL
    job = client.query(query)
    job.result()  # 等待完成

    return {
        "status": "created",
        "job_id": job.job_id,
        "created_at": datetime.now().isoformat(),
    }


def evaluate_bqml_model(
    model_ref: str,
    project: Optional[str] = None
) -> Dict[str, float]:
    """
    評估 BigQuery ML 模型

    Args:
        model_ref: 模型參考 (project.dataset.model_name)
        project: GCP 專案 ID

    Returns:
        dict: 評估指標
    """
    if not HAS_GCP:
        raise ImportError("google-cloud-bigquery not installed")

    project = project or GCP_PROJECT
    client = bigquery.Client(project=project)

    query = f"SELECT * FROM ML.EVALUATE(MODEL `{model_ref}`)"
    result = client.query(query).result()

    metrics = {}
    for row in result:
        for key, value in row.items():
            metrics[key] = float(value) if value is not None else None

    return metrics


def predict_with_bqml(
    model_ref: str,
    data_query: str,
    project: Optional[str] = None
) -> pd.DataFrame:
    """
    使用 BigQuery ML 模型進行預測

    Args:
        model_ref: 模型參考
        data_query: 數據查詢 SQL
        project: GCP 專案 ID

    Returns:
        DataFrame: 預測結果
    """
    if not HAS_GCP:
        raise ImportError("google-cloud-bigquery not installed")

    project = project or GCP_PROJECT
    client = bigquery.Client(project=project)

    query = f"""
    SELECT *
    FROM ML.PREDICT(
        MODEL `{model_ref}`,
        ({data_query})
    )
    """

    result = client.query(query).result()
    return result.to_dataframe()


def train_automl_model(
    dataset_display_name: str,
    target_column: str,
    training_display_name: str,
    budget_milli_node_hours: int = 1000,
    project: Optional[str] = None,
    location: Optional[str] = None
) -> Dict[str, Any]:
    """
    訓練 Vertex AI AutoML 表格模型

    Args:
        dataset_display_name: 數據集名稱
        target_column: 目標欄位
        training_display_name: 訓練任務名稱
        budget_milli_node_hours: 訓練預算 (毫節點小時)
        project: GCP 專案 ID
        location: GCP 區域

    Returns:
        dict: 模型資訊
    """
    if not HAS_VERTEX:
        raise ImportError("google-cloud-aiplatform not installed")

    project = project or GCP_PROJECT
    location = location or GCP_LOCATION

    aiplatform.init(project=project, location=location)

    # 獲取數據集
    datasets = aiplatform.TabularDataset.list(
        filter=f'display_name="{dataset_display_name}"'
    )

    if not datasets:
        raise ValueError(f"找不到數據集: {dataset_display_name}")

    dataset = datasets[0]

    # 建立訓練任務
    job = aiplatform.AutoMLTabularTrainingJob(
        display_name=training_display_name,
        optimization_prediction_type="regression",
        optimization_objective="minimize-rmse"
    )

    # 執行訓練
    model = job.run(
        dataset=dataset,
        target_column=target_column,
        training_fraction_split=0.8,
        validation_fraction_split=0.1,
        test_fraction_split=0.1,
        budget_milli_node_hours=budget_milli_node_hours,
    )

    return {
        "status": "trained",
        "model_id": model.resource_name,
        "display_name": model.display_name,
        "trained_at": datetime.now().isoformat(),
    }


def predict_with_automl(
    model_id: str,
    instances: List[Dict],
    project: Optional[str] = None,
    location: Optional[str] = None
) -> List[Dict]:
    """
    使用 Vertex AI 模型進行預測

    Args:
        model_id: 模型 ID
        instances: 預測數據
        project: GCP 專案 ID
        location: GCP 區域

    Returns:
        list: 預測結果
    """
    if not HAS_VERTEX:
        raise ImportError("google-cloud-aiplatform not installed")

    project = project or GCP_PROJECT
    location = location or GCP_LOCATION

    aiplatform.init(project=project, location=location)

    model = aiplatform.Model(model_id)
    predictions = model.predict(instances)

    return predictions.predictions


def create_bq_dataset(
    dataset_id: str,
    project: Optional[str] = None
) -> str:
    """
    建立 BigQuery 數據集

    Args:
        dataset_id: 數據集 ID
        project: GCP 專案 ID

    Returns:
        str: 完整數據集參考
    """
    if not HAS_GCP:
        raise ImportError("google-cloud-bigquery not installed")

    project = project or GCP_PROJECT
    client = bigquery.Client(project=project)

    dataset_ref = f"{project}.{dataset_id}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"

    try:
        client.create_dataset(dataset)
        print(f"已建立數據集: {dataset_ref}")
    except Exception as e:
        if "Already Exists" in str(e):
            print(f"數據集已存在: {dataset_ref}")
        else:
            raise

    return dataset_ref


def load_df_to_bq(
    df: pd.DataFrame,
    table_ref: str,
    project: Optional[str] = None,
    if_exists: str = 'replace'
) -> int:
    """
    將 DataFrame 載入 BigQuery

    Args:
        df: 要載入的 DataFrame
        table_ref: 表格參考 (project.dataset.table)
        project: GCP 專案 ID
        if_exists: 'replace' 或 'append'

    Returns:
        int: 載入的記錄數
    """
    if not HAS_GCP:
        raise ImportError("google-cloud-bigquery not installed")

    project = project or GCP_PROJECT
    client = bigquery.Client(project=project)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE if if_exists == 'replace'
                          else bigquery.WriteDisposition.WRITE_APPEND
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # 等待完成

    print(f"已載入 {len(df)} 筆記錄至 {table_ref}")
    return len(df)


def get_gcp_cost_estimate(
    training_hours: float,
    prediction_rows: int,
    storage_gb: float
) -> Dict[str, float]:
    """
    估算 GCP ML 成本

    Args:
        training_hours: 訓練時數
        prediction_rows: 預測記錄數
        storage_gb: 儲存空間 (GB)

    Returns:
        dict: 成本估算
    """
    # 價格參考 (2024 年)
    VERTEX_TRAINING_PER_HOUR = 20.0  # AutoML Tables
    VERTEX_PREDICTION_PER_1000 = 0.05
    BQ_STORAGE_PER_GB = 0.02
    BQ_QUERY_PER_TB = 5.0

    training_cost = training_hours * VERTEX_TRAINING_PER_HOUR
    prediction_cost = (prediction_rows / 1000) * VERTEX_PREDICTION_PER_1000
    storage_cost = storage_gb * BQ_STORAGE_PER_GB

    return {
        "training": training_cost,
        "prediction": prediction_cost,
        "storage": storage_cost,
        "total": training_cost + prediction_cost + storage_cost,
        "currency": "USD",
        "note": "估算值，實際費用可能不同",
    }


def generate_bqml_create_model_sql(
    model_name: str,
    table_ref: str,
    target_column: str,
    model_type: str = 'BOOSTED_TREE_REGRESSOR',
    options: Optional[Dict] = None
) -> str:
    """
    生成 BigQuery ML CREATE MODEL SQL

    Args:
        model_name: 模型名稱
        table_ref: 訓練數據表格
        target_column: 目標欄位
        model_type: 模型類型
        options: 額外選項

    Returns:
        str: SQL 語句
    """
    default_options = {
        'data_split_method': 'AUTO_SPLIT',
        'num_parallel_tree': 8,
        'max_iterations': 50,
    }

    if options:
        default_options.update(options)

    options_str = ",\n  ".join(f"{k}={repr(v) if isinstance(v, str) else v}"
                               for k, v in default_options.items())

    sql = f"""
CREATE OR REPLACE MODEL `{model_name}`
OPTIONS(
  model_type='{model_type}',
  input_label_cols=['{target_column}'],
  {options_str}
) AS
SELECT *
FROM `{table_ref}`
WHERE {target_column} IS NOT NULL
"""

    return sql.strip()


if __name__ == "__main__":
    print("測試 GCP ML Tools...")

    # 檢查認證狀態
    status = check_gcp_credentials()
    print(f"認證狀態: {json.dumps(status, indent=2)}")

    # 成本估算範例
    cost = get_gcp_cost_estimate(
        training_hours=2,
        prediction_rows=1000,
        storage_gb=1
    )
    print(f"成本估算: ${cost['total']:.2f}")

    print("GCP ML Tools 載入成功")
