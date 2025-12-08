import re

def self_audit(answer_text):
    """
    Lightweight auditing system to detect medical danger,
    hallucinations, unsupported claims, and unsafe advice.
    """

    unsupported_claims = []
    safety_flags = []

    # ---- 1. Detect dangerous medical advice ----
    unsafe_patterns = [
        r"\btake\b.*\bmg\b",
        r"\bdosage\b",
        r"\bprescribe\b",
        r"\bself medicate\b",
        r"\bantibiotic\b.*\bwithout\b",
        r"\bstop your medication\b",
        r"\bstop taking\b",
        r"\bignore\b.*\bsymptom\b",
        r"\bno need to see a doctor\b"
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, answer_text, re.IGNORECASE):
            safety_flags.append("Possible unsafe medical advice detected")

    # ---- 2. Detect absolute claims (“always”, “guaranteed”, etc.) ----
    absolute_terms = ["always", "never", "guaranteed", "certainly", "cure"]
    if any(word in answer_text.lower() for word in absolute_terms):
        unsupported_claims.append("Overconfident or absolute claim detected")

    # ---- 3. Determine safety ----
    is_safe = len(safety_flags) == 0

    # ---- 4. Confidence score ----
    confidence_score = 100 if is_safe else 60

    return {
        "unsupported_claims": unsupported_claims,
        "safety_flags": safety_flags,
        "is_safe": is_safe,
        "confidence_score": confidence_score
    }
