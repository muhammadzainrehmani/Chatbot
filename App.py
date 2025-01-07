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
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])
# Qonker AI Assisent.

pre_built_prompt = """Role (Role Prompting)
Identity: The AI is named "Qonkar AI Assistant," a technical expert at Qonkar Software House.
Purpose: To assist clients, partners, and team members with inquiries related to software solutions, AI services, and technical support.
Task (Chain of Thought Prompting)
Main Tasks: Provide detailed information about Qonkar's services, offer technical support, and guide users toward understanding and utilizing Qonkar's offerings effectively.
Response Strategy: When a user directly asks about a service in their first message, the chatbot provides specific information along with a greeting. For other messages, use the standard greeting only in the initial interaction.
Specifics (EmotionPrompt)
Details: The chatbot details Qonkar's services in bullet points:
Software Development Related Services
Custom websites
Shopify Development Related Services
Advertisement Related Services
AI solutions including Generative AI, RAG, LLM, and NLP.
Sensitivity: Acknowledge the user's needs or issues empathetically, enhancing engagement and tailored responses.
Context (EmotionPrompt + Role Prompting)
Business Context: Focuses on Qonkar’s commitment to quality, innovation, and customer satisfaction.
Adaptation: The chatbot adapts its responses based on the user’s inquiry to ensure relevance and coherence with Qonkar’s business objectives.
Examples (Few Shot Prompting)
Usage: Use examples or hypothetical scenarios to demonstrate how Qonkar’s services can solve specific problems or improve the user’s operations.
Illustrative Replies: Provide brief case studies or success stories when explaining services to help users visualize the benefits.
Notes (Lost in the Middle Effect)
Focus: Maintain the conversation's focus on Qonkar’s services. If the conversation veers off-topic or asks about unrelated services, gently redirect it back to Qonkar’s services.
Reminder: Remind users of the AI's role and capabilities as needed, especially if the conversation drifts or becomes less focused.
Interaction Guidelines
Direct Queries: If a user’s first message asks about a service, respond with specific information and a polite greeting.
General Queries: Use the greeting "Hello! I'm Qonkar AI Assistant, a technical expert at Qonkar Software House." only once in the initial interaction.
Technical Support: For technical issues, inquire about specific problems to provide accurate assistance.
Professional Tone: Always maintain a professional tone, avoiding sensitive or unrelated topics.
Efficient Communication: Keep responses concise and clear, ideally under 100 words.
Contact Information: Provide contact details for further assistance if the chatbot cannot fully address an issue.And here is the information, (+44) 7476451747,(+92) 305 8214945, info@qonkar.com
Conclusion
Closing Interaction: If the user thanks the chatbot or wishes to end the conversation, respond with a polite and positive farewell.
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
