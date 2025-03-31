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
from prompts.fact_check_prompt import get_prompt as get_fact_check_prompt
from prompts.dei_check_prompt import get_prompt as get_dei_check_prompt


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
media_model = genai.GenerativeModel("gemini-1.5-flash")  
fact_check_model = genai.GenerativeModel("gemini-1.5-flash")  
dei_check_model = genai.GenerativeModel("gemini-1.5-flash") 


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

# Updated function to load specific reference materials (PDF and DOCX)
def load_dei_reference_materials(folder_path):
    dei_reference_texts = []
    target_files = ["Subject Specific Guidelines-Social Studies", "DEI Content Authoring Guidelines"]
    
    for filename in os.listdir(folder_path):
        # Check if the filename contains any of the target file names
        if any(target_file in filename for target_file in target_files):
            file_path = os.path.join(folder_path, filename)
            
            # Process based on file extension
            if filename.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            elif filename.lower().endswith('.docx'):
                text = extract_text_from_docx(file_path)
            else:
                continue
                
            dei_reference_texts.append(f"Document: {filename}\n{text}\n\n")
    
    return "\n".join(dei_reference_texts)

# Function to load specific blueprint reference material
def load_blueprint_reference(folder_path):
    target_file = "CCAG-EdgeEX Lesson Blueprinting-270325-194434"
    
    for filename in os.listdir(folder_path):
        if target_file in filename:
            file_path = os.path.join(folder_path, filename)
            if filename.lower().endswith('.pdf'):
                return extract_text_from_pdf(file_path)
            elif filename.lower().endswith('.docx'):
                return extract_text_from_docx(file_path)
    
    # If file not found, return an empty string or a message
    return "Blueprint reference file not found."


# Load reference materials
reference_materials_folder = 'reference_materials'
reference_content = load_reference_materials(reference_materials_folder)

# Load DEI-specific reference materials
dei_reference_content = load_dei_reference_materials(reference_materials_folder)

# Load blueprint-specific reference material
blueprint_reference_content = load_blueprint_reference(reference_materials_folder)

# Streamlit page setup
st.set_page_config(page_title="Lesson Blueprint Generator", layout="centered")
st.title("Lesson Blueprint, Assessment, and Media Suggestion Generator")

# User inputs
lesson_info = st.text_area("Enter Lesson Information (title, description, lesson question, and learning objectives):")
additional_resources = st.text_area("Enter any additional resources such as websites or additional content (optional):")


# Instruction prompt for Lesson Blueprint Generation
def create_lesson_blueprint(lesson_info, additional_resources, blueprint_reference_content):
    # Get the prompt from the imported function, using the specific blueprint reference
    prompt = get_prompt(blueprint_reference_content, lesson_info, additional_resources)
    
    # Add DEI reference materials to consider
    prompt += f"""
    
    ### Additional DEI Considerations
    Please ensure your lesson blueprint incorporates these DEI guidelines:
    {dei_reference_content}
    """
    
    try:
        response = blueprint_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating content: {str(e)}"

# Instruction prompt for Assessment Items Generation
def create_assessment_items(blueprint):
    prompt = get_assessment_prompt(blueprint)
    
    # Add DEI reference materials to consider
    prompt += f"""
    
    ### Additional DEI Considerations
    Please ensure your assessment items follow these DEI guidelines:
    {dei_reference_content}
    """
    
    try:
        response = assessment_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating assessment items: {str(e)}"

# Instruction prompt for Media Suggestions Generation
def create_media_suggestions(blueprint, assessment):
    prompt = get_media_prompt(blueprint, assessment)
    
    # Add DEI reference materials to consider
    prompt += f"""
    
    ### Additional DEI Considerations
    Please ensure your media suggestions follow these DEI guidelines:
    {dei_reference_content}
    """
    
    try:
        response = media_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating media suggestions: {str(e)}"
    
# Functions for fact checking and DEI checking
def create_fact_check(blueprint, assessment, media_suggestions):
    prompt = get_fact_check_prompt(blueprint, assessment, media_suggestions)
    
    # Add DEI reference materials for context
    prompt += f"""
    
    ### Additional Context
    While conducting the fact check, please be aware of these DEI guidelines:
    {dei_reference_content}
    """
    
    try:
        response = fact_check_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating fact check: {str(e)}"

def create_dei_check(blueprint, assessment, media_suggestions):
    prompt = get_dei_check_prompt(blueprint, assessment, media_suggestions, dei_reference_content)
    try:
        response = dei_check_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating DEI check: {str(e)}"

# Generate button and workflow
if st.button("Generate Content"):
    if not lesson_info.strip():
        st.warning("Please enter lesson information to generate content.")
    else:
        # Generate primary content
        with st.spinner("Generating lesson blueprint..."):
            blueprint_output = create_lesson_blueprint(lesson_info, additional_resources, blueprint_reference_content)
        
        with st.spinner("Generating assessment items..."):
            assessment_output = create_assessment_items(blueprint_output)
        
        with st.spinner("Generating media suggestions..."):
            media_output = create_media_suggestions(blueprint_output, assessment_output)
        
        # Run fact check and DEI checks in parallel
        col1, col2 = st.columns(2)
        
        with col1:
            with st.spinner("Running fact check..."):
                fact_check_output = create_fact_check(blueprint_output, assessment_output, media_output)
                
        with col2:
            with st.spinner("Running DEI check..."):
                dei_check_output = create_dei_check(blueprint_output, assessment_output, media_output)
        
        # Display all outputs in expandable sections
        with st.expander("Generated Lesson Blueprint", expanded=True):
            st.write(blueprint_output)
            
        with st.expander("Generated Assessment Items", expanded=True):
            st.write(assessment_output)
            
        with st.expander("Generated Media Suggestions", expanded=True):
            st.write(media_output)
            
        with st.expander("Fact Check Report", expanded=True):
            st.write(fact_check_output)
            
        with st.expander("DEI Check Report", expanded=True):
            st.write(dei_check_output)