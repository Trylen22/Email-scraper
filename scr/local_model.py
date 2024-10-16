import subprocess
import json

class LocalModel:
    def __init__(self, model_name="mistral"):
        """
        Initialize the model with the specified name.
        Ensure the Mistral model is already installed and configured via Ollama.
        """
        self.model_name = model_name

    def summarize(self, text):
        """
        Uses the Mistral model to generate a summary for the given text.
        
        Args:
            text (str): The text to summarize.

        Returns:
            str: The generated summary.
        """
        prompt = f"Summarize the following text: {text}"
        
        # Use subprocess to run the ollama command with the prompt.
        try:
            result = subprocess.run(
                ["ollama", "generate", self.model_name, "--prompt", prompt],
                text=True,
                capture_output=True
            )
            
            # Check for errors in the subprocess execution
            if result.returncode != 0:
                print(f"Error in calling ollama: {result.stderr}")
                return "Error in generating summary."
            
            # Parse the JSON response if necessary
            output = result.stdout
            try:
                response = json.loads(output)
                return response.get("text", "No summary generated.")
            except json.JSONDecodeError:
                return output

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "Error in generating summary."

# Example usage:
# if __name__ == "__main__":
#     model = LocalModel("mistral")
#     sample_text = "Here is some long text that you want to summarize..."
#     summary = model.summarize(sample_text)
#     print(summary)
