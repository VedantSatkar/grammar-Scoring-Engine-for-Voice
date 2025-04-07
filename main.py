##Installation:- 
##pip install speechrecognition pydub spacy textblob
##python -m spacy download en_core_web_sm
##
##Run python file with:- 
##python grammar_scoring.py
#
#
#import speech_recognition as sr  
#import spacy  
#from textblob import TextBlob  
#
## Load spaCy NLP Model
#nlp = spacy.load("en_core_web_sm")  
#
## Function to convert speech to text
#def speech_to_text(audio_file):  
#    recognizer = sr.Recognizer()  
#    with sr.AudioFile(audio_file) as source:  
#        audio_data = recognizer.record(source)  
#        try:  
#            text = recognizer.recognize_google(audio_data)  
#            return text  
#        except sr.UnknownValueError:  
#            return "Could not understand the audio."  
#        except sr.RequestError:  
#            return "Could not request results, check your internet."  
#
## Function to check grammar and suggest corrections
#def check_grammar(text):  
#    doc = nlp(text)  
#    corrected_text = TextBlob(text).correct()  
#    errors = []  
#
#    for token in doc:  
#        if token.dep_ == "nsubj" and token.pos_ != "NOUN":  
#            errors.append(f"Grammar Issue: '{token.text}' should be a NOUN.")  
#
#    return {"original": text, "corrected": str(corrected_text), "errors": errors}  
#
## Function to calculate grammar score
#def grammar_score(text):
#    analysis = check_grammar(text)
#    total_words = len(text.split())
#    error_count = len(analysis["errors"])
#    score = max(0, 100 - (error_count / total_words) * 100)  # Reduce score based on errors
#    return round(score, 2)
#
## Full pipeline to run speech-to-text + grammar check + scoring
#def grammar_scoring_pipeline(audio_file):  
#    text = speech_to_text(audio_file)  
#    if "Could not" in text:  
#        return {"error": text}  
#
#    analysis = check_grammar(text)  
#    score = grammar_score(text)  
#
#    return {  
#        "transcribed_text": text,  
#        "corrected_text": analysis["corrected"],  
#        "grammar_issues": analysis["errors"],  
#        "grammar_score": score  
#    }  
#
## Run the program
##if _name_ == "_main_":
##    audio_path = "sample_audio.wav"  # Ensure this file exists in the same directory
##    result = grammar_scoring_pipeline(audio_path)
##    print(result)
#    
#if __name__ == "__main__":
#    audio_path = "simple.mp3"
#    result = grammar_scoring_pipeline(audio_path)
#    print(result)
#

# Installation:
# pip install speechrecognition spacy textblob
# python -m spacy download en_core_web_sm



