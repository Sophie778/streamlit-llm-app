import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# LLMの初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 専門家の種類に応じたシステムメッセージを返す関数
def get_system_prompt(expert_type: str) -> str:
    if expert_type == "医療":
        return "あなたは優秀な医師です。医学的な知識に基づいて、正確で分かりやすい回答をしてください。"
    elif expert_type == "法律":
        return "あなたは経験豊富な弁護士です。法律に関する質問に対して、専門的かつ丁寧に回答してください。"
    elif expert_type == "栄養":
        return "あなたは管理栄養士です。食事や栄養に関する質問に、科学的根拠に基づいて答えてください。"
    else:
        return "あなたは知識豊富なアシスタントです。"

# 入力テキストと専門家の種類を受け取り、LLMの回答を返す関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    system_prompt = get_system_prompt(expert_type)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    result = llm(messages)
    return result.content

# Streamlit UI
st.set_page_config(page_title="専門家AIアシスタント", layout="centered")

st.title("🧠 専門家AIアシスタント")
st.markdown("""
このアプリでは、あなたの質問に対してAIが専門家として回答します。  
以下の手順で操作してください：

1. 専門家の種類を選択（医療・法律・栄養）
2. 質問を入力
3. 「送信」ボタンを押すと、AIが回答を表示します
""")

# ラジオボタンで専門家の種類を選択
expert_type = st.radio("専門家の種類を選んでください：", ["医療", "法律", "栄養"])

# 入力フォーム
user_input = st.text_area("質問を入力してください：", height=150)

# 送信ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが回答中..."):
            response = get_llm_response(user_input, expert_type)
            st.success("✅ 回答結果")
            st.write(response)