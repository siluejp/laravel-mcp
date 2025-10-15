from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_STORE_PATH = "faiss_index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class RAGService:
    def __init__(self):
        """
        Initializes the RAG service by loading the embedding model and the vector store.
        """
        print("Loading RAG service...")
        model_kwargs = {'device': 'cpu'}
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME, model_kwargs=model_kwargs)
        
        try:
            self.vector_store = FAISS.load_local(VECTOR_STORE_PATH, self.embeddings, allow_dangerous_deserialization=True)
            print("FAISS vector store loaded successfully.")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            print("Please ensure you have run the `scripts/ingest_docs.py` script first.")
            self.vector_store = None

    def find_relevant_documents(self, query: str, k: int = 5):
        """
        Finds the top k most relevant documents from the vector store for a given query.
        """
        if self.vector_store is None:
            return []
            
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error during similarity search: {e}")
            return []

# Example usage (for testing)
if __name__ == '__main__':
    rag_service = RAGService()
    if rag_service.vector_store:
        query = "How to use middleware?"
        documents = rag_service.find_relevant_documents(query)
        print(f"Found {len(documents)} relevant documents for query: '{query}'")
        for doc in documents:
            print("-" * 20)
            print(f"Source: {doc.metadata.get('source')}")
            print(doc.page_content[:300] + "...")
