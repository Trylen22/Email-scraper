import subprocess

class LocalModel:
    def __init__(self, model_name="deepseek-r1:1.5b"):
        """
        Initialize the LocalModel instance with the specified model name.
        Ensure the Mistral model is installed and accessible via Ollama.
        
        Args:
            model_name (str): The name of the model to use (default: "mistral").
        """
        self.model_name = model_name

    def summarize(self, text):
        """Generate a concise, focused summary for the provided text."""
        prompt = f"""Summarize this email in one clear sentence, focusing only on the main point or action required:

Email:
{text}

Guidelines:
- Use 20 words or less
- Focus on the key message or action
- Omit redundant details
- Don't repeat URLs or contact information
- Don't use phrases like "Key Details" or "Action Items"

Reply with just the summary."""
        
        try:
            # Run Ollama command
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,
                text=True,
                capture_output=True
            )
            
            if result.returncode != 0:
                return f"Error in generating summary: {result.stderr.strip()}"
            
            # Clean up the summary
            summary = result.stdout.strip()
            if "Summary:" in summary:
                summary = summary.split("Summary:")[-1].strip()
            
            return summary

        except FileNotFoundError:
            return "Error: Ollama command not found. Ensure Ollama is installed and in your PATH."
        except Exception as e:
            print(f"Unexpected error occurred: {str(e)}")
            return f"Error in generating summary: {str(e)}"

    def __call__(self, text):
        """Convenience method to allow direct calling of instance."""
        return self.summarize(text)


# Example usage
if __name__ == "__main__":
    model = LocalModel("mistral")
    sample_text = "Machine learning models are a subset of artificial intelligence that focus on training algorithms to learn from data."
    summary = model.summarize(sample_text)
    print(f"Summary:\n{summary}")
