# クイックスタート: Laravel 5.6 コーディング支援AIエージェント

このガイドは、プロジェクトをセットアップし、ローカルで実行する方法を説明します。

## 1. 前提条件

- Python 3.11+
- `uv` パッケージインストーラ
- Docker (オプションですが推奨)
- OpenAI APIキー

## 2. セットアップ

1.  **依存関係のインストール:**
    `uv` を使って、必要なPythonパッケージをインストールします。
    ```bash
    uv pip install -r requirements.txt
    ```

2.  **環境変数の設定:**
    プロジェクトのルートに `.env` という名前のファイルを作成し、OpenAI APIキーを設定します。
    ```
    OPENAI_API_KEY="your-openai-api-key"
    ```
    このファイルは `.gitignore` に記載されているため、Gitリポジトリには含まれません。

3.  **RAGナレッジベースの作成:**
    AIエージェントが使用するベクトルストアを作成します。このコマンドはLaravelのドキュメントをダウンロードし、処理するため、初回は時間がかかります。
    ```bash
    uv run python scripts/ingest_docs.py
    ```
    これにより、プロジェクトルートに `faiss_index` ディレクトリが作成されます。

## 3. サーバーの実行

### ローカルでの直接実行

開発中は、`uvicorn` を使って直接サーバーを起動できます。
```bash
uv run uvicorn src.main:asgi_app --reload
```
サーバーは `http://localhost:8000` で利用可能になります。

### Dockerを使用する場合 (推奨)

1.  **Dockerイメージのビルド:**
    ```bash
    docker build -t mcp-server .
    ```

2.  **Dockerコンテナの実行:**
    `.env` ファイルから環境変数を読み込んでコンテナを起動します。
    ```bash
    docker run -d -p 8000:8000 --env-file .env --name mcp-server mcp-server
    ```

## 4. テストの実行

ユニットテストを実行して、すべてが正しく設定されていることを確認します。
```bash
uv run pytest
```

## 5. エージェントとの対話

サーバーは、Model Context Protocolを介して `/assistant/laravel_5_6_assistant` ツールを公開します。クライアントは、MCP仕様に準拠したリクエストを送信することで対話できます。

**クライアント対話の例（コンセプト）:**

```python
# この例はコンセプトを示すものであり、
# 実際のMCPクライアントライブラリの実装に依存します。
import mcp_client 

# サーバーに接続
client = mcp_client.connect("http://localhost:8000")

# Laravelアシスタントツールを使用
response = client.use_tool(
    "/assistant/laravel_5_6_assistant",
    {"query": "Laravel 5.6でミドルウェアを作成する方法は？"}
)

print(response["response"])
# 出力例:
# To create a middleware in Laravel 5.6, you can use the `make:middleware` Artisan command...
```
