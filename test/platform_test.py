import asyncio
import backend.straico_platform as platform
import pprint
import pathlib


async def model_listing():
    model_id_mapping = {}
    models = await platform.models()
    for model in models:
        name = model["name"]
        model_name = model["model"]
        _id = model["_id"], model["pricing"]["coins"]
        model_id_mapping[name] = _id
        model_id_mapping[model_name] = _id
    return model_id_mapping


async def chat_with_image(model_id, model_cost, image_path, text_prompt):
    async with platform.autoerase_upload_image(image_path) as upload_stat:
        async with platform.autoerase_chat(
            model_id,
            model_cost,
            upload_stat["file"]["url"],
            upload_stat["file"]["words"],
            text_prompt,
        ) as chat_response:
            return chat_response["message"]["data"]["content"]

    # pprint.pprint(chat_response)
    """{ 'hash': 'fdd',
 'message': {'_id': 'dd',
             'additional_config': None,
             'data': {'content': 'The CAPTCHA text is "JP2 4 12".',
                      'function': None,
                      'role': 'assistant'},
             'date': '2024-08-20T14:57:57.429Z',
             'hidden': False,
             'model': 'GPT-4o mini',
             'modelRef': 'dddd',
             'selected': True,
             'tool': None,
             'tool_calls': None},
 'modal': {'data': [36096.31, 0], 'show': 'review_medium'},
 'success': True,
 'title': 'Captcha: What You Need to Know'}"""


async def main():
    image_path = pathlib.Path("./Screenshot 2024-08-20 at 22.22.23.png")
    text_prompt = "what is the captcha"

    # model_mapping = await model_listing()
    # pprint.pprint(model_mapping)
    # model = "OpenAI: GPT-4o mini"
    # model_id, model_cost = model_mapping[model]
    # print(model_id, model_cost)

    model_id = "66998fd4f394ef4982b23d18"
    model_cost = 0.4
    response = await chat_with_image(model_id, model_cost, image_path, text_prompt)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
