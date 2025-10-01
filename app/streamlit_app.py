import streamlit as st
from agent_dir.routing_agent import routing_agent
import asyncio

async def routing_agent_async(user_input):
    return await routing_agent(user_input)

def routing_agent_sync(user_input):
    try:
        # Try to get current running loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Already in event loop (Streamlit), run as task
        return asyncio.run_coroutine_threadsafe(
            routing_agent_async(user_input), loop
        ).result()
    else:
        # No running loop, safe to use asyncio.run
        return asyncio.run(routing_agent_async(user_input))


st.set_page_config(page_title="Domain Chatbot")
st.title("Domain Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = routing_agent_sync(user_input)
            st.session_state["messages"].append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
