# MCP Supabaseサーバーの設定方法

MCPを使用してSupabaseと連携する場合の設定方法です。

## 1. MCP Supabaseサーバーのインストール

```bash
# NPXを使用してSupabase MCPサーバーをインストール
npx @modelcontextprotocol/server-supabase
```

## 2. Claude Desktopの設定

`~/.claude_desktop_config.json`にSupabase MCPサーバーを追加：

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-supabase"
      ],
      "env": {
        "SUPABASE_URL": "your_supabase_project_url",
        "SUPABASE_SERVICE_ROLE_KEY": "your_supabase_service_role_key"
      }
    }
  }
}
```

## 3. 必要な環境変数

- `SUPABASE_URL`: SupabaseプロジェクトのURL
- `SUPABASE_SERVICE_ROLE_KEY`: Supabaseのサービスロールキー（管理者権限）

## 4. MCPサーバーで利用可能な機能

MCP Supabaseサーバーを使用すると以下の操作が可能になります：

- **データベース操作**: テーブルの作成、読み取り、更新、削除
- **認証**: ユーザー管理と認証
- **ストレージ**: ファイルのアップロードと管理
- **Edge Functions**: サーバーレス関数の実行

## 5. MCPを使った投票アプリの利点

- Claudeが直接Supabaseを操作可能
- 複雑なSQL文の自動生成
- エラーハンドリングの簡素化
- リアルタイムデータベース操作

## 注意点

- Service Role Keyは強力な権限を持つため、安全に管理してください
- 本番環境では適切なRow Level Security (RLS)を設定してください