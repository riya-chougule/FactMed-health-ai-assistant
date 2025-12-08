from core.extract_medical_terms import extract_medical_terms
import openai
from duckduckgo_search import DDGS
from Bio import Entrez
import requests
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question):
    """
    Generate a medically safe answer for a user question and fetch trusted citations.
    """

    # Step 1: Extract medical terms from the question
    terms = extract_medical_terms(question)

    # Step 2: Fetch relevant citations from PubMed
    citations = []
    Entrez.email = "your_email@example.com"  # required by NCBI
    for term in terms:
        try:
            handle = Entrez.esearch(db="pubmed", term=term, retmax=3)
            record = Entrez.read(handle)
            handle.close()
            ids = record["IdList"]
            for pid in ids:
                citations.append(f"https://pubmed.ncbi.nlm.nih.gov/{pid}/")
        except Exception as e:
            continue

    # Step 3: Generate AI answer
    prompt = f"""
    You are a reliable medical AI. Provide a clear, concise, and safe explanation for:
    {question}
    Use verified medical sources only.
    """
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a trusted medical assistant AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=400
    )

    answer_text = response.choices[0].message.content

    return {
        "answer": answer_text,
        "citations": citations
    }
