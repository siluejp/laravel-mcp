from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main():
    """
    Downloads and caches the sentence-transformer model from Hugging Face.
    """
    print(f"Downloading and caching model: {MODEL_NAME}")
    try:
        # This line will download the model to the local cache if it's not there.
        SentenceTransformer(MODEL_NAME)
        print("Model downloaded and cached successfully.")
        print("You can now try using the Codex assistant again.")
    except Exception as e:
        print(f"An error occurred while downloading the model: {e}")
        print("Please ensure you have an active internet connection and can reach huggingface.co")

if __name__ == "__main__":
    main()
