# app/prompts.py

def create_prompts(jd_text):
    """
    Creates dynamic prompts based on the provided Job Description (JD).
    Args:
        jd_text (str): The job description text.
    Returns:
        tuple: Tuple containing JD analysis prompt, resume analysis prompt, and comparison prompt.
    """
    # Prompt to analyze the JD in detail
    jd_analysis_prompt = f"""
    Analyze the following job description in detail and extract the key requirements including:
    - Core Required Skills (technical and soft skills)
    - Preferred Skills (if mentioned)
    - Required Certifications or Licenses
    - Minimum and Preferred Years of Experience
    - Required Educational Background (including degrees or fields of study)
    - Any specific tools, software, or technologies mentioned
    - Key Responsibilities and Expectations for the role
    Provide a structured list of these requirements.
    
    Job Description:
    {jd_text}
    """

    # Prompt to analyze the resume in depth
    resume_analysis_prompt = """
    You are an experienced HR evaluator. Extract detailed information from the provided resume:
    - Core Skills (technical, soft skills, tools, and technologies)
    - Certifications or Licenses (if any)
    - Total Years of Experience (and relevance to the job)
    - Highest Education Level (degree and field of study)
    - Notable Achievements or Highlights (projects, leadership, etc.)
    - Mention of any specific tools, software, or technologies
    Provide this information in a structured format.
    """

    # Prompt to compare JD and resume thoroughly
    comparison_prompt = """
    Based on the details extracted from the job description and the resume, perform a thorough comparison and analysis:
    - Calculate the percentage match based on skills, experience, certifications, and education
    - Identify any missing elements or gaps in skills, experience, or qualifications from the resume
    - Highlight the strengths of the candidate based on the job requirements
    - Provide a final assessment on the suitability of the candidate for the role
    - Suggest whether the candidate should be considered for the role, and what areas may need improvement
    Provide the analysis in a structured and concise format.
    """
    
    return jd_analysis_prompt, resume_analysis_prompt, comparison_prompt
