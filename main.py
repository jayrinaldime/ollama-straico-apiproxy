from app import app
from api_endpoints import lm_studio
from api_endpoints import ollama

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3214)