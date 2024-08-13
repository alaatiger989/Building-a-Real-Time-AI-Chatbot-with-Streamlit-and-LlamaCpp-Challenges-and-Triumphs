import streamlit as st
from langchain_community.llms import LlamaCpp


# Cache the model loading
@st.cache_resource
def load_model():
    return LlamaCpp(
        model_path="C:/Users/thegh/Python Projects/Ai Models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        n_gpu_layers=30,
        n_ctx=5000,
        f16_kv=True,
        max_tokens=5000,
        temperature=0.1,
        streaming=True,
        verbose=True
    )


# Load the model
llm = load_model()

# Initialize chat history if not already in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Define a function that returns a generator for the streamed response
def generate_response(prompt):
    return llm.stream(prompt)


# Streamlit UI setup
st.title("AI Chatbot with Llama")
st.write("Ask any question, and the AI will respond in real-time!")

# Generate response when the user submits a question
if 'generating' not in st.session_state:
    st.session_state.generating = False

# Input field
if st.session_state.generating:
    user_question = st.text_input("You:", placeholder="Generating response...", disabled=True)
else:
    user_question = st.text_input("You:", placeholder="Ask your question here...")

if st.button("Submit") and user_question and not st.session_state.generating:
    # Combine chat history and user question
    initial_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

                Cutting Knowledge Date: December 2023
                Today Date: 23 Jul 2024

                You are a helpful assistant and Respond in details<|eot_id|><|start_header_id|>user<|end_header_id|>
                """
    full_prompt = initial_prompt + "".join(st.session_state.chat_history) + "User: " + user_question + " Assistant:"

    # Set generating flag
    st.session_state.generating = True

    # Display the loading spinner while generating the response
    response_placeholder = st.empty()
    response_text = ""

    # Generate response
    with st.spinner("Generating response..."):
        response_generator = generate_response(full_prompt)

        for chunk in response_generator:
            response_text += chunk
            response_placeholder.markdown(f"**Assistant:** {response_text}")

        # Add the user question and response to chat history
        st.session_state.chat_history.append(f"**User:** {user_question}\n\n")
        st.session_state.chat_history.append(f"**Assistant:** {response_text}\n\n")

    # Reset generating flag
    st.session_state.generating = False

# Display full chat history
for entry in st.session_state.chat_history:
    st.write(entry)

