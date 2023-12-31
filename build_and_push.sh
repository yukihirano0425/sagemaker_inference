#!/bin/zsh

REPOSITORY_NAME="sagemaker-sample-endpoint"

# IAM認証情報に紐付くアカウント番号を取得
echo Get the account number associated with the current IAM credentials
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
if [ $? -ne 0 ]
then
    exit 255
fi

REGION=$(aws configure get region)

# ECRへプッシュする名称を生成
TAG="${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/sagemaker-sample-endpoint:latest"

# リポジトリがECRに存在しない場合、新規作成
echo If the repository doesnt exist in ECR, create it
aws ecr describe-repositories --repository-names sagemaker-sample-endpoint > /dev/null 2>&1
if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name sagemaker-sample-endpoint > /dev/null
fi

echo login
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com

echo docker build
docker buildx build --platform=linux/amd64 -t sagemaker-sample-endpoint -f Dockerfile .

echo docker tag ${REPOSITORY_NAME} ${TAG}
docker tag ${REPOSITORY_NAME} ${TAG}

docker push ${TAG}
