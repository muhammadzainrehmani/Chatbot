import os
from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
# Initialize the GenAI client
import google.generativeai as genai

genai_api_key = st.secrets["genai_api_key"]

# Add custom logos for the assistant and user
user_logo = "qonkar-technologies-logo.svg" # Path to Qonkar AI Assistant logo


# Set streamlit page configuration
st.set_page_config(page_title="Qonkar ChatBot")
st.title("Qonkar AI Assistant")
st.write("**(You can also contact us via: info@qonkar.com)**")

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

if 'context' not in st.session_state:
    st.session_state['context'] = []  # Store the conversation history

# genai.configure(api_key=os.environ["API_KEY"])

genai.configure(api_key=genai_api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])
# Qonker AI Assisent.

pre_built_prompt = """Your name is Qonkar AI Assistant. You are a technical expert at Qonkar Software House, here to assist clients, partners, and team members with questions about our software solutions, AI services, and technical support. Your tone is professional, helpful, and courteous.

1. Begin the conversation with a friendly greeting, ask for the user’s name, and inquire how you can assist them with their software or AI needs. Use the friendly greeting only in the first response. If the user directly asks about a specific need, skip introductions and provide a direct response to their query.
2. Provide clear, accurate, and concise information on Qonkar’s services, which include only  software development(Custom software development), Custom Website, Shopify Store, Digital Marketing(all services that cover in digital marketing) and in AI solutions working in Generative AI( API Integration),RAG(or relavent services of RAG that RAG can solve the problem like chatbot, etc), LLM and NLP Relavent task. When user ask any other services that are not related to above than you say no Untill Qonkar not provide this services.
3. Emphasize our commitment to quality, innovation, and customer satisfaction when discussing Qonkar’s offerings.
4. For technical support inquiries, ask for any specific issues or details to provide the most relevant assistance.
5. Maintain a professional tone, steering clear of sensitive or unrelated topics. Gently redirect the conversation if it veers off topic.
6. Offer concise responses, with a maximum of 100 words to ensure clarity and efficiency in communication.
7. Provide the user answer that he asked.
8.In any situation that you are not able to provide the information or any relavent situation provide our contact information to the user for discuss our team manualy and here is the information, (+44) 7476451747,(+92) 305 8214945, info@qonkar.com
9.If the user thanks you or ends the conversation, reply with a polite and positive farewell.

Remember, your primary goal is to support clients and team members, enhance their understanding of Qonkar’s solutions, and reinforce our commitment to excellence and innovation.
"""

# # Sample Prompts
# sample_prompts = [
#     "Tell me more about Qonkar Technologies.",
#     "What AI solutions does Qonkar offer?",
#     "Can Qonkar build a chatbot for my Organization?",
#     "Can Qonkar build a custom website for my business?",
# ]

# Sample Prompts
sample_prompts = [
    "Could you provide more information about Qonkar Technologies?",
    "What AI solutions are offered by Qonkar Technologies?",
    "Does Qonkar Technologies develop custom chatbots for organizations?",
    "Can Qonkar Technologies create a tailored website for my business?",
]


def build_message_list():
    """
    Build a concatenated string of all messages including system, human and AI messages.
    """
    # Start with the pre-built prompt
    messages = pre_built_prompt + "\n\n"

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            messages += f"User: {human_msg}\n"
        if ai_msg is not None:
            messages += f"AI Mentor: {ai_msg}\n"

    return messages

def generate_response():
    """
    Generate AI response using the GenAI model.
    """
    # Build the concatenated string of messages
    concatenated_messages = build_message_list()

    # Generate response using the GenAI model
    response = chat_session.send_message(concatenated_messages)
    ai_response = response.text

    return ai_response


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


# Define function to handle prompt clicks
def handle_prompt_click(prompt):
    st.session_state.prompt_input = prompt  # Update the input field
    st.session_state.entered_prompt = prompt  # Trigger the response generation
    submit() # submit input value by enter or by click


# Display sample prompts as buttons, All in single line
# st.write("**Sample Prompts:**")
# cols = st.columns(len(sample_prompts))  # Create columns for better layout
# for i, prompt in enumerate(sample_prompts):
#     with cols[i]:
#         if st.button(prompt):
#             handle_prompt_click(prompt)

# Display sample prompts as buttons, each in single single Row
st.write("**Sample Prompts:**")
for prompt in sample_prompts:
    if st.button(prompt): # Display each button on a new line
        handle_prompt_click(prompt)



# Create a text input for user
st.text_input('**YOU:** ',  key='prompt_input', on_change=submit)

if st.session_state.entered_prompt != "":
    with st.spinner("Generating response..."): # Add spinner here
        # Get user query
        user_query = st.session_state.entered_prompt

        # Append user query to past queries
        st.session_state.past.append(user_query)

        # Generate response
        output = generate_response()

        # Append AI response to generated responses
        st.session_state.generated.append(output)


# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        AI = st.chat_message("ai")
        AI.image("qonkar-technologies-logo.svg", width=100)
        AI.write(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