'''
import speech_recognition as sr
import spacy
from textblob import TextBlob
import streamlit as st

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to listen from microphone
def speech_to_text_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak something (recording will begin after a second)...")
        recognizer.adjust_for_ambient_noise(source)
        try:

            audio = recognizer.listen(source, timeout=2, phrase_time_limit=10)
        
        except sr.WaitTimeoutError:
            return "Microphone timed out. Please try again."
        
        

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Could not request results, check your internet."

# Grammar checking
def check_grammar(text):
    doc = nlp(text)
    corrected_text = TextBlob(text).correct()
    errors = []

    for token in doc:
        if token.dep_ == "nsubj" and token.pos_ != "NOUN":
            errors.append(f"Grammar Issue: '{token.text}' should be a NOUN.")

    return {"original": text, "corrected": str(corrected_text), "errors": errors}

# Score calculation
def grammar_score(text):
    analysis = check_grammar(text)
    total_words = len(text.split())
    error_count = len(analysis["errors"])
    score = max(0, 100 - (error_count / total_words) * 100)
    return round(score, 2)

# 🌐 Streamlit App
def main():
    st.set_page_config(page_title="Grammar Checker", layout="centered")

    st.markdown("""
        <style>
            .main {
                padding: 2rem 3rem;
                background-color: #f8f9fa;
                border-radius: 12px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }
            .stButton>button {
                border-radius: 12px;
                padding: 0.75rem 1.5rem;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
            }
            .stTextInput>div>div>input {
                padding: 0.5rem;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🧠 AI Grammar Checker")
    st.subheader("Check grammar using your voice or type your text ✍️")

    st.markdown("---")

    option = st.radio("Choose Input Method", ["🎙️ Speak", "⌨️ Type"], horizontal=True)

    input_text = ""

    if option == "🎙️ Speak":
        if st.button("🎤 Start Recording"):
            input_text = speech_to_text_from_mic()
            if "Could not" in input_text or "timed out" in input_text:
                st.error(input_text)
            else:
                st.success("Speech converted to text!")
                st.write("**You said:**", input_text)
    else:
        input_text = st.text_area("Type your text here", height=150)

    if input_text:
        st.markdown("---")
        st.subheader("📌 Results")

        analysis = check_grammar(input_text)
        score = grammar_score(input_text)

        st.write("### ✍️ Original Text")
        st.write(analysis["original"])

        st.write("### ✅ Corrected Text")
        st.success(analysis["corrected"])

        st.write("### 📈 Grammar Score")
        st.progress(score / 100)
        st.info(f"Your grammar score is **{score}/100**")

        if analysis["errors"]:
            st.write("### ⚠️ Grammar Issues Found")
            for issue in analysis["errors"]:
                st.warning(issue)
        else:
            st.success("🎉 Great job! No grammar issues found.")

    st.markdown("---")
    st.caption("Made with ❤️ by Vedant Satkar")
    
def detect_tense(text):
    doc = nlp(text)
    tense_info = {"tense": "Unknown", "tip": "No clear tense found."}

    for token in doc:
        if token.tag_ in ['VBD', 'VBN']:
            tense_info["tense"] = "Past"
            tense_info["tip"] = "🕒 Past Tense: Used for actions completed in the past. Example: 'I ate lunch.'"
            break
        elif token.tag_ in ['VBP', 'VBZ']:
            tense_info["tense"] = "Present"
            tense_info["tip"] = "🕓 Present Tense: Used for current or regular actions. Example: 'She walks to school.'"
            break
        elif token.tag_ == 'MD' and token.head.tag_ == 'VB':
            tense_info["tense"] = "Future"
            tense_info["tip"] = "🕐 Future Tense: Used for actions that will happen later. Example: 'He will travel tomorrow.'"
            break

    return tense_info


if __name__ == "__main__":
    main()

# Pipeline for microphone
def grammar_scoring_pipeline_from_mic():
    text = speech_to_text_from_mic()

    if "Could not" in text:
        return {"error": text}

    analysis = check_grammar(text)
    score = grammar_score(text)

    return {
        "transcribed_text": text,
        "corrected_text": analysis["corrected"],
        "grammar_issues": analysis["errors"],
        "grammar_score": score
    }

# Main
if __name__ == "__main__":
    result = grammar_scoring_pipeline_from_mic()
    print("\n📝 Result:")
    print(result)


import speech_recognition as sr
import spacy
from textblob import TextBlob
import streamlit as st

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to listen from microphone
def speech_to_text_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak something (recording will begin after a second)...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return "Microphone timed out. Please try again."

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Could not request results, check your internet."

# Grammar checking
def check_grammar(text):
    doc = nlp(text)
    corrected_text = TextBlob(text).correct()
    errors = []

    for token in doc:
        if token.dep_ == "nsubj" and token.pos_ != "NOUN":
            errors.append(f"Grammar Issue: '{token.text}' should be a NOUN.")

    return {"original": text, "corrected": str(corrected_text), "errors": errors}

# Grammar score
def grammar_score(text):
    analysis = check_grammar(text)
    total_words = len(text.split())
    error_count = len(analysis["errors"])
    score = max(0, 100 - (error_count / total_words) * 100)
    return round(score, 2)

# Detect Tense
def detect_tense(text):
    doc = nlp(text)
    tense_info = {"tense": "Unknown", "tip": "No clear tense found."}

    for token in doc:
        if token.tag_ in ['VBD', 'VBN']:
            tense_info["tense"] = "Past"
            tense_info["tip"] = "🕒 Past Tense: Used for actions completed in the past. Example: 'I ate lunch.'"
            break
        elif token.tag_ in ['VBP', 'VBZ']:
            tense_info["tense"] = "Present"
            tense_info["tip"] = "🕓 Present Tense: Used for current or regular actions. Example: 'She walks to school.'"
            break
        elif token.tag_ == 'MD' and token.head.tag_ == 'VB':
            tense_info["tense"] = "Future"
            tense_info["tip"] = "🕐 Future Tense: Used for actions that will happen later. Example: 'He will travel tomorrow.'"
            break

    return tense_info

# 🌐 Streamlit App
def main():
    st.set_page_config(page_title="Grammar Checker", layout="centered")

    st.markdown("""
        <style>
            .main {
                padding: 2rem 3rem;
                background-color: #f8f9fa;
                border-radius: 12px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }
            .stButton>button {
                border-radius: 12px;
                padding: 0.75rem 1.5rem;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
            }
            .stTextArea textarea {
                padding: 1rem;
                font-size: 16px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
            .stRadio>div {
                padding-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🧠 AI Grammar Checker")
    st.subheader("Check grammar using your voice or type your text ✍️")

    st.markdown("---")

    option = st.radio("Choose Input Method", ["🎙️ Speak", "⌨️ Type"], horizontal=True)
    input_text = ""

    if option == "🎙️ Speak":
        if st.button("🎤 Start Recording"):
            input_text = speech_to_text_from_mic()
            if "Could not" in input_text or "timed out" in input_text:
                st.error(input_text)
            else:
                st.success("Speech converted to text!")
                st.write("**You said:**", input_text)
    else:
        input_text = st.text_area("Type your text here 👇", height=150)

    if input_text:
        if st.button("🔘 Run Grammar Check"):
            st.markdown("---")
            st.subheader("📌 Results")

            analysis = check_grammar(input_text)
            score = grammar_score(input_text)
            tense = detect_tense(input_text)

            st.write("### ✍️ Original Text")
            st.write(analysis["original"])

            st.write("### ✅ Corrected Text")
            st.success(analysis["corrected"])

            st.write("### 📈 Grammar Score")
            st.progress(score / 100)
            st.info(f"Your grammar score is **{score}/100**")

            st.write("### 🕰️ Tense Detected")
            st.success(f"**Tense:** {tense['tense']}")
            st.caption(tense["tip"])

            if analysis["errors"]:
                st.write("### ⚠️ Grammar Issues Found")
                for issue in analysis["errors"]:
                    st.warning(issue)
            else:
                st.success("🎉 Great job! No grammar issues found.")

    st.markdown("---")
    st.caption("Made with ❤️ by Vedant Satkar")

if __name__ == "__main__":
    main()
'''

