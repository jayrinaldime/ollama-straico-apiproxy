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
        "links": [
            {"name": "API Documentation", "url": "/docs"},
            {"name": "Swagger UI", "url": "/redoc"}
        ]
    })
