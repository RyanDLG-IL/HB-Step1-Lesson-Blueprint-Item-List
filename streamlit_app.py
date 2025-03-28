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
    Using the following Lesson Blueprint, generate a comprehensive set of assessment items that align with the lesson's learning objectives. The assessment items must follow the exact structure and specifications provided below.

      ### Required Assessment Items (Generate ALL of these):
    
    
    1. Instructional Segment 1 Item 1 (Objective 1 DOK Low) - needs Feedback
    2. Instructional Segment 1 Item 2 (Objective 1 DOK Low) - needs Feedback
    3. Instructional Segment 2 Item 1 (Objective 2 DOK Low) - needs Feedback
    4. Instructional Segment 2 Item 2 (Objective 2 DOK Low) - needs Feedback
    5. Instructional Segment 3 Item 1 (Objective 3 DOK High) - needs Feedback
    6. Instructional Segment 3 Item 2 (Objective 3 DOK High) - needs Feedback
    7. Instructional Segment 4 Item 1 (Objective 3 DOK 3) - needs Feedback
    8. Instructional Segment 4 Item 2 (Objective 3 DOK 3) - needs Feedback
    9. Objective 1 DOK 1 SSA Item 1 - needs Feedback
    10. Objective 1 DOK 1 SSA Item 2 - needs Feedback
    11. Objective 1 DOK 2 SSA Item 1 - needs Feedback
    12. Objective 1 DOK 2 SSA Item 2 - needs Feedback
    13. Objective 2 DOK 1 SSA Item 1 - needs Feedback
    14. Objective 2 DOK 1 SSA Item 2 - needs Feedback
    15. Objective 2 DOK 2 SSA Item 1 - needs Feedback
    16. Objective 2 DOK 2 SSA Item 2 - needs Feedback
    17. Objective 3 DOK 1 SSA Item 1 - needs Feedback
    18. Objective 3 DOK 1 SSA Item 2 - needs Feedback
    19. Objective 3 DOK 2 SSA Item 1 - needs Feedback
    20. Objective 3 DOK 2 SSA Item 2 - needs Feedback
    21. Objective 3 DOK 3 SSA Item 1 - needs Feedback
    22. Objective 3 DOK 3 SSA Item 2 - needs Feedback
    23. Objective 1 DOK 1 Assessment Item 1
    24. Objective 1 DOK 1 Assessment Item 2
    25. Objective 1 DOK 1 Assessment Item 3
    26. Objective 1 DOK 1 Assessment Item 4
    27. Objective 1 DOK 2 Assessment Item 1
    28. Objective 1 DOK 2 Assessment Item 2
    29. Objective 1 DOK 2 Assessment Item 3
    30. Objective 1 DOK 2 Assessment Item 4
    31. Objective 1 DOK 2 Assessment Item 5
    32. Objective 1 DOK 2 Assessment Item 6
    33. Objective 2 DOK 1 Assessment Item 1
    34. Objective 2 DOK 1 Assessment Item 2
    35. Objective 2 DOK 1 Assessment Item 3
    36. Objective 2 DOK 1 Assessment Item 4
    37. Objective 2 DOK 2 Assessment Item 1
    38. Objective 2 DOK 2 Assessment Item 2
    39. Objective 2 DOK 2 Assessment Item 3
    40. Objective 2 DOK 2 Assessment Item 4
    41. Objective 2 DOK 2 Assessment Item 5
    42. Objective 2 DOK 2 Assessment Item 6
    43. Objective 3 DOK 1 Assessment Item 1
    44. Objective 3 DOK 1 Assessment Item 2
    45. Objective 3 DOK 1 Assessment Item 3
    46. Objective 3 DOK 1 Assessment Item 4
    47. Objective 3 DOK 2 Assessment Item 1
    48. Objective 3 DOK 2 Assessment Item 2
    49. Objective 3 DOK 2 Assessment Item 3
    50. Objective 3 DOK 2 Assessment Item 4
    51. Objective 3 DOK 2 Assessment Item 5
    52. Objective 3 DOK 2 Assessment Item 6
    53. Objective 3 DOK 3 Assessment Item 1
    54. Objective 3 DOK 3 Assessment Item 2
    55. Objective 3 DOK 3 Assessment Item 3
    56. Objective 3 DOK 3 Assessment Item 4

    ### Social Studies DOK Level Guidelines:
    - DOK 1 (Recall of Information): Items ask students to recall facts, terms, concepts, trends, generalizations, and theories. May require students to recognize or identify specific information contained in maps, charts, tables, graphs, or other graphics. Items typically ask who, what, when, and where. Simple "describe" and "explain" tasks that require only recitation or reproduction of information are DOK 1.
    
    - DOK 2 (Basic Reasoning): Items require mental processing beyond recalling information. Students may need to compare or contrast people, places, events, and concepts; convert information from one form to another; classify items into meaningful categories; or describe/explain issues, problems, patterns, cause and effect, significance, relationships, points of view or processes in their own words. A DOK 2 explanation requires students to go beyond simple recall to discuss how or why.
    
    - DOK 3 (Application): Items require reasoning, use of evidence, and higher-level thinking. Students must justify the how and why through application and evidence. This includes drawing and justifying conclusions based on evidence; using concepts to explain how and why; analyzing similarities and differences among issues; proposing and evaluating solutions; recognizing misconceptions; or making connections across time and place to explain concepts.

    ### Item Format Guidelines:
    - Multiple-choice items will consist of 4 answer choices. Only 1 answer choice should be correct. 
    - Incorrect options should be based on common misconceptions or misunderstandings. 
    - Incorrect choices should seem plausible and should not be wildly incorrect. 
    - All answer choices should be parallel in style and should be roughly the same length.

    - Multiple-select items will consist of 5 answer choices. 2-3 choices should be correct. 
    - Incorrect options should be based on common misconceptions or misunderstandings. 
    - Incorrect choices should seem plausible and should not be wildly incorrect. 
    - All answer choices should be parallel in style and should be roughly the same length.

    ### Feedback Requirements:
    For items noted as needing feedback, provide targeted feedback that:
    - Anticipates misconceptions and stumbling blocks
    - Reminds students of key concepts and skills taught in the lesson
    - Supports and reinforces key learning to help students correct their answers
    - Is unique to each item and provides focused information
    - Is concise (approximately one sentence)
    - Does NOT give away the correct answer
    - Does NOT teach new concepts or approaches
    - Does NOT consist of generic boilerplate language

    ### Style Guidelines:
    - Each question item should have a Header that begins with a Gerund phrase (e.g., "Analyzing a Primary Source" or "Identifying Cause and Effect")
    - Do not use language such as "which of the following" - rather directly ask "which statement" 
    - Do not use negative questions that include "NOT," "False," or "EXCEPT" 
    - Do not use answer choices that include: "None of the above" or "all of the above"
    - US is the preferred abbreviation for the United States - not U.S.
    - Always use an Oxford comma
    - For 6th grade audience: lexile level should be 500-650
    - For 7th grade audience: lexile level should be 650-800
    - For 9th grade audience: lexile level should be 800-1000
    - For 10th grade audience: lexile level should be 900-1100

    >>>Lesson Blueprint:
    {blueprint}

    Provide the assessment items in a structured format with clear sections for:
    1. Instructional Segment Items (with feedback)
    2. Self-Study Assignment Items (with feedback)
    3. Assessment Items

    For each item, include:
    - Clear item number and identification (e.g., "Instructional Segment 1 Item 1")
    - The gerund phrase header
    - The question
    - Answer choices (labeled A, B, C, D or A, B, C, D, E for multiple select)
    - Correct answer(s) clearly indicated
    - Feedback (for items that require it)
    - Clear indication of which objective and DOK level each item addresses
    
    Example format for an item with feedback:
    
    ## Instructional Segment 1 Item 1 (Objective 1, DOK Level 1)
    
    ### Identifying Geographic Features
    
    Which statement correctly describes a key characteristic of Alabama's Coastal Plain region?
    
    A. It's a mountainous region with diverse flora and fauna. 
    B. It features rolling hills and fertile valleys. 
    C. It's characterized by flat, low-lying land with sandy soil and swamps. 
    D. It has high elevations and a cooler climate than other regions.
    
    Correct Answer: C
    
    Feedback: The Coastal Plain region is defined by its low elevation and flat terrain near the Gulf of Mexico.
    """
    try:
        response = assessment_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating assessment items: {str(e)}"

# Instruction prompt for Media Suggestions Generation
def create_media_suggestions(blueprint, assessment):
    prompt = f"""
    ## Context ##
    You are assisting a content developer who creates online educational lessons for social studies. The lessons follow structured lesson blueprints that include clear learning goals, objectives, vocabulary, warm-up activities, instruction sections, and assessments. You will specifically identify visual media (primarily maps, photos, satellite imagery, historical images) relevant to lesson content. All media recommendations must prioritize open-source or free-to-use images. Rather than providing URLs, offer detailed descriptions of images that can guide the content development team in finding or creating the visual media. All descriptions must comply with provided Diversity, Equity, and Inclusion (DEI) guidelines, emphasizing diverse and equitable representation.

    ## Objective ##
    Provide detailed, authentic descriptions of visual media suggestions aligned explicitly with provided lesson blueprint content and assessments. Include recommended placement in lesson sections or associated assessment items (including the specific item number(s)). Ensure descriptions are clear enough to guide the content development team in effectively sourcing or creating the media.

    ## Style ##
    Structured, concise, and actionable. Clearly separate each description with detailed reasoning for alignment with lesson content, instructional goals, and DEI compliance.

    ## Tone ##
    Professional, supportive, and inclusive. Descriptions should clearly reflect cultural awareness, equity, and educational relevance.

    ## Audience ##
    Educational content developers, instructional designers, and educators familiar with social studies curriculum development and DEI standards.

    ## Response ##
    Present your detailed image descriptions in a structured table with the following headers:

    | Lesson Section or Assessment Item (include item number if applicable) | Media Type (Image/Map/Satellite Imagery/Video) | Detailed Description (clear, actionable, linked to lesson goals and DEI) |
    |-----------------------------------------------------------------------|-------------------------------------------------|--------------------------------------------------------------------------|

    ### Provided Lesson Blueprint:
    {blueprint}

    ### Provided Assessment Items:
    {assessment}
    """
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