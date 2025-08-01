"""This project produces a short series of stop motion images for the book Minor Movements by Gilberto Guadiana
using the GPT image generation api.
"""

import os
import gpt_stop_motion
import gpt_scene_prompts
from openai import OpenAI
from dotenv import load_dotenv

STOP_MOTION_FPS = 12
BOOK_PATH = r".\src\MinorMovementsGilbertoGuadiana.pdf"
EXCLUDE_BOOK_PAGES = [0, 1]

def main():
    load_dotenv()
    openai_client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY")
    )
    scene_descriptions = gpt_scene_prompts.generate_video_scene_descriptions(openai_client, 
                                                                             BOOK_PATH, 
                                                                             EXCLUDE_BOOK_PAGES,
                                                                             STOP_MOTION_FPS)

if __name__ == "__main__":
    main()