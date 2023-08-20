from datetime import datetime

from boto3.session import Session

# SageMakerクライアント作成
client = Session().client("sagemaker", region_name="ap-northeast-1")

# トレーニングジョブ名
training_job_name = "sagemaker-sample-" + datetime.now().strftime("%Y%m%d-%H%M%S")
# 入力ファイルパス
input_s3uri = "s3://sagemaker-inference-data-input/" + "sample.mp4"
# 出力パス
output_s3uri = "s3://sagemaker-inference-data-output/"


def create_training_job() -> dict:
    # トレーニングパラメータ
    training_params = {
        # トレーニングのジョブ名
        "TrainingJobName": training_job_name,
        # ハイパーパラメータ
        "HyperParameters": {
            "max_save_frames": "10",
        },
        # Dockerイメージ
        "AlgorithmSpecification": {
            "TrainingImage": "013267072576.dkr.ecr.ap-northeast-1.amazonaws.com/sagemaker-sample-endpoint:latest",
            "TrainingInputMode": "File",
        },
        # SageMakerにアタッチするロール
        "RoleArn": "arn:aws:iam::013267072576:role/sagemaker-role",
        # 入力チャネル
        "InputDataConfig": [
            # 動画格納パス
            {
                "ChannelName": "movie",
                "DataSource": {
                    "S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": input_s3uri}
                },
            }
        ],
        # 出力パス
        "OutputDataConfig": {"S3OutputPath": output_s3uri},
        # 学習インスタンス指定
        "ResourceConfig": {
            "InstanceType": "ml.m4.xlarge",
            "InstanceCount": 1,
            "VolumeSizeInGB": 10,
        },
        # タイムアウト時間指定
        "StoppingCondition": {"MaxRuntimeInSeconds": 60 * 60},
    }

    # トレーニングジョブ発行
    response = client.create_training_job(**training_params)
    print(response)


if __name__ == "__main__":
    create_training_job()
