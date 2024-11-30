from fastapi.responses import JSONResponse
from app import app, logging
from backend.straico import list_model, list_agents


logger = logging.getLogger(__name__)


@app.get("/api/models")
@app.get("/v1/api/models")
@app.get("/v1/models")
@app.get("/models")
async def lmstudio_list_models():
    """
     {'name': 'Anthropic: Claude 3 Haiku',
    'model': 'anthropic/claude-3-haiku:beta',
    'pricing': {'coins': 1, 'words': 100}}
    """
    agent_request = list_agents()
    models = await list_model()

    if models is None:
        return JSONResponse(content={"models": []})

    if "chat" in models:
        models = models["chat"]

    models = [
        {
            "id": model["model"],
            "object": "model",
            "owned_by": model["name"].split(":")[0],
            "permission": [{}],
        }
        for model in models
    ]
    agents = await agent_request
    if agents is not None and len(agents) > 0:
        models += [
            {
                "id":  f"agent/{m['name']}:{m['_id']}",
                "object": "model",
                "owned_by": "Straico",
                "permission": [{}],
            }
            for m in agents
        ]

    response = {"data": models, "object": "list"}
    return JSONResponse(content=response)
