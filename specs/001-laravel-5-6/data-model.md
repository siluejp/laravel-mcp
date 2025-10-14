# データモデル: Laravel 5.6 コーディング支援AIエージェント

このドキュメントは、アプリケーションで使用されるエンティティのデータモデルを概説します。データはSQLiteデータベースに保存されます。

## 1. Conversation (会話)

単一の会話ターン（問い合わせとその応答）を表します。

- **`id`**: `INTEGER` (主キー) - 会話レコードの一意の識別子。
- **`session_id`**: `TEXT` - 複数のターンをグループ化するためのユーザーセッションの識別子。
- **`user_id`**: `TEXT` - ユーザーの識別子。
- **`query_text`**: `TEXT` - ユーザーの元のテキスト問い合わせ。
- **`query_timestamp`**: `DATETIME` - ユーザーが問い合わせを送信した日時。
- **`response_text`**: `TEXT` - エージェントのテキスト応答。
- **`response_timestamp`**: `DATETIME` - エージェントが応答を送信した日時。
- **`source_references`**: `TEXT` (JSON) - RAG応答のために使用されたドキュメントURLのリスト。