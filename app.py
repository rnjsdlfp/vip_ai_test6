import streamlit as st
import openai

# 사이드바에서 OpenAI API 키와 Assistant ID 입력받기
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    assistant_id = st.text_input("Assistant ID", key="assistant_id")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

st.title("💬 VIP AI")
st.caption("🚀 A Streamlit chatbot powered by OpenAI & Jireh")

# Function to create system message based on assistant ID
def create_system_message(assistant_id):
    return {"role": "system", "content": f"You are an assistant with ID {assistant_id}. Your role is to help the user effectively and provide accurate information."}

# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# 기존 메시지 출력
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div style="text-align: right;">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;">{msg["content"]}</div>', unsafe_allow_html=True)

# 사용자 입력 처리
prompt = st.text_input("User Input", key="user_input")
if prompt:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if not assistant_id:
        st.info("Please add the Assistant ID to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div style="text-align: right;">{prompt}</div>', unsafe_allow_html=True)

    try:
        # Add the assistant's ID message at the beginning of each call
        messages = [create_system_message(assistant_id)] + st.session_state.messages[1:]
        
        # 최신 API 호출을 위한 코드
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # 사용 가능한 모델로 변경
            messages=messages
            #messages=st.session_state["messages"]
        )
        msg = response.choices[0].message['content']
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.markdown(f'<div style="text-align: left;">{msg}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")
