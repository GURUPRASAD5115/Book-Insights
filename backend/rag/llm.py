import os
import logging
import json
import re
import requests
import google.generativeai as genai

logger = logging.getLogger(__name__)

# -----------------------------
# GEMINI CONFIG
# -----------------------------
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    logger.warning("⚠️ GEMINI_API_KEY not found")


class LLMManager:
    def __init__(self):
        # 🔹 LOCAL (OLLAMA)
        self.ollama_url = "http://localhost:11434/api/generate"
        self.local_model = os.getenv("LOCAL_LLM_MODEL", "llama3")

        # 🔹 GEMINI
        self.model_name = os.getenv("LLM_MODEL", "gemini-1.5-flash")

        try:
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"✅ Gemini initialized: {self.model_name}")
        except Exception as e:
            logger.error(f"❌ Gemini init error: {e}")
            self.model = None

    # -----------------------------
    # 🔥 OLLAMA CALL
    # -----------------------------
    def _ollama(self, prompt):
        try:
            res = requests.post(
                self.ollama_url,
                json={
                    "model": self.local_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=20
            )

            if res.status_code == 200:
                return res.json().get("response", "").strip()

        except Exception as e:
            logger.warning(f"Ollama error: {e}")

        return None

    # -----------------------------
    # GEMINI CALL
    # -----------------------------
    def _gemini(self, prompt):
        try:
            if not self.model:
                return None

            response = self.model.generate_content(prompt)
            return self._get_text(response)

        except Exception as e:
            logger.warning(f"Gemini error: {e}")
            return None

    # -----------------------------
    # SMART ROUTER (KEY PART)
    # -----------------------------
    def _ask(self, prompt):
        # 1️⃣ TRY OLLAMA FIRST
        result = self._ollama(prompt)

        if self._is_good(result):
            logger.info("✅ Answer from OLLAMA")
            return result

        # 2️⃣ FALLBACK TO GEMINI
        result = self._gemini(prompt)

        if self._is_good(result):
            logger.info("✅ Answer from GEMINI")
            return result

        return "⚠️ No valid AI response"

    # -----------------------------
    # CHECK RESPONSE QUALITY
    # -----------------------------
    def _is_good(self, text):
        if not text:
            return False

        bad = [
            "i don't know",
            "not enough information",
            "cannot answer",
            "no context"
        ]

        t = text.lower()
        return not any(b in t for b in bad)

    # -----------------------------
    # SAFE TEXT
    # -----------------------------
    def _get_text(self, response):
        try:
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
            return ""
        except:
            return ""

    # -----------------------------
    # SUMMARY
    # -----------------------------
    def generate_summary(self, text):
        prompt = f"Summarize this book in 2-3 sentences:\n{text}"
        return self._ask(prompt)

    # -----------------------------
    # GENRES
    # -----------------------------
    def classify_genres(self, text):
        prompt = f"""
Return ONLY JSON list of genres.

{text}
"""
        result = self._ask(prompt)

        try:
            return json.loads(result)
        except:
            cleaned = re.sub(r'[\[\]\n]', '', result)
            return [g.strip() for g in cleaned.split(",") if g.strip()]

    # -----------------------------
    # SENTIMENT
    # -----------------------------
    def analyze_sentiment(self, text):
        prompt = f"""
Return ONLY one word: positive, neutral, or negative.

{text}
"""
        result = self._ask(prompt).lower()

        if result in ["positive", "negative", "neutral"]:
            return result

        return "neutral"

    # -----------------------------
    # Q&A
    # -----------------------------
    def generate_answer(self, context, question):
        prompt = f"""
Answer using context only.
Be short and relevant.
Do NOT repeat full text.

Context:
{context}

Question:
{question}
"""
        return self._ask(prompt)