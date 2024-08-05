from app import logging

logger = logging.getLogger(__name__)


def prompt_completion(msg: str, model: str = "openai/gpt-3.5-turbo-0125") -> str:
    # some  clients add :latest
    if model.endswith(":latest"):
        model = model.replace(":latest", "")
    post_request_data = {"model": model, "message": msg}
    logger.debug(f"Request Post Data: {post_request_data}")

    return """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nec felis eu lacus finibus laoreet non non arcu. Mauris et lorem at ligula aliquam sodales sit amet suscipit justo. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In lectus libero, commodo quis finibus imperdiet, lobortis vitae ex. Cras commodo elit vel erat lobortis pretium. Nunc sagittis elementum ligula a aliquam. Nunc mollis est sodales enim feugiat dignissim. Nam et commodo orci. Quisque id semper nunc. Duis vel convallis elit. Donec dignissim eros in sapien consectetur sagittis. Donec est tortor, convallis non elit id, viverra luctus est. Nullam elementum, tortor eu mattis accumsan, diam lacus tristique elit, placerat viverra lacus urna in massa.

Nunc ac arcu ex. Proin ultrices ultricies semper. Ut id mauris eget tortor tincidunt scelerisque. Sed eget urna at ipsum interdum dapibus ut non ipsum. Nam luctus, arcu posuere iaculis volutpat, est erat finibus ligula, eget iaculis diam leo elementum nisl. Integer congue nec turpis euismod consequat. Duis at sem vitae dolor ornare tristique. Duis dapibus nisi massa, sit amet tristique tortor tempus sit amet. Nunc ac mollis tortor. Cras at elit enim. Sed egestas eget ipsum cursus molestie. Aliquam et finibus nisi, at viverra mi. Sed mattis non magna a semper.
"""


def list_model():
    return {
        "data": {
            "chat": [
                {
                    "name": "Anthropic: Claude 3 Haiku",
                    "model": "anthropic/claude-3-haiku:beta",
                    "pricing": {"coins": 1, "words": 100},
                },
                {
                    "name": "Anthropic: Claude 3 Opus",
                    "model": "anthropic/claude-3-opus",
                    "pricing": {"coins": 24, "words": 100},
                },
                {
                    "name": "Anthropic: Claude 3 Sonnet",
                    "model": "anthropic/claude-3-sonnet",
                    "pricing": {"coins": 5, "words": 100},
                },
                {
                    "name": "Anthropic: Claude 3.5 Sonnet",
                    "model": "anthropic/claude-3.5-sonnet",
                    "pricing": {"coins": 5, "words": 100},
                },
                {
                    "name": "Cohere: Command R+",
                    "model": "cohere/command-r-plus",
                    "pricing": {"coins": 4, "words": 100},
                },
                {
                    "name": "Dolphin 2.6 Mixtral 8x7B",
                    "model": "cognitivecomputations/dolphin-mixtral-8x7b",
                    "pricing": {"coins": 1, "words": 100},
                },
                {
                    "name": "Goliath 120B",
                    "model": "alpindale/goliath-120b",
                    "pricing": {"coins": 5, "words": 100},
                },
                {
                    "name": "Google: Gemini Pro 1.5",
                    "model": "google/gemini-pro-1.5",
                    "pricing": {"coins": 3, "words": 100},
                },
                {
                    "name": "Gryphe: MythoMax L2 13B 8k",
                    "model": "gryphe/mythomax-l2-13b-8k",
                    "pricing": {"coins": 1, "words": 100},
                },
                {
                    "name": "Meta: Llama 3 70B Instruct (nitro)",
                    "model": "meta-llama/llama-3-70b-instruct:nitro",
                    "pricing": {"coins": 1, "words": 100},
                },
                {
                    "name": "Meta: Llama 3 8B Instruct",
                    "model": "meta-llama/llama-3-8b-instruct",
                    "pricing": {"coins": 0.5, "words": 100},
                },
                {
                    "name": "Mistral: Large",
                    "model": "mistralai/mistral-large",
                    "pricing": {"coins": 8, "words": 100},
                },
                {
                    "name": "Mistral: Mixtral 8x7B",
                    "model": "mistralai/mixtral-8x7b-instruct",
                    "pricing": {"coins": 1, "words": 100},
                },
                {
                    "name": "OpenAI: GPT-3.5 Turbo 16k",
                    "model": "openai/gpt-3.5-turbo-0125",
                    "pricing": {"coins": 1, "words": 100},
                },
                {
                    "name": "OpenAI: GPT-4",
                    "model": "openai/gpt-4",
                    "pricing": {"coins": 20, "words": 100},
                },
                {
                    "name": "OpenAI: GPT-4 Turbo 128k - New (April 9)",
                    "model": "openai/gpt-4-turbo-2024-04-09",
                    "pricing": {"coins": 8, "words": 100},
                },
                {
                    "name": "OpenAI: GPT-4 Turbo 128k - Old",
                    "model": "openai/gpt-4-0125-preview",
                    "pricing": {"coins": 8, "words": 100},
                },
                {
                    "name": "OpenAI: GPT-4 Vision",
                    "model": "openai/gpt-4-vision-preview",
                    "pricing": {"coins": 10, "words": 100},
                },
                {
                    "name": "OpenAI: GPT-4o",
                    "model": "openai/gpt-4o",
                    "pricing": {"coins": 4, "words": 100},
                },
                {
                    "name": "Perplexity: Llama3 Sonar 70B Online",
                    "model": "perplexity/llama-3-sonar-large-32k-online",
                    "pricing": {"coins": 1, "words": 100},
                },
                {
                    "name": "Perplexity: Llama3 Sonar 8B Online",
                    "model": "perplexity/llama-3-sonar-small-32k-online",
                    "pricing": {"coins": 1, "words": 100},
                },
                {
                    "name": "Qwen 2 72B Instruct",
                    "model": "qwen/qwen-2-72b-instruct",
                    "pricing": {"coins": 0.5, "words": 100},
                },
            ]
        },
        "success": True,
    }


def user_detail():
    return {
        "data": {
            "first_name": "Test",
            "last_name": "User",
            "coins": 999999.99,
            "plan": "Diamond Pack",
        },
        "success": True,
    }
