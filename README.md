# 🍻 飲み会ゲームアプリ

Streamlit + Supabaseで作成したリアルタイム投票型飲み会ゲームです。

## 🎮 機能
- **お題入力**: ホストがお題を設定
- **リアルタイム投票**: 参加者がYES/NOで投票
- **結果表示**: YESの人数を即座に表示
- **ゲーム進行**: 連続してお題を楽しめる

## 🚀 デプロイ

### Streamlit Cloudでのデプロイ
1. [Streamlit Cloud](https://streamlit.io/cloud)にアクセス
2. GitHubリポジトリを連携
3. `main.py`を指定してデプロイ
4. 環境変数を設定：
   - `SUPABASE_URL`: あなたのSupabaseプロジェクトURL
   - `SUPABASE_KEY`: SupabaseのANON公開キー

### Supabaseセットアップ
1. [Supabase](https://supabase.com)でプロジェクト作成
2. SQL Editorで`database_setup.sql`を実行
3. Settings > APIから接続情報を取得

## 🛠️ ローカル開発
```bash
pip install -r requirements.txt
streamlit run main.py
```

## 🎯 使い方
1. お題を入力して「ゲーム開始」
2. 参加者がYES/NOボタンで投票
3. 「ゲーム終了」で結果発表
4. 「次のお題へ」で新しいゲーム開始

## データベース構造
- `polls`: 投票の質問と状態を管理
- `votes`: 各投票の結果を記録

リアルタイムで複数人が同時投票可能です！