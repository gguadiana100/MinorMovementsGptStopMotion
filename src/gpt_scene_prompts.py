"""This module provides a collection of methods for generating scene prompts from the text in a PDF.
"""

import PyPDF2
from openai import OpenAI

# Base prompt generated using Claude LLM
def create_stop_motion_prompt(story_text: str, fps: int = 12): 
    prompt = f"""You are a creative director specializing in stop-motion animation for short story fiction. I will provide you with text from the short story, and you need to create a detailed concept for a 5-second stop-motion scene that captures the essence of that short story.

    Please provide your response in the following structured format:

    **SCENE CONCEPT:**
    [Brief 1-2 sentence description of the key moment to animate]

    **VISUAL STYLE:**
    [Art style, color palette, lighting mood - suitable for stop-motion]

    **CHARACTER DESCRIPTION:**
    [Detailed physical description of main character(s) for consistency across frames]

    **SETTING DESCRIPTION:**
    [Detailed description of the environment, props, and background elements]

    **5-SECOND ANIMATION BREAKDOWN:**
    - Second 1: [What happens in frames 1-{fps}]
    - Second 2: [What happens in frames {fps+1}-{fps*2}]
    - Second 3: [What happens in frames {fps*2+1}-{fps*3}] 
    - Second 4: [What happens in frames {fps*3+1}-{fps*4}]
    - Second 5: [What happens in frames {fps*4+1}-{fps*5}]
    Total frames needed: {fps*5} frames

    **KEY POSES/MOMENTS:**
    [3-4 specific keyframe descriptions that would be most important to capture]

    **CAMERA ANGLE:**
    [Describe the perspective and any camera movement]

    **MOOD/EMOTION:**
    [The primary feeling this scene should convey]

    Requirements:
    - Keep character designs simple but distinctive for stop-motion consistency
    - Focus on one clear, engaging action or moment
    - Ensure the scene has a clear beginning, middle, and end within 5 seconds
    - Consider lighting and staging that would work well for stop-motion photography
    - Make it visually compelling for both children and adults

    Story text to adapt:
    {story_text}
    """
    return prompt

def extract_pdf_text_per_page_pypdf2(pdf_path: str) -> dict[int,str]:
    pdf_page_index_to_text = {}
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_pages = len(pdf_reader.pages)
        for page_index in range(pdf_pages):
            pdf_page_index_to_text[page_index] = pdf_reader.pages[page_index].extract_text()
    return pdf_page_index_to_text

def request_gpt_text_response(client: OpenAI, prompt: str) -> list[dict]:
    response = client.responses.create(
        model = "gpt-4.1-mini",
        input = prompt
    )
    return response

def generate_video_scene_descriptions(client: OpenAI, pdf_path: str, fps: int = 12) -> dict[int, str]:
    pdf_page_index_to_video_scene_description = {}
    pdf_page_index_to_text = extract_pdf_text_per_page_pypdf2(pdf_path)
    for page_index, story_text in pdf_page_index_to_text.items():
        stop_motion_prompt = create_stop_motion_prompt(stop_motion_prompt, fps)
        video_scene_description_response = request_gpt_text_response(client, stop_motion_prompt)
        video_scene_description = video_scene_description_response.output_text
        pdf_page_index_to_video_scene_description[page_index] = video_scene_description


    
