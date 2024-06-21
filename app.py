import streamlit as st
import openai 
import uuid
import time

client = openai()

# 사이드바에서 OpenAI API 키와 Assistant ID 입력받기
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    assistant_id = st.text_input("Assistant ID", key="assistant_id", value="asst_Dlr6YRJen7llwFxT393E5noC")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    # 스레드 선택 드롭다운 및 새 스레드 생성 버튼
    if "threads" not in st.session_state:
        st.session_state["threads"] = {}
    selected_thread = st.selectbox("Select Thread", options=["새로운 스레드 생성"] + list(st.session_state["threads"].keys()))

    if selected_thread == "새로운 스레드 생성":
        if st.button("Create New Thread"):
            new_thread_id = str(uuid.uuid4())
            st.session_state["threads"][new_thread_id] = []
            selected_thread = new_thread_id
            st.success(f"New thread created with ID: {new_thread_id}")

st.title("💬 VIP AI")
st.caption("🚀 A Streamlit chatbot powered by OpenAI & Jireh")

# Function to create system message based on assistant ID
def create_system_message(assistant_id):
    return {"role": "system", "content": f"You are an assistant with ID {assistant_id}. Your role is to help the user effectively and provide accurate information."}

# Check if a thread is selected and initialize messages if not already present
if selected_thread:
    if selected_thread not in st.session_state["threads"]:
        st.session_state["threads"][selected_thread] = [create_system_message(assistant_id)]
    messages = st.session_state["threads"][selected_thread]
else:
    st.info("Please select or create a thread to continue.")
    st.stop()

# Display existing messages for the current thread
for msg in messages:
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
    messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div style="text-align: right;">{prompt}</div>', unsafe_allow_html=True)

    try:
    
        run = client.beta.threads.runs.create(
            thread_id=selected_thread,
            assistant_id=assistant_id
            )
    
        run_id = run.id
    
        while true:
            run = client.beta.threads.runs.retrieve(
                thread_id=selected_thread,
                run_id=run_id
                )
    
            if run.status == "completed":
                break
            else:
                time.sleep(2)
            print(run)
    
        thread_messages = client.beta.threads.messages.list(thread_id)
    
        msg = thread_messages.data[0].content[0].text.value
        print(msg)
       
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_mnessage("assistant").write(msg)

    except Exception as e:
        st.error(f"Error: {e}")
        
        # Update the session state with the new messages
        #st.session_state["threads"][selected_thread] = messages
