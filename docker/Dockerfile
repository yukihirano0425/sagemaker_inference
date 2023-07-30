FROM python:3.9-slim

ENV PROGRAM_DIR=/opt/program
WORKDIR $PROGRAM_DIR

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
        wget \
        python3-pip \
        python3-setuptools \
        nginx \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# python実行パス シンボリックリンク指定
RUN ln -s /usr/bin/python3 /usr/bin/python

# pipパッケージ インストール
COPY docker/requirements.txt $PROGRAM_DIR/requirements.txt
RUN pip3 install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt

# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED=TRUE
# .pyc を生成しない
ENV PYTHONDONTWRITEBYTECODE=TRUE
# パス指定
ENV PATH="/opt/program:${PATH}"
ENV MODEL_PATH=/opt/ml/model

COPY docker/src /opt/program
RUN chmod +x /opt/program/serve