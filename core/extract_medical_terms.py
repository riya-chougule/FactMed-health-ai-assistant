# core/extract_medical_terms.py

import openai
import re

# Ensure your OpenAI API key is set in environment variables
# openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_medical_terms(text, max_terms=10):
    """
    Extract relevant medical terms from the provided text.
    Returns a list of unique medical concepts for use in PubMed and trusted-source lookups.
    
    Args:
        text (str): User question or AI answer text
        max_terms (int): Maximum number of medical terms to return
    Returns:
        list[str]: List of medical terms
    """
    
    prompt = f"""
    You are a medical assistant AI. 
    From the following text, extract up to {max_terms} unique medical conditions, diseases, symptoms, lab tests, or relevant clinical terms.
    Output only a comma-separated list of terms, no explanations or extra text.
    
    Text:
    {text}
    """
    
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert medical concept extractor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=200
    )
    
    terms_text = response.choices[0].message.content
    
    # Split by comma and clean
    terms = [t.strip().lower() for t in re.split(r',|\n', terms_text) if t.strip()]
    
    # Deduplicate and limit
    unique_terms = list(dict.fromkeys(terms))[:max_terms]
    
    return unique_terms

# Example usage
if __name__ == "__main__":
    sample_text = "I have red itchy rashes on my palms, and some small bumps."
    medical_terms = extract_medical_terms(sample_text)
    print("Extracted medical terms:", medical_terms)
