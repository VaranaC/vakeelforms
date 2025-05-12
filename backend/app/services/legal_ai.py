import requests

async def get_legal_explanation(text: str):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/nbroad/tiny-random-bert",
            headers={"Content-Type": "application/json"},
            json={"inputs": f"Explain this legal text: {text}"}
        )

        result = response.json()

        # ✅ Handle list response
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "✅ Flow works — dummy explanation.")

        # ✅ Handle error dict
        elif isinstance(result, dict) and "error" in result:
            return f"⚠️ AI Error: {result['error']}"

        return "⚠️ Unexpected response from AI model."

    except Exception as e:
        return f"🚨 Exception during AI call: {str(e)}"
