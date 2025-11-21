from dotenv import load_dotenv
from redis import Redis
import os

load_dotenv()

def main():
    redis = Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=os.getenv("REDIS_PORT", 6379),
        decode_responses=True
    )

    redis.set("key_1", "some value")

    item = redis.get("key_1")

    print(item)


if __name__ == "__main__":
    main()
