import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path to allow imports from 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the tool directly
from src.tools.laravel_assistant import laravel_5_6_assistant


class TestLaravelAssistant(unittest.TestCase):

    @patch('src.tools.laravel_assistant.SessionLocal')
    @patch('src.tools.laravel_assistant.rag_chain')
    @patch('os.getenv')
    def test_successful_query(self, mock_getenv, mock_rag_chain, mock_session_local):
        """
        Test a successful query through the tool.
        """
        # Arrange
        mock_getenv.return_value = "fake-api-key"
        mock_rag_chain.invoke.return_value = "This is the AI response."
        mock_db_session = MagicMock()
        mock_session_local.return_value = mock_db_session
        
        # Act
        response = laravel_5_6_assistant.fn(query="test query")
        
        # Assert
        self.assertEqual(response, "This is the AI response.")
        mock_rag_chain.invoke.assert_called_once_with({"question": "test query"})
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.close.assert_called_once()

    def test_empty_query(self):
        """
        Test that the tool returns an error for an empty query.
        """
        # Act
        response = laravel_5_6_assistant.fn(query="")
        
        # Assert
        self.assertEqual(response, "Please provide a query.")

    @patch('os.getenv', return_value=None)
    def test_no_api_key(self, mock_getenv):
        """
        Test that the tool returns an error if the OpenAI API key is not set.
        """
        # Act
        response = laravel_5_6_assistant.fn(query="test query")
        
        # Assert
        expected_error = (
            "Error: The AI model is not configured on the server. "
            "Please set the OPENAI_API_KEY."
        )
        self.assertEqual(response, expected_error)

if __name__ == '__main__':
    unittest.main()