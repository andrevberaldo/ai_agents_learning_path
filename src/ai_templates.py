
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from src.cache import init_model_cache


def main():
    load_dotenv()
    init_model_cache()

    historical_character = "Ayrton Senna"
    language = "pt-BR"

    template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "Your are a historic teacher that has greate ability to make summaries"
        ),
        HumanMessagePromptTemplate.from_template(
            "Write a short summary about {historical_character} in {language}"
        )
    ])

    prompt = template.format(historical_character=historical_character, language=language)

    openai = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_CHAT"),
        max_tokens=150
    )

    response = openai.invoke(input=prompt)

    print(response.content)


if __name__ == "__main__":
    main()