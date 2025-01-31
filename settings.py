import os
from paperqa import Settings

class SettingsManager:
    def __init__(self, llm_type: str, ollama_model: str):
        """
        Initialize settings for PaperQA based on the selected LLM type.

        :param llm_type: "gpt" for OpenAI models, "ollama" for local models.
        :param ollama_model: Custom model name for Ollama. Defaults to DeepSeek-R1-Distill-Qwen-7B-GGUF:Q6_K.
        """
        self.llm_type = llm_type.lower()
        self.ollama_model = ollama_model

        if self.llm_type == "gpt":
            self.settings = self._setup_gpt_settings()
        elif self.llm_type == "ollama":
            self.settings = self._setup_ollama_settings()
        else:
            raise ValueError(f"Invalid LLM type: {llm_type}. Choose 'gpt' or 'ollama'.")

    def _setup_gpt_settings(self):
        """
        Set up PaperQA settings for GPT models using the OpenAI API.
        Assumes the API key is set in the environment variable OPENAI_API_KEY.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY is not set in the environment.")

        return Settings()  # PaperQA defaults to OpenAI, so no extra config needed

    def _setup_ollama_settings(self):
        """
        Set up PaperQA settings for a local model running with Ollama.
        Allows selecting a custom model.
        """
        local_llm_config = {
            "model_list": [
                {
                    "model_name": self.ollama_model,
                    "litellm_params": {
                        "model": self.ollama_model,
                        "api_base": "http://localhost:11434",
                    },
                }
            ]
        }

        return Settings(
            llm=self.ollama_model,
            llm_config=local_llm_config,
            summary_llm=self.ollama_model,
            summary_llm_config=local_llm_config,
            embedding=self.ollama_model,
        )

    def get_settings(self):
        """Return the configured PaperQA settings object."""
        return self.settings
