import json
import tempfile

from fastapi import Request
from fastapi.responses import JSONResponse
from app import app, logging
from backend.straico import image_generation
from aio_straico.api.v0 import ImageSize
from base64 import encodebytes


logger = logging.getLogger(__name__)


@app.post("/v1/images/generations")
async def lm_image_generation(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    logger.debug(post_json_data)

    # model = post_json_data.get("model")
    # if model != "openai/dall-e-3":
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

    with tempfile.TemporaryDirectory() as directory:
        images = await image_generation(
            model=model, n=n, prompt=prompt, size=size, directory=directory
        )
        encoded_images = []

        for image_path in images:
            with image_path.open("rb") as reader:
                bin_image = reader.read(-1)
                data_base64 = encodebytes(bin_image).decode()
                encoded_images.append({"b64_json": data_base64})

    return JSONResponse(content={"created": 1589478378, "data": encoded_images})
