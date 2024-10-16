from local_model import LocalModel

def generate_summary(processed_data):
    """Generates a summary of the processed email data using the Mistral model."""
    model = LocalModel("mistral")  # Use the name configured for Mistral in your Ollama setup
    
    # Combine email content into a single text block
    content = " ".join(email["body"] for email in processed_data)
    
    # Generate summary using the model
    summary = model.summarize(content)
    
    return summary
