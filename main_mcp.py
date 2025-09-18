import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="投票アプリ (MCP版)",
    page_icon="🗳️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🗳️ 投票アプリ (MCP版)")

st.info("""
📋 **MCP (Model Context Protocol) 版の投票アプリです**

このバージョンでは、Claude CodeがMCP Supabaseサーバーを通じて
直接データベース操作を行います。

**セットアップが必要です:**
1. `MCP_SETUP.md` の手順に従ってMCP Supabaseサーバーを設定
2. Claude Desktop設定でSupabase MCPサーバーを有効化
""")

tab1, tab2, tab3 = st.tabs(["投票作成", "投票参加", "結果確認"])

with tab1:
    st.header("新しい投票を作成")
    
    question = st.text_input("質問を入力してください（例: 〇〇の人！）", placeholder="例: カラオケが好きな人！")
    
    if st.button("投票を開始", type="primary"):
        if question:
            st.success("質問を受け取りました！")
            st.info(f"作成する質問: {question}")
            st.markdown("""
            **Claude Codeに以下をお願いしてください:**
            
            ```
            MCP Supabaseサーバーを使って、以下の質問で新しい投票を作成してください：
            "{}"
            
            手順：
            1. pollsテーブルに新しいレコードを挿入
            2. 現在アクティブな投票があれば無効化
            3. 投票IDを返す
            ```
            """.format(question))
        else:
            st.error("質問を入力してください。")

with tab2:
    st.header("投票に参加")
    
    st.markdown("""
    **投票を行うには、Claude Codeに以下をお願いしてください:**
    
    **YESに投票する場合:**
    ```
    MCP Supabaseサーバーを使って、現在アクティブな投票にYESで投票してください
    ```
    
    **NOに投票する場合:**
    ```
    MCP Supabaseサーバーを使って、現在アクティブな投票にNOで投票してください
    ```
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("YES", type="primary", use_container_width=True):
            st.success("YESボタンが押されました！")
            st.info("Claude CodeにYES投票をお願いしてください")
    
    with col2:
        if st.button("NO", use_container_width=True):
            st.success("NOボタンが押されました！")
            st.info("Claude CodeにNO投票をお願いしてください")

with tab3:
    st.header("結果確認")
    
    if st.button("結果を表示", type="primary"):
        st.markdown("""
        **Claude Codeに以下をお願いしてください:**
        
        ```
        MCP Supabaseサーバーを使って、現在アクティブな投票の結果を集計して表示してください
        
        以下の情報を表示：
        1. 質問内容
        2. YESの投票数
        3. NOの投票数
        4. 総投票数
        5. YES率の円グラフまたは棒グラフ
        ```
        """)
    
    if st.button("投票を終了"):
        st.info("""
        **Claude Codeに以下をお願いしてください:**
        
        ```
        MCP Supabaseサーバーを使って、現在アクティブな投票を終了してください
        ```
        """)

st.markdown("---")

with st.expander("📊 現在の投票状況を確認"):
    if st.button("状況確認"):
        st.markdown("""
        **Claude Codeに以下をお願いしてください:**
        
        ```
        MCP Supabaseサーバーを使って、以下を確認してください：
        1. 現在アクティブな投票があるか
        2. あれば質問内容と現在の投票数
        3. なければ最新の投票結果
        ```
        """)

with st.expander("🔧 データベース管理"):
    if st.button("テーブル作成"):
        st.markdown("""
        **Claude Codeに以下をお願いしてください:**
        
        ```
        MCP Supabaseサーバーを使って、投票アプリ用のテーブルを作成してください：
        
        1. pollsテーブル (id, question, created_at, is_active)
        2. votesテーブル (id, poll_id, vote, created_at)
        3. 適切なインデックスとRLSポリシー
        ```
        """)
    
    if st.button("全投票履歴表示"):
        st.markdown("""
        **Claude Codeに以下をお願いしてください:**
        
        ```
        MCP Supabaseサーバーを使って、過去の全投票履歴を表示してください
        ```
        """)

st.markdown("*MCP版では、Claude Codeが直接Supabaseを操作します！*")