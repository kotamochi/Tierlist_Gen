# Pythonランタイムを親イメージとして使用
FROM python:3.11-alpine

# 作業ディレクトリを設定
WORKDIR /app

# 現在のディレクトリの内容をコンテナ内の/appにコピー
COPY . /app

# requirements.txtで指定された必要なパッケージをインストール
RUN pip install -r requirements.txt

# コンテナ起動時にapp.pyを実行
CMD ["python", "app.py"]