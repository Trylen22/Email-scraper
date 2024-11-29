import subprocess

class LocalModel:
    def __init__(self, model_name="mistral"):
        """
        Initialize the LocalModel instance with the specified model name.
        Ensure the Mistral model is installed and accessible via Ollama.
        
        Args:
            model_name (str): The name of the model to use (default: "mistral").
        """
        self.model_name = model_name

    def summarize(self, text):
        """
        Generate a summary for the provided text using the Mistral model via Ollama.
        
        Args:
            text (str): The input text to summarize.

        Returns:
            str: The generated summary or an error message if something goes wrong.
        """
        prompt = f"Summarize the following text:\n{text}"
        
        try:
            # Run the Ollama command via subprocess, passing the prompt as stdin
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,  # Pass the prompt as standard input
                text=True,  # Ensure text mode for inputs/outputs
                capture_output=True  # Capture both stdout and stderr
            )
            
            # Check for errors during subprocess execution
            if result.returncode != 0:
                error_message = result.stderr.strip()
                print(f"Error in calling Ollama:\n{error_message}")
                return f"Error in generating summary: {error_message}"
            
            # Return the raw output as the summary
            return result.stdout.strip()

        except FileNotFoundError:
            return "Error: Ollama command not found. Ensure Ollama is installed and in your PATH."
        except Exception as e:
            print(f"Unexpected error occurred: {str(e)}")
            return f"Error in generating summary: {str(e)}"


# Example usage
if __name__ == "__main__":
    model = LocalModel("mistral")
    sample_text = "Machine learning models are a subset of artificial intelligence that focus on training algorithms to learn from data."
    summary = model.summarize(sample_text)
    print(f"Summary:\n{summary}")
