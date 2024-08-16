from sentence_transformers import SentenceTransformer
from os import environ

cached_models = {}
cache_embedding_max_size = int(environ.get("EMBEDDING_MODEL_CACHE_SIZE", "5"))


def get_embedding_model(model_name):
    global cached_models
    global cache_embedding_max_size
    if model_name in cached_models:
        return cached_models[model_name]
    else:
        if cache_embedding_max_size <= len(cached_models):
            cached_models.pop(list(cached_models.keys())[0])
        model = SentenceTransformer(model_name, trust_remote_code=True)
        cached_models[model_name] = model
        return model
