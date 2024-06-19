import streamlit as st
import openai

# 사이드바에서 OpenAI API 키와 Assistant ID 입력받기
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    assistant_id = st.text_input("Assistant ID", key="assistant_id")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 VIP AI")
st.caption("🚀 A Streamlit chatbot powered by OpenAI & Jireh")

# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# 기존 메시지 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not assistant_id:
        st.info("Please add the Assistant ID to continue.")
        st.stop()

    openai.api_key = openai_api_key

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # 최신 API 호출을 위한 코드
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # 사용 가능한 모델로 변경
            messages=st.session_state["messages"],
            user=assistant_id  # Assistant ID 사용
        )
        msg = response.choices[0].message['content']
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.error(f"Error: {e}")
