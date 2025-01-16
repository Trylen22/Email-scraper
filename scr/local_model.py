import subprocess

class LocalModel:
    def __init__(self, model_name="tinyllama"):
        """
        Initialize the LocalModel instance with the specified model name.
        Ensure the Mistral model is installed and accessible via Ollama.
        
        Args:
            model_name (str): The name of the model to use (default: "mistral").
        """
        self.model_name = model_name

    def summarize(self, text):
        """Generate a summary for the provided text using the model via Ollama."""
        print(f"\nUsing model: {self.model_name}")  # Debug print for model name
        
        # Simplified prompt for better results with smaller models
        prompt = f"""Classify this email as HIGH, MEDIUM, or LOW priority:
HIGH = urgent deadlines, grades, required actions
MEDIUM = course materials, office hours
LOW = general info, optional events

Email:
{text}

Reply with priority in brackets, then a brief summary in one sentence."""
        
        try:
            # Run Ollama command
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,
                text=True,
                capture_output=True
            )
            
            if result.returncode != 0:
                error_message = result.stderr.strip()
                print(f"Error in calling Ollama:\n{error_message}")
                return f"Error in generating summary: {error_message}"
            
            # Clean up and format the summary
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
