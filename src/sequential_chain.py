from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge", "xyz-200.txt")
CHAT_HISTORY_PATH = os.path.join(BASE_DIR, "history", "chat.txt")

def main():
    load_dotenv()

    customer_question = "Sim, já verifiquei os assentos não tem sinal de desgastes e estão bem fixados"
    
    # loading the knowledge base and chat history
    knowledge = TextLoader(file_path=KNOWLEGE_BASE_PATH, encoding="utf-8").load()
    chat_history = TextLoader(file_path=CHAT_HISTORY_PATH, encoding="utf-8").load()    
    
    # Instantiating the llm model
    openai = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_CHAT"),
        max_completion_tokens=300,
        temperature=0
    )

    # Build a prompt for knoledge base
    prompt_knoledge_base = PromptTemplate(
        input_variables=["context", "question"],
        template="""
            Use o seguinte contexto para responder à pergunta.
            Seja técnico.
            Responda apenas com base nas informações fornecidas;
            Não forneça instruções de procedimentos já realizados;
            Não utilize informações externas ao contexto;
            Contexto: {context}
            Pergunta: {question}
        """
    )

    chat_history = PromptTemplate(
        input_variables=["chat_history", "question"],
        template="""
            Use o seguinte contexto para responder à pergunta.
            Seja técnico.
            Responda apenas com base nas informações fornecidas;
            Não forneça instruções de procedimentos já realizados;
            Não utilize informações externas ao contexto;
            Histórico: {chat_history}
            Pergunta: {question}
        """
    )

    final_prompt = PromptTemplate(
        input_variables=["knowledge_base_response", "chat_history_response"],
        template="""
            Seja técnico.
            Combine as seguintes respostas para gerar uma resposta final ao usuário,
            mas não forneça instruções de procedimentos já realizados anteriormente pelo usuário.
            Resposta Base de Conhecimentos: {knowledge_base_response}
            Histórico da conversa: {chat_history_response}
        """
    )

    # chainning
    chain_base_knowlegde = prompt_knoledge_base | openai
    chain_chat_history = chat_history | openai
    final_chain = final_prompt | openai

    knowledge_base_response = chain_base_knowlegde.invoke({"context": knowledge, "question": customer_question})
    chat_history_response = chain_chat_history.invoke({"chat_history": chat_history, "question": customer_question})
    final_result = final_chain.invoke({"knowledge_base_response": knowledge_base_response.content, "chat_history_response": chat_history_response})

    print(final_result.content)


if __name__ == '__main__':
    main()