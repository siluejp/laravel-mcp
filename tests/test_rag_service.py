import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path to allow imports from 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.rag_service import RAGService

class TestRAGService(unittest.TestCase):

    @patch('src.core.rag_service.HuggingFaceEmbeddings')
    @patch('src.core.rag_service.FAISS')
    def test_initialization_successful(self, mock_faiss, mock_embeddings):
        """
        Test that the RAGService initializes correctly when the FAISS index exists.
        """
        # Arrange
        mock_faiss.load_local.return_value = MagicMock()
        
        # Act
        rag_service = RAGService()
        
        # Assert
        self.assertIsNotNone(rag_service.vector_store)
        mock_faiss.load_local.assert_called_once()
        mock_embeddings.assert_called_once()

    @patch('src.core.rag_service.HuggingFaceEmbeddings')
    @patch('src.core.rag_service.FAISS')
    def test_initialization_fails(self, mock_faiss, mock_embeddings):
        """
        Test that the RAGService handles the case where the FAISS index is not found.
        """
        # Arrange
        mock_faiss.load_local.side_effect = Exception("File not found")
        
        # Act
        rag_service = RAGService()
        
        # Assert
        self.assertIsNone(rag_service.vector_store)

    @patch('src.core.rag_service.HuggingFaceEmbeddings')
    @patch('src.core.rag_service.FAISS')
    def test_find_relevant_documents(self, mock_faiss, mock_embeddings):
        """
        Test the document search functionality.
        """
        # Arrange
        mock_vector_store = MagicMock()
        mock_vector_store.similarity_search.return_value = ["doc1", "doc2"]
        mock_faiss.load_local.return_value = mock_vector_store
        
        rag_service = RAGService()
        
        # Act
        results = rag_service.find_relevant_documents("test query")
        
        # Assert
        self.assertEqual(len(results), 2)
        mock_vector_store.similarity_search.assert_called_once_with("test query", k=5)

if __name__ == '__main__':
    unittest.main()
