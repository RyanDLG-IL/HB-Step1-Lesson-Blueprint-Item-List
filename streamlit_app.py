import streamlit as st
import os
import fitz as pymupdf
from docx import Document
from dotenv import load_dotenv
import google.generativeai as genai

# Import the prompt function from the prompts directory
from prompts.lesson_blueprint_prompt import get_prompt
from prompts.assessment_items_prompt import get_prompt as get_assessment_prompt
from prompts.media_suggestions_prompt import get_prompt as get_media_prompt



# Load environment variables
load_dotenv()
genai_api_key = os.getenv("GEMINI_API_KEY")

if not genai_api_key:
    st.error("GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=genai_api_key)
# Model instances
blueprint_model = genai.GenerativeModel("gemini-1.5-flash")
assessment_model = genai.GenerativeModel("gemini-1.5-flash")
media_model = genai.GenerativeModel("gemini-1.5-flash")  # New instance for media suggestions

# Helper functions
def extract_text_from_pdf(pdf_path):
    try:
        doc = pymupdf.open(pdf_path)
        text = ''
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF ({pdf_path}): {str(e)}"

def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX ({docx_path}): {str(e)}"

def load_reference_materials(folder_path):
    reference_texts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.lower().endswith(('.txt', '.md')):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        elif filename.lower().endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            continue
        reference_texts.append(f"Document: {filename}\n{text}\n\n")
    return "\n".join(reference_texts)

# Load reference materials
reference_materials_folder = 'reference_materials'
reference_content = load_reference_materials(reference_materials_folder)

# Streamlit page setup
st.set_page_config(page_title="Lesson Blueprint Generator", layout="centered")
st.title("Lesson Blueprint, Assessment, and Media Suggestion Generator")

# User inputs
lesson_info = st.text_area("Enter Lesson Information (title, description, lesson question, and learning objectives):")
additional_resources = st.text_area("Enter any additional resources such as websites or additional content (optional):")


# Instruction prompt for Lesson Blueprint Generation
def create_lesson_blueprint(lesson_info, additional_resources, reference_content):
    # Get the prompt from the imported function
    prompt = get_prompt(reference_content, lesson_info, additional_resources)
    
    try:
        response = blueprint_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating content: {str(e)}"

# Instruction prompt for Assessment Items Generation
from prompts.assessment_items_prompt import get_prompt as get_assessment_prompt

def create_assessment_items(blueprint):
    prompt = get_assessment_prompt(blueprint)
    try:
        response = assessment_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating assessment items: {str(e)}"

# Instruction prompt for Media Suggestions Generation
def create_media_suggestions(blueprint, assessment):
    prompt = get_media_prompt(blueprint, assessment)
    try:
        response = media_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating media suggestions: {str(e)}"

# Generate button and workflow
if st.button("Generate Content"):
    if not lesson_info.strip():
        st.warning("Please enter lesson information to generate content.")
    else:
        # Generate Lesson Blueprint
        with st.spinner("Generating lesson blueprint..."):
            blueprint_output = create_lesson_blueprint(lesson_info, additional_resources, reference_content)
        
        # Generate Assessment Items using the blueprint output
        with st.spinner("Generating assessment items..."):
            assessment_output = create_assessment_items(blueprint_output)
        
        # Generate Media Suggestions using both blueprint and assessment outputs
        with st.spinner("Generating media suggestions..."):
            media_output = create_media_suggestions(blueprint_output, assessment_output)
        
        # Display outputs in expandable sections
        with st.expander("Generated Lesson Blueprint", expanded=True):
            st.write(blueprint_output)
        with st.expander("Generated Assessment Items", expanded=True):
            st.write(assessment_output)
        with st.expander("Generated Media Suggestions", expanded=True):
            st.write(media_output)