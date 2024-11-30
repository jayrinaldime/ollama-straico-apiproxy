from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from app import app

# Add template configuration
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Straico Proxy API Services",
        "description": "Welcome to the Straico API platform. Explore our available services and endpoints.",
        "user": {
            "first_name": "Jay",
            "last_name": "Rinaldi", 
            "coins": 772594.06, 
            "plan": "Diamond Pack"
        },
        "links": [
            {"name": "API Documentation", "url": "/docs"},
            {"name": "Swagger UI", "url": "/redoc"},
            {"name": "Ollama Model List", "url": "/api/tags"},
            {"name": "LM Studio / OpenAI Compatible Model List", "url": "/v1/models"},
            {"name": "User Details", "url": "/api/user"},
            {"name": "RAG List", "url": "/rag-list"},
        ],
    })
```

view/__init__.py
```python
<<<<<<< SEARCH
    })
