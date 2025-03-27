import streamlit as st
import os
import fitz as pymupdf
from docx import Document
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai_api_key = os.getenv("GEMINI_API_KEY")

if not genai_api_key:
    st.error("GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=genai_api_key)
# Existing model for generating lesson blueprints
blueprint_model = genai.GenerativeModel("gemini-1.5-flash")
# New model instance for generating assessment items (change model name as needed)
assessment_model = genai.GenerativeModel("gemini-1.5-flash")

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
st.title("Lesson Blueprint Generator")

# User inputs
lesson_info = st.text_area("Enter Lesson Information (title, description, lesson question, and learning objectives):")
additional_resources = st.text_area("Enter Additional Resources (optional):")

# Instruction prompt for Lesson Blueprint Generation
def create_lesson_blueprint(lesson_info, additional_resources, reference_content):
    prompt = f"""
    ### Reference Materials
    {reference_content}

    ### Context
    You are an AI instructional designer creating detailed lesson blueprints for middle and high school social studies lessons.

    ### Objective
    Using the provided lesson information (title, description, lesson question, and learning objectives), any additional resources provided, and the \"CCAG-EdgeEX Lesson Blueprinting-270325-194434\" from your knowledge base, develop a structured Lesson Blueprint clearly segmented into sections. Each blueprint must include:

    - A restatement of the provided lesson question.
    - A restatement of the provided learning objectives.
    - A rephrased version of each learning objective in student-friendly language.
    - Identification of key vocabulary terms (4–6 words) essential for understanding the lesson content.
    - A warm-up section designed to activate prior knowledge and engage students.
    - Clearly segmented instructional sections aligned with each learning objective provided, including:
        - Clearly stated learning objectives.
        - Concise content breakdown organized logically into subpoints.
        - Instructional supports (e.g., visual aids, interactive activities, multimedia recommendations).
        - Explicit attention to potential misconceptions or challenges related to the lesson content.
    - A closing connection summarizing the core learning outcomes and linking them meaningfully to broader themes or real-world relevance.
    - Additional notes recommending extension activities, multimedia resources, or formative assessments.

    ### Provided Information
    Lesson Information: {lesson_info}
    Additional Resources: {additional_resources}

    ### Style
    Structured, clear, and detailed. Organize content logically using concise bullet points and clearly labeled subsections, facilitating straightforward implementation into teaching materials or multimedia instruction.

    ### Tone
    Professional, informative, and student-focused. Clearly and objectively convey lesson content, emphasizing clarity of instruction, student understanding, and engagement.

    ### Audience
    Instructional content developers, social studies teachers, and educational designers with familiarity in instructional methods and multimedia instructional tools. Assume moderate familiarity with social studies content but explicitly clarify complex concepts.

    ### Response
    Provide the Lesson Blueprint in the following format:

    Lesson Blueprint

    **Lesson Question**  
    - Restate the provided lesson question clearly.

    **Lesson Learning Goals**  
    - Restate the provided learning objectives exactly as given.
    - Rephrase each learning objective in student-friendly language.

    **Key Vocabulary**  
    - List 4–6 essential vocabulary terms students must understand to engage effectively with the lesson.

    **Warm-Up**  
    - Brief, engaging introduction designed to activate prior knowledge related to the lesson.

    **Instruction Sections** (Segment logically based on provided objectives)  
    For each section include:
    - Clearly stated learning objective.
    - Concise content breakdown, organized into logical subpoints.
    - Instructional supports (e.g., visual aids, interactive maps, multimedia recommendations).
    - Explicit attention to potential misconceptions or challenges students may encounter.

    **Closing Connection**  
    - Summarize the core learning outcomes and link meaningfully to broader themes, historical significance, or contemporary relevance.

    **Additional Notes**  
    - Recommendations for extension activities, multimedia resources, or formative assessment practices.
    """
    try:
        response = blueprint_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating content: {str(e)}"

# Instruction prompt for Assessment Items Generation
def create_assessment_items(blueprint):
    prompt = f"""
    Using the following Lesson Blueprint, generate a series of assessment items that align with the lesson's learning objectives.

    Multiple-choice items will consist of 4 answer choices. Only 1 answer choice should be correct. Incorrect options should be based on common misconceptions or misunderstandings. Incorrect choices should seem probable and should not be wildly incorrect. All answer choices should be parallel in style and should be roughly the same length. 

    Multiple-select items will consist of 5 answer choices. 2-3 choices should be correct. Incorrect options should be based on common misconceptions or misunderstandings. Incorrect choices should seem probable and should not be wildly incorrect. All answer choices should be parallel in style and should be roughly the same length. 

    All question items should include a hint feedback item for students who may make an incorrect selection. 

    All question items should identify the correct answer for multiple choice and correct answers for multiple-select.

    Do not use:
    - Language such as "which of the following" instead directly ask "which statement" 
    - Negative questions that include "NOT," "False," or "EXCEPT" (for example avoid a question like: "All of the following are true, except," or "which of the following is false?"
    -answer choices that include: "None of the above" or "all of the above"

    Style guides:
    - US is the preferred abbreviation for the United States - not U.S.
    - always use an Oxford comma

    Make sure that each question item has a Header that begins with Gerund phrase (for example: Analyzing a Primary Source, or Identifying Cause and Effect)

    For 6th grade audience lexile level should be 500-650, for 7th grade audience the lexile level should be 650-800, for a 9th grade audience the lexile level should be 800-1000 and for 10th grade audience the lexile level should be 900-1100.

    >>>Lesson Blueprint:
    {blueprint}

    Provide the assessment items in a structured format with clear item numbers for later reference.
    """
    try:
        response = assessment_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating assessment items: {str(e)}"

# Generate button and workflow
if st.button("Generate Lesson Blueprint"):
    if not lesson_info.strip():
        st.warning("Please enter lesson information to generate content.")
    else:
        # Generate Lesson Blueprint
        with st.spinner("Generating lesson blueprint..."):
            blueprint_output = create_lesson_blueprint(lesson_info, additional_resources, reference_content)
        
        # Generate Assessment Items using the blueprint output
        with st.spinner("Generating assessment items..."):
            assessment_output = create_assessment_items(blueprint_output)
        
        # Display outputs in expandable sections
        with st.expander("Generated Lesson Blueprint", expanded=True):
            st.write(blueprint_output)
        with st.expander("Generated Assessment Items", expanded=True):
            st.write(assessment_output)
