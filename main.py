import streamlit as st
from typing import Generator
from langchain_groq import ChatGroq
import os

from dotenv import load_dotenv, find_dotenv

# Load the API keys from .env
load_dotenv(find_dotenv(), override=True)


from src.agent import get_graph, stream_values

graph = get_graph()


def main():
    st.set_page_config(layout="wide", page_title="AI ChatBot")

    st.subheader("AI ChatBot", divider="grey", anchor=False)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your input here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        try:

            response = graph.stream(
                input={"messages": st.session_state.messages}, stream_mode="messages"
            )

            # Use the generator function with st.write_stream
            with st.chat_message("ai"):
                full_response = st.write_stream(stream_values(response))

        except Exception as e:
            st.error(e, icon="🚨")

        # Append the full response to session_state.messages
        if isinstance(full_response, str):
            st.session_state.messages.append({"role": "ai", "content": full_response})
        else:
            # Handle the case where full_response is not a string
            combined_response = "\n".join(str(item) for item in full_response)
            st.session_state.messages.append(
                {"role": "ai", "content": combined_response}
            )


if __name__ == "__main__":
    main()
