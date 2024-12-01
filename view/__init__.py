import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, HTTPException, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app import app
from backend import user_detail, list_rags, delete_rag, create_rag, list_agents, delete_agent, create_agent, get_model_mapping
# Add template configuration
templates = Jinja2Templates(directory="templates")

# Add file validation constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.csv', '.txt', '.xlsx', '.py'}
MAX_FILES = 4

from asyncio import gather
def secure_filename(filename):
    """
    Generate a secure filename by removing potentially dangerous characters
    and ensuring a safe filename
    """
    # Remove non-ascii characters and replace with '_'
    filename = "".join(
        c if c.isalnum() or c in ('-', '_', '.') else '_' 
        for c in filename
    )
    
    # Ensure filename is not empty
    if not filename:
        filename = 'unnamed_file.txt'
    
    return filename

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
            {"name": "RAG Management", "url": "/rag-list"},
            {"name": "Agent Management", "url": "/agent-list"},
        ],
    })

@app.get("/rag-list", response_class=HTMLResponse)
async def rag_list(request: Request):
    rag_docs = await list_rags()
    return templates.TemplateResponse("rag_list.html", {
        "request": request,
        "rag_docs": rag_docs
    })

@app.post("/api/rag/create")
async def create_rag_endpoint(
    name: str = Form(...),
    description: str = Form(...),
    chunking_method: str = Form('fixed_size'),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(50),
    breakpoint_threshold_type: str = Form(None),
    buffer_size: int = Form(500),
    file_to_uploads: List[UploadFile] = File(...)
):
    # Create a temporary directory to store uploaded files
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Validate files first
            # await validate_uploaded_files(file_to_uploads)
            
            # Save files to temporary directory
            file_paths = []
            for uploaded_file in file_to_uploads:
                # Generate a safe filename
                safe_filename = secure_filename(uploaded_file.filename)
                file_path = Path(temp_dir) / safe_filename
                
                # Write file contents
                with file_path.open('wb') as buffer:
                    buffer.write(await uploaded_file.read())
                file_paths.append(file_path)


            # Call RAG creation method
            rag_result = await create_rag(
                name=name,
                description=description,
                file_to_uploads=file_paths,
                chunking_method=chunking_method,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                breakpoint_threshold_type=breakpoint_threshold_type,
                buffer_size=buffer_size
            )
            
            return JSONResponse(
                content={
                    "message": "RAG created successfully", 
                    "rag_id": rag_result
                }
            )
        
        except HTTPException as he:
            # Re-raise HTTP exceptions
            raise he
        except Exception as e:
            # Log unexpected errors
            #logger.error(f"Unexpected error in RAG creation: {e}")
            raise HTTPException(status_code=500, detail="Internal server error during RAG creation")

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


@app.get("/agent-list", response_class=HTMLResponse)
async def agent_list(request: Request):
    agents, models, rags = await gather(list_agents(), get_model_mapping(), list_rags())
    model_mapping = dict([(m["model"], m) for m in models])
    for agent in agents:
        default_llm = agent["default_llm"]
        agent["model_name"] = model_mapping[default_llm]["name"]
    return templates.TemplateResponse("agent_list.html", {
        "request": request,
        "agents": agents,
        "models": models,
        "rags": rags
    })

@app.delete("/api/agent/delete/{agent_id}")
async def delete_agent_endpoint(agent_id: str):
    try:
        result = await delete_agent(agent_id)
        return JSONResponse(
            content={"message": "Agent deleted successfully", "result": result},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/create")
async def create_rag_endpoint(
        name: str = Form(...),
        description: str = Form(...),
        custom_prompt: str = Form(...),
        model: str = Form(...),
        rag: str = Form(...),
        tags: str = Form(...)
):
        # Call Agent creation method
        tags = [tag.strip() for tag in tags.strip().split(",") if len(tag.strip()) > 0 ]

        agent_result = await create_agent(
            name=name,
            description=description,
            custom_prompt=custom_prompt,
            model=model,
            rag_id=rag,
            tags=tags
        )

        return JSONResponse(
            content={
                "message": "Agent created successfully",
                "agent_id": agent_result
            }
        )

@app.post("/api/agent/update/{agent_id}")
async def update_agent_endpoint(
    agent_id: str,
    name: str = Form(...),
    description: str = Form(...),
    custom_prompt: str = Form(...),
    model: str = Form(...),
    rag: str = Form(...),
    tags: str = Form(...)
):
    # Call Agent update method
    tags = [tag.strip() for tag in tags.strip().split(",") if len(tag.strip()) > 0]

    agent_result = await update_agent(
        agent_id=agent_id,
        name=name,
        description=description,
        custom_prompt=custom_prompt,
        model=model,
        rag_id=rag,
        tags=tags
    )

    return JSONResponse(
        content={
            "message": "Agent updated successfully",
            "agent_id": agent_id
        }
    )
