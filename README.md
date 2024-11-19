# Qonkar AI Chatbot with Streamlit

This repository contains a Streamlit-based chatbot application that utilizes Google's Gemini API. The chatbot provides an interactive conversational experience, enhanced with pre-defined sample prompts for user convenience.

## Features

1.	**Gemini API Integration:** Leverages the power of Google's Gemini for natural language understanding and generation.
2.	**Interactive Chat Interface:** Streamlit provides a user-friendly interface for engaging in conversations with the chatbot.
3.	**Sample Prompts:** Offers clickable sample prompts to guide user interaction and provide examples of effective queries.
4.	**Automatic Prompt Submission:** Clicking a sample prompt automatically populates the input field and submits it to the Gemini 
          API.
5.	**Loading Spinner:** Displays a visual loading spinner while waiting for the chatbot's response.
6.	**Conversation History:**  Maintains a history of the conversation for context and reference.


## Installation

1. **Clone the repository:**

         git clone https://github.com/your-username/your-repository-name.git
2.	**Navigate to the project directory:**
	  cd your-repository-name
    
3.	**Create a virtual environment (recommended):**
          python3 -m venv .venv
  	  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    
4.	**Install dependencies:**
          pip install -r requirements.txt
    
5.	**Set up your Gemini API Key:**
    o	Obtain a Gemini API key from Google AI Platform.
    o	Set the GOOGLE_API_KEY environment variable:
    o	Export GOOGLE_API_KEY="YOUR_API_KEY" # Linux/macOS
    o	Set GOOGLE_API_KEY="YOUR_API_KEY" # Windows
    
Or you can directly paste it in the model parameter at the beginning of app.py


**Usage**

1.	**Run the Streamlit app:**
      streamlit run app.py
    
2.	**Interact with the chatbot:**
    o	Type your prompts in the input field and press Enter.
    o	Click on the provided sample prompts to quickly initiate conversations.
  	
**Configuration**

•	**app.py:** The main application file. You can customize the following:
      o	**pre_built_prompt:** Modify the initial prompt to guide the chatbot's persona and behavior.
      o	**model:** Specifies the desired Gemini model.
      o	**temperature, top_p, max_output_tokens:** Adjust these parameters to fine-tune the chatbot's responses (creativity, diversity, length, etc.).
      o	**sample_prompts:** Add or modify the list of sample prompts.
      
**Contributing**
    Contributions are welcome! Please feel free to open issues and submit pull requests.

**License**
    []

**Contact**
    Qonkar - info@qonkar.com
 
Remember to replace placeholders like your-username,  your-repository-name, and YOUR_API_KEY with your actual information.  This detailed README provides clear instructions for setup, usage, and configuration, making your project easy to understand and use for others.

