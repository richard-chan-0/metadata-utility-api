from src.api import create_app
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = create_app()

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
