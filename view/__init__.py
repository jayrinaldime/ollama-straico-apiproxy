import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, HTTPException, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app import app
from backend import user_detail, list_rags, delete_rag, create_rag
from backend.straico_platform import list_rag_documents  # Add this import
# Add template configuration
templates = Jinja2Templates(directory="templates")

# Add file validation constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.csv', '.txt', '.xlsx', '.py'}
MAX_FILES = 4

def secure_filename(filename):
    """
    Generate a secure filename by removing potentially dangerous characters
    and ensuring a safe filename
    """
    # Remove directory path if present
    filename = os.path.basename(filename)
    
    # Remove non-ascii characters and replace with '_'
    filename = "".join(
        c if c.isalnum() or c in ('-', '_', '.') else '_' 
        for c in filename
    )
    
    # Ensure filename is not empty
    if not filename:
        filename = 'unnamed_file'
    
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
            
            # Prepare original filenames for tracking
            original_filenames = ', '.join(f.filename for f in file_to_uploads)
            
            # Call RAG creation method
            rag_result = await create_rag(
                name=name,
                description=description,
                original_filename=original_filenames,
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
                    "rag_id": rag_result,
                    "files": original_filenames
                }
            )
        
        except HTTPException as he:
            # Re-raise HTTP exceptions
            raise he
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error in RAG creation: {e}")
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
