import streamlit as st
import requests

from app.config.settings import Settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi-AI Agent", page_icon="🤖", layout="centered"   )

st.title("Multi-AI Agent using Groq and Tavilty Search")

system_prompt = st.text_area("Define your AI Agent", height=70)

selected_model = st.selectbox("Select Your AI Model", Settings().ALLOWED_MODELS_NAMES)

allow_web_search = st.checkbox("Allow Search", value=False)

user_query = st.text_area("Enter your query", height=150)


API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }

    try:
        logger.info(f"Sending request to API for model: {selected_model}")
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200: # Check for successful response
            agent_response = response.json().get("response","")
            logger.info(f"Successfully received response from API for model: {selected_model}")

            st.subheader("AI Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)  # Preserve line breaks in Markdown

        else:
            logger.error("Backend error")
            st.error("Error with backend")
    
    except Exception as e:
        logger.error("Error occured while sending request to backend")
        st.error(str(CustomException("Failed to communicate to backend")))   

         
    #     else:
    #         logger.error(f"API returned an error: {response.status_code} - {response.text}")
    #         st.error(f"Error: {str(CustomException('Failed to get AI response', error_detail=response.text))}")

    # except Exception as e:
    #     logger.error("Error occurred while communicating with the API")
    #     st.error(f"Error: {str(CustomException('Failed to get AI response', error_detail=e))}")

