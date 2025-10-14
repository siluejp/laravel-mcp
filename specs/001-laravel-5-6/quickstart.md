# クイックスタート: Laravel 5.6コーディング支援AIエージェント

このガイドは、Dockerを使用してMCPサーバーをローカルで実行する方法を説明します。

## 前提条件

- Docker
- LLMのAPIキー（環境変数経由で設定）

## サーバーの実行

1.  **Dockerイメージのビルド:**
    ```bash
    docker build -t mcp-server .
    ```

2.  **Dockerコンテナの実行:**
    LLMプロバイダーに必要な環境変数を設定します。
    ```bash
    docker run -d -p 8000:8000 \
      -e LLM_API_KEY='your-api-key' \
      --name mcp-server \
      mcp-server
    ```
    サーバーは `http://localhost:8000` で利用可能になります。

## エージェントとの対話

サーバーは、Model Context Protocolを介して `laravel_5_6_assistant` ツールを公開します。クライアントは、MCP仕様に準拠したリクエストを送信することで対話できます。

**クライアント対話の例（コンセプト）:**

```python
import mcp_client

# サーバーに接続
client = mcp_client.connect("http://localhost:8000")

# Laravelアシスタントツールを使用
response = client.use_tool(
    "laravel_5_6_assistant",
    {"query": "Laravel 5.6でミドルウェアを作成する方法は？"}
)

print(response["response"])
# 出力例:
# ミドルウェアを作成するには、artisanコマンドを使用します...
# `php artisan make:middleware MyMiddleware`
# ...
```