"""This module provides a collection of methods for generating stop motion video scene prompts
from the text in a PDF that has scannable text.
"""

import pytesseract
from pdf2image import convert_from_path
from openai import OpenAI
from openai.types.responses import Response

# Base prompt generated using Claude LLM
def create_stop_motion_prompt(story_text: str, duration_in_seconds: int = 5, fps: int = 12) -> str: 
    prompt = f"""You are a creative director specializing in stop-motion animation for short story fiction. I will provide you with text from the short story, and you need to create a detailed concept for a 5-second stop-motion scene that captures the essence of that short story.

    Please provide your response in the following structured format:

    **SCENE CONCEPT:**
    [Brief 1-2 sentence description of the key moment to animate]

    **VISUAL STYLE:**
    [Art style - clay animation, color palette, lighting mood - suitable for stop-motion, background - solid background]

    **CHARACTER DESCRIPTION:**
    [Detailed physical description of main character(s) for consistency across frames]

    **SETTING DESCRIPTION:**
    [Detailed description of the environment, props, and background elements]

    **FRAME BY FRAME ANIMATION BREAKDOWN:**
    - Frame 1: [What happens in frame 1]
    - Frame 2: [What happens in frame 2]
    - Frame N: [What happens in frame N]
    [Include an entry for each of the {fps*duration_in_seconds} frames. Each frame should feature the main character(s).
     Also, detail the exact changes that are needed to ensure image continuity and detailed movements. Do not batch entries.
     There should be {fps*duration_in_seconds} entries.]
    Total frames needed: {fps*duration_in_seconds} frames

    **KEY POSES/MOMENTS:**
    [3-4 specific keyframe descriptions that would be most important to capture]

    **CAMERA ANGLE:**
    [Describe the perspective and any camera movement]

    **MOOD/EMOTION:**
    [The primary feeling this scene should convey]

    Requirements:
    - Keep character designs simple but distinctive for stop-motion consistency
    - Focus on one clear, engaging action or moment
    - Ensure the scene has a clear beginning, middle, and end within {duration_in_seconds} seconds
    - Consider lighting and staging that would work well for stop-motion photography
    - Make it visually compelling for both children and adults

    Story text to adapt:
    {story_text}
    """
    return prompt

# Method from https://stackoverflow.com/questions/45480280/convert-scanned-pdf-to-text-python
def extract_pdf_text_per_page_pytesseract(pdf_path: str) -> dict[int,str]:
    pdf_page_index_to_text = {}
    pages = convert_from_path(pdf_path)
    for page_index, image_blob in enumerate(pages):
        page_text = pytesseract.image_to_string(image_blob, lang="eng")
        pdf_page_index_to_text[page_index] = page_text
    return pdf_page_index_to_text

def request_gpt_text_response(client: OpenAI, prompt: str) -> Response:
    response = client.responses.create(
        model = "gpt-4.1-mini",
        input = prompt
    )
    return response

def generate_video_scene_descriptions(client: OpenAI, pdf_path: str, excluded_pages: list[int],
                                      duration_in_seconds: int, fps: int = 12) -> dict[int, str]:
    pdf_page_index_to_video_scene_description = {}
    pdf_page_index_to_text = extract_pdf_text_per_page_pytesseract(pdf_path)
    for page_index, story_text in pdf_page_index_to_text.items():
        if page_index in excluded_pages:
            continue
        stop_motion_prompt = create_stop_motion_prompt(story_text, duration_in_seconds, fps)
        video_scene_description_response = request_gpt_text_response(client, stop_motion_prompt)
        video_scene_description = video_scene_description_response.output_text
        pdf_page_index_to_video_scene_description[page_index] = video_scene_description
    return pdf_page_index_to_video_scene_description


    
