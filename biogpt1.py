import streamlit as st
import google.generativeai as genai
import json
import os

# File to store API key
CONFIG_FILE = "config.json"

def load_api_key():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
                return config.get('api_key')
    except Exception:
        return None
    return None

def save_api_key(api_key):
    with open(CONFIG_FILE, 'w') as file:
        json.dump({'api_key': api_key}, file)

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def get_gemini_response(model, question):
    prompt = f"""You are a medical assistant. Please provide helpful medical information for the following question.
    
    Question: {question}
    
    Please provide a detailed response including:
    1. Possible causes
    2. Relief measures
    3. When to seek professional medical help
    4. Preventive measures
    
    Remember to include a disclaimer that this is not a substitute for professional medical advice."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    st.title("Medical Assistant Chatbot")
    
    # Load existing API key
    api_key = load_api_key()
    
    # Only show API input if no key is saved
    if not api_key:
        st.warning("Please enter your Gemini API key to start.")
        new_api_key = st.text_input("Enter Gemini API Key", type="password")
        if st.button("Save API Key"):
            if new_api_key:
                save_api_key(new_api_key)
                st.success("API key saved successfully!")
                st.rerun()  # Updated from experimental_rerun()
            else:
                st.error("Please enter an API key.")
        return
    
    # Initialize model if not in session state
    if 'model' not in st.session_state:
        st.session_state.model = configure_gemini(api_key)
    
    # Chat interface
    st.header("Chat with Medical Assistant")
    user_question = st.text_input("What medical concerns do you have?")
    
    if st.button("Get Answer"):
        if not user_question:
            st.warning("Please enter your question.")
        else:
            with st.spinner("Generating response..."):
                response = get_gemini_response(
                    st.session_state.model,
                    user_question
                )
                st.write(response)
    
    # Add option to reset API key
    if st.sidebar.button("Reset API Key"):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        st.session_state.clear()
        st.rerun()  # Updated from experimental_rerun()
    
    # Disclaimer
    st.markdown("---")
    st.caption("Disclaimer: This chatbot is for informational purposes only and should not replace professional medical advice.")

if __name__ == "__main__":
    main()