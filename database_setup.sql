-- Supabaseで実行するSQL文

-- 投票テーブル
CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- 投票データテーブル
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls(id) ON DELETE CASCADE,
    vote BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- インデックス追加（パフォーマンス向上）
CREATE INDEX idx_polls_active ON polls(is_active, created_at DESC);
CREATE INDEX idx_votes_poll_id ON votes(poll_id);

-- Row Level Security (RLS) を有効化
ALTER TABLE polls ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;

-- 全ユーザーがテーブルを読み書きできるポリシー
CREATE POLICY "Public Access" ON polls FOR ALL USING (true);
CREATE POLICY "Public Access" ON votes FOR ALL USING (true);