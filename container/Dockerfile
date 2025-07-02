# Python Verison: 3.11
# python 3.11-slim-bullseye for linux/amd64
FROM python@sha256:aad3c9cb248194ddd1b98860c2bf41ea7239c384ed51829cf38dcb3569deb7f1

COPY pip.conf /etc/pip.conf

# appディレクトリを作成
WORKDIR /app

 
# 必要なPythonライブラリのインストール
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt


# プログラムや設定ファイルなどをコピーする
COPY main.py /app
COPY empty_metadata.json /app
COPY modules/ /app/modules/
COPY eln/ /app/eln/
