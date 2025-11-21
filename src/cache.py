import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.globals import set_llm_cache
from langchain_community.cache import RedisCache, InMemoryCache
from redis import Redis

load_dotenv()

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
        
    

def main():
    """
        Function responsible to instantiate a openai model to interact with.
    """
    init_model_cache()

    openai = OpenAI(
        model=os.getenv("OPENAI_MODEL_COMPLETION"),
        max_tokens=100
    )

    prompt = "In short words, who were Carl Sagan?"

    response_1 = openai.invoke(input=prompt)

    print(response_1)

    response_2 = openai.invoke(prompt)

    print(response_2)
    
    

if __name__ == "__main__":
    main()