import speech_recognition as sr
import spacy
from textblob import TextBlob
import streamlit as st
import tempfile
import os
from pydub import AudioSegment
from fpdf import FPDF

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to listen from microphone
def speech_to_text_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return "Microphone timed out. Please try again."
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Could not request results, check your internet."

# Function to process uploaded audio file
def speech_to_text_from_file(uploaded_file):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        audio = AudioSegment.from_file(uploaded_file)
        audio.export(temp_wav.name, format="wav")
        with sr.AudioFile(temp_wav.name) as source:
            audio_data = recognizer.record(source)
        os.unlink(temp_wav.name)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Could not understand the audio file."
    except sr.RequestError:
        return "Could not request results from Google API."

# Grammar checking
def check_grammar(text):
    doc = nlp(text)
    corrected_text = TextBlob(text).correct()
    errors = []
    for token in doc:
        if token.dep_ == "nsubj" and token.pos_ != "NOUN":
            errors.append(f"Grammar Issue: '{token.text}' should be a NOUN.")
    return {"original": text, "corrected": str(corrected_text), "errors": errors}

# Score calculation
def grammar_score(text):
    analysis = check_grammar(text)
    total_words = len(text.split())
    error_count = len(analysis["errors"])
    score = max(0, 100 - (error_count / total_words) * 100)
    return round(score, 2)

