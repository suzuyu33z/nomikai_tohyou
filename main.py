import streamlit as st
from supabase import create_client, Client
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="飲み会ゲーム",
    page_icon="🍻",
    layout="centered"
)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabaseの設定が必要です。環境変数SUPABASE_URLとSUPABASE_KEYを設定してください。")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_new_poll(question: str):
    try:
        result = supabase.table("polls").insert({
            "question": question,
            "is_active": True
        }).execute()
        return result.data[0]['id'] if result.data else None
    except Exception as e:
        st.error(f"お題の作成に失敗しました: {e}")
        return None

def vote(poll_id: int, vote_value: bool):
    try:
        supabase.table("votes").insert({
            "poll_id": poll_id,
            "vote": vote_value
        }).execute()
        return True
    except Exception as e:
        st.error(f"投票に失敗しました: {e}")
        return False

def get_poll_results(poll_id: int):
    try:
        result = supabase.table("votes").select("vote").eq("poll_id", poll_id).execute()
        if result.data:
            yes_count = sum(1 for vote in result.data if vote["vote"])
            total_count = len(result.data)
            return yes_count, total_count
        return 0, 0
    except Exception as e:
        st.error(f"結果の取得に失敗しました: {e}")
        return 0, 0

def get_active_poll():
    try:
        result = supabase.table("polls").select("*").eq("is_active", True).order("created_at", desc=True).limit(1).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"アクティブなお題の取得に失敗しました: {e}")
        return None

def close_poll(poll_id: int):
    try:
        supabase.table("polls").update({"is_active": False}).eq("id", poll_id).execute()
        return True
    except Exception as e:
        st.error(f"ゲーム終了に失敗しました: {e}")
        return False

# ゲームの状態管理
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'input'  # 'input', 'voting', 'results'

st.title("🍻 飲み会ゲーム")

# ゲーム状態に応じた画面表示
if st.session_state.game_state == 'input':
    # お題入力画面
    st.header("お題を入力してください")
    
    # アクティブなゲームがあるかチェック
    active_poll = get_active_poll()
    if active_poll:
        st.warning("既にゲームが進行中です！")
        if st.button("進行中のゲームに参加"):
            st.session_state.game_state = 'voting'
            st.rerun()
    else:
        question = st.text_input("お題", placeholder="例: カラオケが好きな人！")
        
        if st.button("ゲーム開始", type="primary", disabled=not question):
            if question:
                poll_id = create_new_poll(question)
                if poll_id:
                    st.session_state.current_poll_id = poll_id
                    st.session_state.game_state = 'voting'
                    st.success(f"ゲーム開始！お題: {question}")
                    st.rerun()

elif st.session_state.game_state == 'voting':
    # 投票画面
    active_poll = get_active_poll()
    
    if active_poll:
        st.header("🎯 投票中")
        st.subheader(f"お題: {active_poll['question']}")
        
        # 投票済みチェック用のセッション状態
        poll_vote_key = f"voted_poll_{active_poll['id']}"
        
        if poll_vote_key in st.session_state:
            # 既に投票済み
            st.success("✅ 投票済みです！結果発表をお待ちください。")
            st.info("お題の結果は「ゲーム終了」後に発表されます。")
        else:
            # まだ投票していない
            st.info("あなたの回答をお選びください")
            
            # 投票ボタン
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ YES", type="primary", use_container_width=True):
                    if vote(active_poll['id'], True):
                        st.session_state[poll_vote_key] = True  # 投票済みマーク
                        st.success("投票完了！")
                        st.rerun()
            
            with col2:
                if st.button("❌ NO", use_container_width=True):
                    if vote(active_poll['id'], False):
                        st.session_state[poll_vote_key] = False  # 投票済みマーク
                        st.success("投票完了！")
                        st.rerun()
        
        st.markdown("---")
        
        # 終了ボタン（ホスト用）
        if st.button("🏁 ゲーム終了", type="secondary"):
            st.session_state.game_state = 'results'
            st.rerun()

elif st.session_state.game_state == 'results':
    # 結果画面
    active_poll = get_active_poll()
    
    if active_poll:
        st.header("🎉 結果発表！")
        st.subheader(f"お題: {active_poll['question']}")
        
        yes_count, total_count = get_poll_results(active_poll['id'])
        
        # 結果表示（ここで初めて人数が見える）
        st.markdown(f"""
        ## 🎉 結果発表！
        
        ### 🎯 **YESを選んだ人: {yes_count}人**
        ### 📊 総投票数: {total_count}人
        ### 📈 YES率: {yes_count/total_count*100:.1f}%
        """)
        
        if yes_count > 0:
            st.balloons()
            st.success(f"🎊 YESを選んだ人は **{yes_count}人** でした！")
        else:
            st.info("🤔 YESを選んだ人はいませんでした。")
        
        # 進行ボタン
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 次のお題へ", type="primary"):
                # 現在のゲームを終了
                close_poll(active_poll['id'])
                # 新しいゲームへ
                st.session_state.game_state = 'input'
                if 'current_poll_id' in st.session_state:
                    del st.session_state.current_poll_id
                st.rerun()
        
        with col2:
            if st.button("🏠 ホームに戻る"):
                close_poll(active_poll['id'])
                st.session_state.game_state = 'input'
                if 'current_poll_id' in st.session_state:
                    del st.session_state.current_poll_id
                st.rerun()

# リセットボタン（デバッグ用）
if st.sidebar.button("🔄 ゲームをリセット"):
    active_poll = get_active_poll()
    if active_poll:
        close_poll(active_poll['id'])
    st.session_state.game_state = 'input'
    if 'current_poll_id' in st.session_state:
        del st.session_state.current_poll_id
    st.rerun()

st.markdown("---")
st.markdown("*🍻 飲み会で盛り上がろう！*")