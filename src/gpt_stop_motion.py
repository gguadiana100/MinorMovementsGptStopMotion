"""This module provides a collection of methods for generating a stop motion video.
"""

from openai import OpenAI
import base64

gpt_client = OpenAI()

def request_gpt_image(client: OpenAI, image_prompt: str) -> list[dict]:
    created_image_response = client.response.create(
        model = "gpt-4.1-mini",
        input = image_prompt,
        tools = [{"type": "image_generation"}],
    )
    return created_image_response

def create_image_from_gpt_response(image_response):
    image_data = [
        output.result
        for output in image_response.output
        if output.type == "image_generation_call"
    ]
    return image_data

def create_stop_motion_images(image_prompts: list[str]):
    for index, image_prompt in enumerate(image_prompts):
        image_gpt_response = request_gpt_image(image_prompt)
    pass



