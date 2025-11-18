import streamlit as st
from models.text_model import load_text_model
from models.speech_model import load_speech_model
from services.nlp_extractor import extract_drug_info
from services.interaction_checker import check_interactions
from services.dosage_recommender import get_dosage
from services.alternatives_services import get_alternatives
from utils.helpers import detect_drugs_in_text

# -----------------------------------------
# Load models
# -----------------------------------------
tokenizer, text_model = load_text_model()
speech_processor, speech_model = load_speech_model()

# -----------------------------------------
# Streamlit UI
# -----------------------------------------
st.title("💊 AI Drug Safety & NLP Analysis System")

st.markdown("""
### Features
- Drug Interaction Detection  
- Age-Specific Dosage Recommendation  
- Alternative Medication Suggestions  
- NLP Drug Information Extraction (IBM Granite)
""")

input_mode = st.radio("Choose Input Method", ["Type Text", "Upload Audio File"])

if input_mode == "Type Text":
    text = st.text_area("Enter prescription or drug instructions:")

    if st.button("Analyze Text"):
        extracted = extract_drug_info(text, tokenizer, text_model)
        st.json(extracted)

        drug_list = detect_drugs_in_text(text)

        st.subheader("Detected Drugs")
        st.write(drug_list)

        interactions = check_interactions(drug_list)
        st.subheader("Drug Interaction Results")
        st.write(interactions if interactions else "No interactions detected.")

        age = st.number_input("Enter patient's age:", 1, 120)

        for drug in drug_list:
            st.write(f"### {drug.capitalize()}")
            st.write(f"**Dosage Recommendation:** {get_dosage(drug, age)}")
            st.write(f"**Alternatives:** {get_alternatives(drug)}")

elif input_mode == "Upload Audio File":
    audio_file = st.file_uploader("Upload prescription audio (wav/mp3)", type=["wav", "mp3"])

    if audio_file and st.button("Transcribe & Analyze"):
        from services.nlp_extractor import transcribe_audio
        text = transcribe_audio(audio_file, speech_processor, speech_model)
        st.write("### Transcription")
        st.write(text)

        extracted = extract_drug_info(text, tokenizer, text_model)
        st.json(extracted)

st.success("Done!")
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'services')))

