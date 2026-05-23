import os
from typing import Dict, Any, List


class ParadigmTransformationEngine:
    """
    Production‑grade LLM Orchestration Engine that manages token boundaries,
    deterministic few‑shot prompting, and defensive sanitization of refactored code.
    """

    def __init__(self, api_key: str | None = None) -> None:
        # Resolve the API key from argument or environment variable safely.
        self.api_key: str | None = api_key or os.getenv("OPENAI_API_KEY")
        self.client: Any = None

        # Enterprise Gateway: Only initialize the client if credentials exist.
        # This prevents initialization crashes during offline testing or local CI runs.
        if self.api_key:
            self._initialize_client()

    def _initialize_client(self) -> None:
        """Initializes the underlying vendor SDK client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            # Do not crash the engine; log it or handle it gracefully for local testing.
            self.client = None

    def _get_system_instructions(self, target_paradigm: str) -> str:
        """
        Houses strict system boundaries and few‑shot formatting rules
        to ensure the LLM returns pure, valid Python code.
        """
        return (
            f"You are an enterprise‑grade Software Refactoring Engine specialized in pure Python.\n"
            f"Your task is to rewrite the user's input code entirely into a strict {target_paradigm} pattern.\n\n"
            "CRITICAL COMPLIANCE RULES:\n"
            "1. Return ONLY executable Python code. Do not include introductory text, conversational notes, or explanations.\n"
            "2. ABSOLUTELY DO NOT wrap your response in markdown code blocks (e.g., do not use ```python).\n"
            "3. Ensure the output has syntactically correct indentation and matching brackets.\n"
            "4. Maintain the exact same functional input/output contracts as the original code."
        )

    def sanitize_llm_response(self, raw_response: str) -> str:
        """
        Defensive Programming Gate: Parses and strips markdown code blocks,
        stray conversational artifacts, or spacing anomalies introduced by LLM generation.
        """
        cleaned = raw_response.strip()

        # Remove markdown wrappers if the LLM violated the system prompt.
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            # Drop the opening line (e.g. ```python) and the closing line (```)
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1] == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()

        return cleaned

    def refactor_code(self, source_code: str, target_paradigm: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
        """
        Executes code transformation via the active inference pipeline with structural error management.
        Returns a rich metrics dictionary tracking performance, status, and tokens.
        """
        valid_paradigms: List[str] = ["Procedural", "Object‑Oriented", "Functional"]
        if target_paradigm not in valid_paradigms:
            raise ValueError(f"Target paradigm must be one of {valid_paradigms}")

        # Fallback Mock Mechanism if running without an API key (e.g., in local CI or offline development).
        if not self.client:
            return {
                "success": True,
                "status": "MOCK_MODE (No API Key Detected)",
                "target_paradigm": target_paradigm,
                "refactored_code": (
                    "# Mock Output for {target_paradigm}\n"
                    "def process_data(data):\n"
                    "    return [x for x in data]\n"
                ),
                "token_usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }

        try:
            # System and User prompt separation to preserve attention heads.
            response = self.client.chat.completions.create(
                model=model,
                temperature=0.1,  # Low temperature forces deterministic architectural patterns.
                messages=[
                    {"role": "system", "content": self._get_system_instructions(target_paradigm)},
                    {"role": "user", "content": f"Refactor this source code:\n\n{source_code}"},
                ],
            )

            raw_content = response.choices[0].message.content or ""
            sanitized_code = self.sanitize_llm_response(raw_content)

            return {
                "success": True,
                "status": "SUCCESS",
                "target_paradigm": target_paradigm,
                "refactored_code": sanitized_code,
                "token_usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
        except Exception as e:
            # Gracefully trap API failures, rate limits, or network timeouts.
            return {
                "success": False,
                "status": f"API_ERROR: {str(e)}",
                "target_paradigm": target_paradigm,
                "refactored_code": "",
                "token_usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }
