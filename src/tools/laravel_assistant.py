import os
import datetime
import traceback
from fastmcp import FastMCP
from src.core.rag_service import RAGService
from src.core.database import SessionLocal
from src.core.models import Conversation
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Create a new, dedicated FastMCP instance for this tool
assistant_app = FastMCP(name="LaravelAssistantService")

# This requires the OPENAI_API_KEY environment variable to be set.
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY environment variable not set. The AI assistant will not work.")

# Initialize the RAG service and LLM once when the module is loaded.
rag_service = RAGService()
try:
    llm = ChatOpenAI(model="gpt-4o") # Using a powerful model for better code generation
except Exception as e:
    print(f"Could not initialize ChatOpenAI: {e}")
    llm = None

# Define the prompt template
template = """
You are an expert AI assistant specializing in Laravel 5.6.

Your primary goal is to help developers solve their problems. Analyze the user's question and the provided context to give the best possible answer.

**If the user's question appears to be an error message or a request for debugging:**
1.  Analyze the error message and any provided code.
2.  Identify the most likely cause of the error.
3.  Provide a clear explanation of the cause and a step-by-step solution.
4.  If the documentation context is relevant, use it to support your explanation.

**For all other questions (code generation, concepts, etc.):**
1.  Answer the user's question based *only* on the following context from the official Laravel 5.6 documentation.
2.  Provide concise, accurate, and helpful code examples where appropriate.
3.  If the answer cannot be found in the context, state that you do not have enough information from the provided documentation.

**General Rules:**
- Do not mention the context in your response. Just answer the question directly.
- Be friendly and supportive.

Context from documentation:
---
{context}
---

User's Question:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    """Helper function to format retrieved documents into a string."""
    return "\n\n---\n\n".join([d.page_content for d in docs])

# Create the RAG chain using LCEL
rag_chain = (
    {"context": lambda x: format_docs(rag_service.find_relevant_documents(x["question"])), "question": itemgetter("question")}
    | prompt
    | llm
    | StrOutputParser()
)

@assistant_app.tool()
def laravel_5_6_assistant(query: str, user_id: str = "default_user", session_id: str = "default_session") -> str:
    """
    An AI agent that provides coding assistance for Laravel 5.6.
    It can answer questions, debug code, and provide code examples
    by retrieving information from the official documentation.
    """
    if not query:
        return "Please provide a query."
    
    if not llm or not os.getenv("OPENAI_API_KEY"):
        return "Error: The AI model is not configured on the server. Please set the OPENAI_API_KEY."

    if rag_service.vector_store is None:
        return "Error: The documentation vector store is not loaded. Please check the server logs."

    db = SessionLocal()
    try:
        # Invoke the RAG chain with the user's query
        response_text = rag_chain.invoke({"question": query})

        # Log the conversation to the database
        conversation_log = Conversation(
            session_id=session_id,
            user_id=user_id,
            query_text=query,
            response_text=response_text,
            response_timestamp=datetime.datetime.utcnow(),
            source_references="", # Placeholder for now
        )
        db.add(conversation_log)
        db.commit()

        return response_text
    except Exception as e:
        print(f"An error occurred while processing the query: {e}")
        traceback.print_exc()
        db.rollback()
        return "Sorry, an error occurred while processing your request."
    finally:
        db.close()