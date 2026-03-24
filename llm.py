"""LLM service module for the Local AI Telegram Assistant.

This module provides the TinyLLM class, which wraps the llama-cpp-python
library to provide local text generation and summarization capabilities
using a GGUF model.
"""

from llama_cpp import Llama
import os
import logging
from config import MODEL_PATH


class TinyLLM:
    """A singleton class to manage the local LLM instance.

    This class handles loading the model and provides methods for generating
    text and summarizing content.
    """
    _instance = None

    def __new__(cls):
        """Create a new instance of TinyLLM if it doesn't exist (Singleton).

        Returns:
            TinyLLM: The singleton instance of the TinyLLM class.
        """
        if cls._instance is None:
            cls._instance = super(TinyLLM, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.load_model()
        return cls._instance


    def load_model(self):
        """Load the GGUF model from the configured MODEL_PATH.

        If the model file is not found or fails to load, the model attribute
        will be set to None.
        """
        if not os.path.exists(MODEL_PATH):
            print(f"Warning: Model file {MODEL_PATH} not found. LLM disabled.")
            return

        try:
            self.model = Llama(
                model_path=MODEL_PATH,
                n_ctx=768,       # Increased slightly for summaries
                n_threads=max(1, os.cpu_count() - 1), 
                verbose=False,
                n_gpu_layers=0    # Force CPU to save RAM
            )
        except Exception as e:
            print(f"Error loading LLM: {e}")
            self.model = None


    def _sanitize_input(self, text: str):
        """Sanitize input by removing ChatML control tokens.

        Args:
            text (str): The input text to sanitize.

        Returns:
            str: The sanitized text.
        """
        if not text:
            return ""
        # Remove potential prompt injection tokens
        tokens_to_remove = ["<|im_start|>", "<|im_end|>"]
        sanitized = text
        for token in tokens_to_remove:
            sanitized = sanitized.replace(token, "")
        return sanitized


    def generate(self, prompt: str, system_prompt: str = None):
        """Generate a response from the LLM based on a prompt.

        Args:
            prompt (str): The user's input prompt.
            system_prompt (str, optional): An optional system prompt to guide the AI's behavior.
                Defaults to a concise assistant prompt.

        Returns:
            str: The generated text response or an error message.
        """
        if not self.model:
            return "Note: Local AI is disabled because the model file was not found."

        # Sanitize inputs to prevent prompt injection
        prompt = self._sanitize_input(prompt)
        if system_prompt:
            system_prompt = self._sanitize_input(system_prompt)
        else:
            system_prompt = "You are a concise local assistant. Respond in under 30 words."

        full_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        
        try:
            output = self.model(
                full_prompt,
                max_tokens=120,
                stop=["<|im_end|>"],
                echo=False
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            logging.error(f"Error during LLM inference: {e}", exc_info=True)
            return "An error occurred during AI processing. Please try again later."


    def summarize(self, text: str):
        """Summarize the given text using the local LLM.

        Args:
            text (str): The text content to be summarized.

        Returns:
            str: A brief summary of the input text.
        """
        prompt = f"Summarize this briefly: {text}"
        return self.generate(prompt, "You are a summarization tool. Be extremely brief.")


llm_service = TinyLLM()
