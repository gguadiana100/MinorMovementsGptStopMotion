"""This module provides a collection of methods for generating a stop motion video.
"""

from openai import OpenAI
from openai.types.responses import Response
import base64

def request_gpt_image(client: OpenAI, image_prompt: str) -> Response:
    created_image_response = client.responses.create(
        model = "gpt-4.1-mini",
        input = image_prompt,
        tools = [{"type": "image_generation"}],
    )
    return created_image_response

def request_iterated_gpt_image(client: OpenAI, image_prompt: str, gpt_image_response_id: str | None) -> Response | None:
    if gpt_image_response_id is None: 
        return None

    created_image_response = client.responses.create(
        model = "gpt-4.1-mini",
        previous_response_id = gpt_image_response_id,
        input = image_prompt,
        tools = [{"type": "image_generation"}],
    )
    return created_image_response

def get_image_from_gpt_response(image_response: Response) -> list:
    image_data = [
        output.result
        for output in image_response.output
        if output.type == "image_generation_call"
    ]
    return image_data

def save_image_from_gpt_image_data(image_name: str, image_data: list[str]) -> None:
    if image_data:
        image_base64 = image_data[0]
        with open(image_name, "wb") as f:
            f.write(base64.b64decode(image_base64))

def get_stop_motion_frame_image_prompt(scene_description_prompt: str, duration_in_seconds: int,
                                       fps: int, current_frame: int) -> str:
    prompt = f"""Please generate a stop motion image for frame {current_frame} that is one of a sequence of images for a stop motion
    video that is {duration_in_seconds} seconds long with {fps} frames per second. The prompt below is the overall scene description.
    When iterating on previous images, do not change the background so that there is continuity between frames. Only change the image
    to show movement of objects or characters as directed by the following prompt.

    {scene_description_prompt}
    """
    return prompt

def request_stop_motion_gpt_images(client: OpenAI, scene_description_prompt: str, 
                                   duration_in_seconds: int, fps: int) -> list[Response]:
    image_responses = []
    total_frames = duration_in_seconds * fps
    latest_response_id = ""
    for current_frame in range(1, total_frames + 1):
        image_prompt = get_stop_motion_frame_image_prompt(scene_description_prompt, duration_in_seconds,
                                                          fps, current_frame)
        if current_frame == 1:
            image_response = request_gpt_image(client, image_prompt)
        else:
            image_response = request_iterated_gpt_image(client, image_prompt, latest_response_id)
        latest_response_id = image_response.id
        image_responses.append(image_response)
    return image_responses

def save_images_from_gpt_image_responses(image_responses: list[Response], image_path_prefix: str) -> None:
    for index in range(0, len(image_responses)):
        image_path = f"{image_path_prefix}_FRAME_{index + 1}"
        image_data = get_image_from_gpt_response(image_responses[0])
        save_image_from_gpt_image_data(image_path, image_data)



