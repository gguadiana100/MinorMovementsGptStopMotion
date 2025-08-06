"""This project produces a short series of stop motion images for the book Minor Movements by Gilberto Guadiana
using the GPT image generation api.
"""

import os
import gpt_stop_motion
import gpt_scene_prompts
from openai import OpenAI
from dotenv import load_dotenv

STOP_MOTION_DURATION_IN_SECONDS = 3
STOP_MOTION_FPS = 6
BOOK_PATH = r".\src\MinorMovementsGilbertoGuadiana.pdf"
EXCLUDE_BOOK_PAGES = [0, 1]
IMAGE_PATH_PREFIX = "MINOR_MOVEMENTS_STOP_MOTION"
OUTPUT_DIRECTORY = "output"
VIDEO_NAME = "MINOR_MOVEMENTS_STOP_MOTION_test.mp4"
OUTPUT_VIDEO_PATH = f"{OUTPUT_DIRECTORY}\\{VIDEO_NAME}"

def main():
    load_dotenv()
    openai_client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY")
    )
    stop_motion_scene_descriptions = gpt_scene_prompts.generate_video_scene_descriptions(openai_client, 
                                                                             BOOK_PATH, 
                                                                             EXCLUDE_BOOK_PAGES,
                                                                             STOP_MOTION_DURATION_IN_SECONDS,
                                                                             STOP_MOTION_FPS)
    for page_index, video_scene_descriptions in stop_motion_scene_descriptions.items():
        image_responses = gpt_stop_motion.request_stop_motion_gpt_images(openai_client, video_scene_descriptions,
                                                                         STOP_MOTION_DURATION_IN_SECONDS, STOP_MOTION_FPS)
        stop_motion_frame_path_prefix = f"{IMAGE_PATH_PREFIX}_PAGE_{page_index}"
        gpt_stop_motion.save_stop_motion_frames_from_gpt_image_responses(image_responses, stop_motion_frame_path_prefix)
    gpt_stop_motion.create_stop_motion_video_from_directory(OUTPUT_DIRECTORY, STOP_MOTION_FPS, OUTPUT_VIDEO_PATH)

if __name__ == "__main__":
    main()