import openai
import os
import streamlit as st
from htmlTemplates import css, bot_template, user_template
from dotenv import load_dotenv
load_dotenv()

# Set your OpenAI API key
OPENAI_API_KEY = st.secrets["openai"]["api_key"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)



def initialize_session_state():
    """Initialize session state variables"""
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    # if 'user_input' not in st.session_state:
    #     st.session_state['user_input'] = ''
def stream_response(response, placeholder):
    """Stream the response to the UI"""
    streamed_text = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            streamed_text += chunk.choices[0].delta.content
            placeholder.write(
                bot_template.replace("{{MSG}}", streamed_text),
                unsafe_allow_html=True
            )
    return streamed_text


def handle_chat_response(user_question: str, system_prompt:str, bot_placeholder, temperature, model_name):
    """Process chat responses based on file type"""
    try:
        temperature = float(temperature)
        temperature = max(0.0, min(1.0, temperature))
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
            # ,{
            #     "role": "user",
            #     "content": user_question
            # }
        ]
        # Append the history to the messages
        for chat in st.session_state.conversation_history:
            messages.append({"role": "user", "content": chat["user_message"]})
            messages.append({"role": "assistant", "content": chat["bot_message"]})
            # messages.append({"role": "system", "content": chat["bot_message"]})
        messages.append({"role": "user", "content": user_question})
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            # temperature=temperature,
            stream=True
        )

        bot_message = stream_response(response, bot_placeholder)
        # st.session_state.conversation_history.append((user_question, bot_message))
        # Always append to conversation history

        st.session_state.conversation_history.append({
            "user_message": user_question,
            "bot_message": bot_message,

        })




    except Exception as e:
        st.error(f"Error processing request: {str(e)}")


def run():
    model_names = [
        # "gpt-4-turbo",
        "gpt-4o",
        "gpt-3.5-turbo-instruct",
        "gpt-4-turbo-preview",  # Updated model name
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "o3-mini"
    ]
    st.set_page_config(page_title="General AI Assistant", page_icon="🤖")
    st.write(css, unsafe_allow_html=True)
    st.header("AI Assistant : 🤖:")


    initialize_session_state()
    input_prompt = st.text_area("Set System Prompt",
                                 "You are a helpful AI assistant",
                                 height=100)
    base_prompt = (
        "Answer in English or the language of the user's query. "
        "Do not use LaTeX, markdown, or any special formatting—write plain text using standard symbols (*, /, ^, and parentheses for math). "
        "Act as a general AI assistant and answer based on general knowledge from the internet."
    )
    system_prompt = input_prompt + base_prompt
    # model_name = st.sidebar.text_area("model name",
    #                              "gpt-4-turbo")
    selected_model = st.sidebar.selectbox("Select a GPT Model", model_names)
    temperature = st.sidebar.slider(min_value=0.0, max_value=1.0, step=0.1,value=0.7, label="Temperature")


    user_input = st.text_area("Enter your query", height=100)

    # Update user_input in session state
    st.session_state['user_input'] = user_input
    # user_question = st.text_area("Ask a question", height= 100)
    if st.button("Reset Chat"):
        if 'user_input' in st.session_state:
            st.session_state.user_input = ""
        st.session_state.conversation_history = []
    for message in st.session_state.conversation_history:
        st.write(user_template.replace("MSG", message['user_message']), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", message['bot_message']), unsafe_allow_html=True)
    if st.button("Submit"):
        if user_input:  # If input is not empty, call the model
            # answer = chat_with_gpt(system_prompt, user_question)
            st.write(user_template.replace("MSG", st.session_state['user_input']), unsafe_allow_html=True)
            bot_message_placeholder = st.empty()
            handle_chat_response(st.session_state['user_input'],system_prompt, bot_message_placeholder,temperature,selected_model)


def chat_with_gpt(system_prompt, question, model_name):
    base_prompt = (
        "You are a helpful AI assistant. "
        "Answer in English or the language of the user's query. "
        "Do not use LaTeX, markdown, or any special formatting—write plain text using standard symbols (*, /, ^, and parentheses for math). "
        "Act as a general AI assistant and answer based on general knowledge from the internet."
    )
    final_prompt = system_prompt + base_prompt
    response = client.chat.completions.create(
        model=f"{model_name}",#"gpt-4-turbo",
        messages=[
            {"role": "system", "content": f"{final_prompt}"},
            {"role": "user", "content":question}
        ],
        temperature=0.3  # Controls randomness, lower values make responses more deterministic
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    run()
    # print("pass")
