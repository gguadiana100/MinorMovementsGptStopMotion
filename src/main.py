"""This project produces a short series of stop motion images for the book Minor Movements by Gilberto Guadiana
using the GPT image generation api.
"""

import os
from openai import OpenAI

STOP_MOTION_FPS = 12
BOOK_PATH = "MinorMovementsGilbertoGuadiana.pdf"

def main():
    openai_client = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY")
    )

if __name__ == "__main__":
    main()