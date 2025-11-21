import os
from langchain_core.globals import set_llm_cache
from langchain_community.cache import RedisCache, InMemoryCache
from redis import Redis


def init_model_cache():
    """
        Function responsible to set llm cache.
        If a redis host is provided through env variable, it will use redis based cache, otherwise will use in memory based cache.
    """
    redis_host = os.getenv("REDIS_HOST")

    if not redis_host:
        print("Using InMemoryCache")
        
        set_llm_cache(InMemoryCache())
        return
    
    
    print("Using RedisCache")
    redis = Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT")
    )

    set_llm_cache(RedisCache(
        redis_= redis,
        ttl=45
    ))
      