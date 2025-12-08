# core/prompt_optimizer.py

def optimize_prompt(user_input):
    """
    Enhance user input for safety and clarity.
    Adds instructions for citations and medical safety.
    """
    optimized_prompt = f"""
    Provide a medically-informed answer to this question: "{user_input}".
    DO NOT give personal prescriptions or advice.
    Always cite credible sources (CDC, WHO, NIH, PubMed).
    Structure your answer as:
    1. Claims / key points
    2. Supporting citations
    3. Confidence notes
    """
    return optimized_prompt
