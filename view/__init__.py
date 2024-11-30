from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app import app
from backend import user_detail, list_rags, delete_rag
from backend.straico_platform import list_rag_documents  # Add this import
# Add template configuration
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    details = await user_detail()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Straico Proxy API Services",
        "description": "Welcome to the Straico API platform. Explore our available services and endpoints.",
        "user": details,
        "links": [
            {"name": "API Documentation", "url": "/docs"},
            {"name": "Swagger UI", "url": "/redoc"},
            {"name": "Ollama Model List", "url": "/api/tags"},
            {"name": "LM Studio / OpenAI Compatible Model List", "url": "/v1/models"},
            {"name": "User Details", "url": "/api/user"},
            {"name": "RAG List", "url": "/rag-list"},
        ],
    })

@app.get("/rag-list", response_class=HTMLResponse)
async def rag_list(request: Request):
    rag_docs = await list_rags()
    return templates.TemplateResponse("rag_list.html", {
        "request": request,
        "rag_docs": rag_docs
    })

@app.delete("/api/rag/delete/{rag_id}")
async def delete_rag_endpoint(rag_id: str):
    try:
        result = await delete_rag(rag_id)
        return JSONResponse(
            content={"message": "RAG deleted successfully", "result": result}, 
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