# Detect tense
def detect_tense(text):
    doc = nlp(text)
    tense_info = {"tense": "Unknown", "tip": "No clear tense found."}
    for token in doc:
        if token.tag_ in ['VBD', 'VBN']:
            tense_info = {"tense": "Past", "tip": "🕒 Past Tense: Actions completed in the past. Eg: 'I ate lunch.'"}
            break
        elif token.tag_ in ['VBP', 'VBZ']:
            tense_info = {"tense": "Present", "tip": "🕓 Present Tense: Ongoing or regular actions. Eg: 'She walks to school.'"}
            break
        elif token.tag_ == 'MD' and token.head.tag_ == 'VB':
            tense_info = {"tense": "Future", "tip": "🕐 Future Tense: Actions to be done. Eg: 'He will travel tomorrow.'"}
            break
    return tense_info

# Export results to PDF
def export_to_pdf(analysis, score, tense):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Grammar Analysis Report", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Original Text:\n{analysis['original']}\n")
    pdf.multi_cell(0, 10, txt=f"Corrected Text:\n{analysis['corrected']}\n")
    pdf.multi_cell(0, 10, txt=f"Grammar Score: {score}/100")
    pdf.multi_cell(0, 10, txt=f"Detected Tense: {tense['tense']} - {tense['tip']}")
    if analysis["errors"]:
        pdf.cell(0, 10, txt="Grammar Issues:", ln=True)
        for err in analysis["errors"]:
            pdf.multi_cell(0, 10, txt=err)
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(pdf_file.name)
    return pdf_file.name

# Streamlit App
def main():
    st.set_page_config(page_title="Grammar Scoring Engine", layout="centered")
    st.title("🧠 Grammar Scoring Engine for Voice Samples")
    st.subheader("🎤 Upload voice or text to analyze grammar")
    st.markdown("---")

    option = st.radio("Choose Input Method", ["🎙️ Speak Now", "📁 Upload Voice Sample", "⌨️ Type Text"], horizontal=True)

    input_text = ""

    if option == "🎙️ Speak Now":
        if st.button("🎤 Record Now"):
            input_text = speech_to_text_from_mic()
            if "Could not" in input_text or "timed out" in input_text:
                st.error(input_text)
            else:
                st.success("Speech converted to text!")
                st.write("**You said:**", input_text)

    elif option == "📁 Upload Voice Sample":
        uploaded_file = st.file_uploader("Upload an audio file (mp3/wav)", type=['mp3', 'wav'])
        if uploaded_file and st.button("🔍 Analyze Audio"):
            input_text = speech_to_text_from_file(uploaded_file)
            if "Could not" in input_text:
                st.error(input_text)
            else:
                st.success("Audio converted to text!")
                st.write("**Audio says:**", input_text)

    else:
        input_text = st.text_area("Type your text here", height=150)
        if st.button("✅ Analyze Text") and not input_text.strip():
            st.warning("Please enter some text to analyze.")

    if input_text.strip():
        st.markdown("---")
        st.subheader("📌 Analysis Results")

        analysis = check_grammar(input_text)
        score = grammar_score(input_text)
        tense = detect_tense(input_text)

        st.write("### ✍️ Original Text")
        st.write(analysis["original"])

        st.write("### ✅ Corrected Text")
        st.success(analysis["corrected"])

        st.write("### ⏳ Tense Detected")
        st.info(f"**{tense['tense']}** - {tense['tip']}")

        st.write("### 📈 Grammar Score")
        st.progress(score / 100)
        st.info(f"Your grammar score is **{score}/100**")

        if analysis["errors"]:
            st.write("### ⚠️ Grammar Issues Found")
            for issue in analysis["errors"]:
                st.warning(issue)
        else:
            st.success("🎉 Great job! No grammar issues found.")

        st.markdown("---")
        if st.button("📄 Export as PDF"):
            pdf_path = export_to_pdf(analysis, score, tense)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download Report", f, file_name="grammar_report.pdf")

    st.markdown("---")
    st.caption("Made with ❤️ by Vedant Satkar for SHL AI Internship")

if __name__ == "__main__":
    main()
