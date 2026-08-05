import subprocess
import threading
import time

from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

load_dotenv() # Load environment variables from .env file

def run_backend():
    try:
        logger.info("Starting backend server...")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"], check=True)
    except CustomException as e:
        logger.error(f"Problem with Backend server failed to start: {e}")
        raise CustomException("Problem with Backend server failed to start", error_detail=e)


def run_frontend():
    try:
        logger.info("Starting frontend server...")
        # subprocess.run(["streamlit", "run", "app.frontend.ui:st"], check=True)
        subprocess.run(["streamlit" , "run" , "app/frontend/ui.py"],check=True)
    except CustomException as e:
        logger.error(f"Problem with Frontend server failed to start: {e}")
        raise CustomException("Problem with Frontend server failed to start", error_detail=e)


if __name__ == "__main__":
    try:
        thread_backend = threading.Thread(target=run_backend).start()
        time.sleep(3)  # Wait for the backend to start before starting the frontend
        thread_frontend = threading.Thread(target=run_frontend).start()
    except CustomException as e:
        logger.error(f"Error occurred while starting servers: {e}")
        logger.exception(f"CustomException occured : {str(e)}")
        raise CustomException("Error occurred while starting servers", error_detail=e)
        
    
