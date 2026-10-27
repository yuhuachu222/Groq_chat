
import streamlit as st
from groq import Groq

# 初始化 Groq 客戶端
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 使用 Groq API 呼叫 GPT-OSS 模型
def call_llama_model(messages):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0,
            max_completion_tokens=1024,
            top_p=0.5,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error("Groq API 呼叫失敗，請檢查金鑰、模型及使用額度。")
        return None

# Streamlit App
st.title("整合 Streamlit 與 Groq API")
st.write("這是一個基於 Groq API 和 GPT-OSS 模型的聊天介面。")

# 初始化聊天記錄
if "messages" not in st.session_state:
    st.session_state.messages = []

# 建立新聊天
if st.button("新聊天"):
    st.session_state.messages = []
    st.rerun()

# 顯示聊天記錄
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天輸入框
user_input = st.chat_input("請輸入您的訊息")

if user_input:
    user_message = {"role": "user", "content": user_input}
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(user_input)

    messages_to_send = [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        with st.spinner("AI 正在思考中..."):
            ai_response = call_llama_model(messages_to_send)

        if ai_response:
            st.markdown(ai_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response
            })
