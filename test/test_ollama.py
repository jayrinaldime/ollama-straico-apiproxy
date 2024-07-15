import pytest

BASE_URL = "http://127.0.0.1:3214"

MODEL = "DUMMY_MODEL"
MSGS =[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ]

PROMPT = 'Why is the sky blue?'

from ollama import Client, AsyncClient

EXPECTED_TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nec felis eu lacus finibus laoreet non non arcu. Mauris et lorem at ligula aliquam sodales sit amet suscipit justo. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In lectus libero, commodo quis finibus imperdiet, lobortis vitae ex. Cras commodo elit vel erat lobortis pretium. Nunc sagittis elementum ligula a aliquam. Nunc mollis est sodales enim feugiat dignissim. Nam et commodo orci. Quisque id semper nunc. Duis vel convallis elit. Donec dignissim eros in sapien consectetur sagittis. Donec est tortor, convallis non elit id, viverra luctus est. Nullam elementum, tortor eu mattis accumsan, diam lacus tristique elit, placerat viverra lacus urna in massa.

Nunc ac arcu ex. Proin ultrices ultricies semper. Ut id mauris eget tortor tincidunt scelerisque. Sed eget urna at ipsum interdum dapibus ut non ipsum. Nam luctus, arcu posuere iaculis volutpat, est erat finibus ligula, eget iaculis diam leo elementum nisl. Integer congue nec turpis euismod consequat. Duis at sem vitae dolor ornare tristique. Duis dapibus nisi massa, sit amet tristique tortor tempus sit amet. Nunc ac mollis tortor. Cras at elit enim. Sed egestas eget ipsum cursus molestie. Aliquam et finibus nisi, at viverra mi. Sed mattis non magna a semper.
"""
def test_chat():
    client = Client(host=BASE_URL)
    response = client.chat(model=MODEL, messages=MSGS)

    assert response["message"]["content"] == EXPECTED_TEXT
    assert response["done"] is True
    assert response["model"] == MODEL
@pytest.mark.asyncio
async def test_async_chat():
    aio_client = AsyncClient(host=BASE_URL)
    response = await aio_client.chat(model=MODEL, messages=MSGS)

    assert response["message"]["content"] == EXPECTED_TEXT
    assert response["done"] is True
    assert response["model"] == MODEL

@pytest.mark.asyncio
async def test_async_stream_chat():
    aio_client = AsyncClient(host=BASE_URL)
    request = aio_client.chat(model=MODEL, messages=MSGS, stream=True)
    parts = []
    async for part in await request:
        parts.append(part['message']['content'])
        assert part["model"] == MODEL
    whole = " ".join(parts)
    assert whole.strip() == EXPECTED_TEXT.strip()


def test_generate():
    client = Client(host=BASE_URL)
    response = client.generate(model=MODEL, prompt=PROMPT)

    assert response["response"] == EXPECTED_TEXT
    assert response["done"] is True
    assert response["model"] == MODEL

def test_generate_raw():
    client = Client(host=BASE_URL)
    response = client.generate(model=MODEL, prompt=PROMPT, stream=False, raw=True)

    assert response["response"] == EXPECTED_TEXT
    assert response["done"] is True
    assert response["model"] == MODEL

@pytest.mark.asyncio
async def test_async_generate():
    aio_client = AsyncClient(host=BASE_URL)
    response = await aio_client.generate(model=MODEL, prompt=PROMPT)

    assert response["response"] == EXPECTED_TEXT
    assert response["done"] is True
    assert response["model"] == MODEL

@pytest.mark.asyncio
async def test_async_generate_stream():
    aio_client = AsyncClient(host=BASE_URL)
    request = aio_client.generate(model=MODEL, prompt=PROMPT, stream=True)
    parts = []
    async for part in await request:
        parts.append(part['response'])
        assert part["model"] == MODEL

    whole = " ".join(parts)
    assert whole.strip() == EXPECTED_TEXT.strip()

@pytest.mark.asyncio
async def test_async_generate_stream_raw():
    aio_client = AsyncClient(host=BASE_URL)
    request = aio_client.generate(model=MODEL, prompt=PROMPT, stream=True, raw=True)
    parts = []
    async for part in await request:
        parts.append(part['response'])
        assert part["model"] == MODEL

    whole = " ".join(parts)
    assert whole.strip() == EXPECTED_TEXT.strip()

def test_models():
    client = Client(host=BASE_URL)
    models = client.list()

    assert "models" in models
    assert len(models["models"]) == 22