import openai
import os

# Print the API key to confirm it's being loaded correctly
print("API Key loaded:", os.getenv("OPENAI_API_KEY"))

openai.api_key = os.getenv("OPENAI_API_KEY")
def safety_check(user_text):
    """
    Detect unsafe medical questions before answering.
    """

    prompt = f"""
    Determine if the following user message is medically unsafe.
    Unsafe includes:
    - Asking for diagnosis
    - Asking for medication dosages
    - Asking for prescription drugs
    - Emergency symptoms (chest pain, difficulty breathing)
    - Self-harm or harm to others

    Respond with ONLY "safe" or "unsafe".

    User message:
    "{user_text}"
    """

    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Classify medical safety."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=20
    )

    verdict = response.choices[0].message.content.lower().strip()
    return verdict
