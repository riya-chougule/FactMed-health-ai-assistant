import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from core.answer_generator import generate_answer
from core.safety_filter import safety_check
from core.self_audit import self_audit
from core.extract_medical_terms import extract_medical_terms

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="FactMed", page_icon="🩺", layout="centered")

# -------------------------------
# Top banner image (adjust width and height)
# -------------------------------
img_url = 'https://res.cloudinary.com/jerrick/image/upload/v1717096211/6658cf138e8c7d001ef9e598.jpg'

# Fetch image from URL
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))

# Resize image (you can change these dimensions)
img = img.resize((850, 370))  # Width=850px, Height=370px

# Display the resized image in Streamlit
st.image(img)

# -------------------------------
# Title & subtitle (centered below the image)
# -------------------------------
st.markdown("""
    <h1 style="text-align: center; font-size: 3em; color: Green;">🩺 FactMed 🩺</h1>
    <h3 style="text-align: center; color: white;">Reliable AI for Health Information</h3>
""", unsafe_allow_html=True)

# -------------------------------
# Session state (ensure keys exist before the widget)
# -------------------------------
if "question_input" not in st.session_state:
    st.session_state.question_input = ""
if "user_question" not in st.session_state:
    st.session_state.user_question = ""

# -------------------------------
# Input box
# -------------------------------
question_input = st.text_input(
    "Enter your health question:", 
    value=st.session_state.question_input
)

# -------------------------------
# Buttons (making them bigger and colorful)
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <style>
            .big-button {
                background-color: #4CAF50; /* Green */
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: 0.3s;
            }
            .big-button:hover {
                background-color: #45a049;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Create a bigger, colorful "Submit" button
    submit_button = st.button("Submit", key="submit_button", help="Submit your question", use_container_width=True)
    if submit_button:
        # Save the input to session state
        st.session_state.user_question = question_input

with col2:
    st.markdown("""
        <style>
            .clear-button {
                background-color: #FF5733; /* Red */
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: 0.3s;
            }
            .clear-button:hover {
                background-color: #e74c3c;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Create a bigger, colorful "Clear" button
    clear_button = st.button("Clear", key="clear_button", help="Clear the input fields", use_container_width=True)
    if clear_button:
        # Clear session state
        st.session_state.question_input = ""
        st.session_state.user_question = ""

# -------------------------------
# Process question if submitted
# -------------------------------
if st.session_state.user_question:
    # STEP 1: Safety Filter
    with st.spinner("Running medical safety screening..."):
        verdict = safety_check(st.session_state.user_question)

    if verdict == "unsafe":
        st.error("""
        ⚠️ **This question requires professional medical attention.**
        FactMed cannot answer questions involving:
        - Emergency symptoms  
        - Requests for specific medication/dosage  
        - Diagnoses of severe or dangerous conditions  
        - Self-harm or crisis situations  
        Please contact a healthcare provider immediately.
        """)
        st.stop()

    # STEP 2: Generate Answer
    with st.spinner("Generating medically verified answer and fetching trusted sources..."):
        result = generate_answer(st.session_state.user_question)

    # -------------------------------
    # Display Answer
    # -------------------------------
    st.subheader("✅ Answer")
    st.write(result["answer"])

    # -------------------------------
    # Verified Citations / Trusted Pages
    # -------------------------------
    st.subheader("📚 Verified Citations / Trusted Pages")
    if len(result["citations"]) == 0:
        st.write("No verified citations available.")
    else:
        for url in result["citations"]:
            st.markdown(f"- <{url}>", unsafe_allow_html=True)

    # -------------------------------
    # Self-Audit Report
    # -------------------------------
    st.subheader("📝 Self-Audit Report")
    with st.spinner("Performing self-audit..."):
        audit = self_audit(result["answer"])

    st.json(audit)
    if not audit.get("is_safe", True):
        st.error("⚠️ The system flagged this answer as potentially unsafe.")
