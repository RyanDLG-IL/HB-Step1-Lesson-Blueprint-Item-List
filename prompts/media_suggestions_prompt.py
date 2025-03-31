def get_prompt(blueprint, assessment):
    return f"""
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