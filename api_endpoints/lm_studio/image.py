import json
import tempfile

from fastapi import Request
from fastapi.responses import JSONResponse
from app import app, logging
from backend.straico import image_generation
from aio_straico.api.v0 import ImageSize
from aio_straico.utils.tracing import observe, tracing_context

logger = logging.getLogger(__name__)


@app.post("/v1/images/generations")
@observe
async def lm_image_generation(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    tracing_context.update_current_observation(input=dict(post_json_data))

    # model = post_json_data.get("model")
    # if model != "openai/dall-e-3":
    api_key = request.headers.get("authorization")
    if api_key is not None:
        api_key = api_key[7:]
    model = "openai/dall-e-3"
    prompt = post_json_data.get("prompt")
    n = int(post_json_data.get("n", "1"))
    size = post_json_data.get("size", "512x512")
    x, y = size.strip().lower().split("x")
    if x == y:
        size = ImageSize.square
    elif x > y:
        size = ImageSize.landscape
    elif x < y:
        size = ImageSize.portrait

    images = await image_generation(
        model=model, n=n, prompt=prompt, size=size, api_key=api_key
    )

    image_urls = [{"url": image_url} for image_url in images["images"]]
    print(image_urls)

    return JSONResponse(content={"created": 1589478378, "data": image_urls})
