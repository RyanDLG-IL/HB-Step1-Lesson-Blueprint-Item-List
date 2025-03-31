def get_prompt(blueprint):
    return f"""
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
    
    **Instructional Segment 1 Item 1 (Objective 1, DOK Level 1)**
    - Identifying Geographic Features
    
    Which statement correctly describes a key characteristic of Alabama's Coastal Plain region?
    
    A. It's a mountainous region with diverse flora and fauna. 
    B. It features rolling hills and fertile valleys. 
    C. It's characterized by flat, low-lying land with sandy soil and swamps. 
    D. It has high elevations and a cooler climate than other regions.
    
    Correct Answer: C
    
    Feedback: The Coastal Plain region is defined by its low elevation and flat terrain near the Gulf of Mexico.
    """