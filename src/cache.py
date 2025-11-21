import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from src.llm_cache.cache import init_model_cache


def main():
    
    """
        Function responsible to instantiate a openai model to interact with.
    """
    load_dotenv()
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
