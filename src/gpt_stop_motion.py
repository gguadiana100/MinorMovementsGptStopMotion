"""This module provides a collection of methods for generating a stop motion video.
"""

from openai import OpenAI
from openai.types.responses import Response
import base64
import os
import moviepy.video.io.ImageSequenceClip
import re

def request_gpt_image(client: OpenAI, image_prompt: str) -> Response:
    created_image_response = client.responses.create(
        model = "gpt-4.1-mini",
        input = image_prompt,
        tools = [
            {
                "type": "image_generation",
                "size": "1024x1024",
                "quality": "high",
                "background": "opaque"
            }
        ],
    )
    return created_image_response

def request_iterated_gpt_image(client: OpenAI, image_prompt: str, gpt_image_response_id: str | None) -> Response | None:
    if gpt_image_response_id is None: 
        return None

    created_image_response = client.responses.create(
        model = "gpt-4.1-mini",
        previous_response_id = gpt_image_response_id,
        input = image_prompt,
        tools = [
            {
                "type": "image_generation",
                "size": "1024x1024",
                "quality": "high",
                "background": "opaque"
            }
        ],
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
    When iterating on previous images, focus on showing the movement described in the scene and keep image continuity high.

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

def save_stop_motion_frames_from_gpt_image_responses(image_responses: list[Response], image_path_prefix: str) -> None:
    for index in range(0, len(image_responses)):
        image_path = f"{image_path_prefix}_FRAME_{index + 1}.png"
        image_data = get_image_from_gpt_response(image_responses[index])
        save_image_from_gpt_image_data(image_path, image_data)

def page_and_frame_from_frame_image_name(image_name: str) -> tuple[int, int]:
    match = re.search(r"_(\d+)_FRAME_(\d+).png", image_name)
    page_number = int(match.group(1))
    frame = int(match.group(2))
    return (page_number, frame)

# Adapted from https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
def create_stop_motion_video_from_directory(image_directory: str, fps: int, video_path: str) -> None:
    png_image_paths = [os.path.join(image_directory, image_name) for image_name in os.listdir(image_directory)
                       if image_name.endswith(".png")]
    sorted_frames = sorted(png_image_paths, key=page_and_frame_from_frame_image_name)
    stop_motion_video = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(sorted_frames, fps=fps)
    stop_motion_video.write_videofile(video_path)
