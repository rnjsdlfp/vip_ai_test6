import openai
import streamlit as st
import uuid
import time

# 사이드바에서 OpenAI API 키와 Assistant ID 입력받기
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    assistant_id = st.text_input("Assistant ID", key="assistant_id", value="asst_Dlr6YRJen7llwFxT393E5noC")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    
    # OpenAI 클라이언트 초기화
    if openai_api_key:
        client = openai.Client(api_key=openai_api_key)
    else:
        client = None
    
    # 스레드 선택 드롭다운 및 새 스레드 생성 버튼
    if "threads" not in st.session_state:
        st.session_state["threads"] = {}
    
    selected_thread = st.selectbox("Select Thread", options=["새로운 스레드 생성"] + list(st.session_state["threads"].keys()))
    
    if selected_thread == "새로운 스레드 생성":
        if st.button("Create New Thread"):
            if client:
                new_thread = client.beta.threads.create()
                new_thread_id = new_thread.id
                st.session_state["threads"][new_thread_id] = []
                selected_thread = new_thread_id
                st.success(f"New thread created with ID: {new_thread_id}")
            else:
                st.error("OpenAI API key is required to create a new thread.")

st.title("💬 VIP AI")
st.caption("🚀 A Streamlit chatbot powered by OpenAI & Jireh")

# Check if a thread is selected
if not selected_thread or selected_thread == "새로운 스레드 생성":
    st.info("Please select or create a thread to continue.")
    st.stop()

# Check if OpenAI client is initialized
if not client:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# Display existing messages for the current thread
messages = st.session_state["threads"].get(selected_thread, [])
for msg in messages:
    if msg["role"] == "user":
        st.markdown(f'<div style="text-align: right;">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;">{msg["content"]}</div>', unsafe_allow_html=True)

# 사용자 입력 처리
prompt = st.text_input("User Input", key="user_input")
if prompt:
    if not assistant_id:
        st.info("Please add the Assistant ID to continue.")
        st.stop()
    
    messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div style="text-align: right;">{prompt}</div>', unsafe_allow_html=True)
    
    try:
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=selected_thread,
            role="user",
            content=prompt
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=selected_thread,
            assistant_id=assistant_id
        )
        
        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=selected_thread, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(1)
        
        # Retrieve the latest messages
        thread_messages = client.beta.threads.messages.list(thread_id=selected_thread)
        
        # Get the latest assistant message
        assistant_messages = [msg for msg in thread_messages if msg.role == "assistant"]
        if assistant_messages:
            latest_message = assistant_messages[0].content[0].text.value
            messages.append({"role": "assistant", "content": latest_message})
            st.markdown(f'<div style="text-align: left;">{latest_message}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {e}")
    
    # Update the session state with the new messages
    st.session_state["threads"][selected_thread] = messages
