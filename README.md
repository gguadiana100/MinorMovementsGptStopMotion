# Minor Movements Stop Motion Video Creator

This is a Python project that creates stop-motion videos using OpenAI's image generation API. The implementation uses the Responses API with the models GPT-image-1 and GPT-4.1-mini. It creates stop motion video scene prompts using the page content from the book Minor Movements that is in a PDF format. Once all the images are generated, they are put together into an mp4 file.

## Status

This project has been developed using functional testing and does not currently have unit tests or error handling.

## Overview

This tool generates sequential images using an OpenAI GPT model and combines them into stop-motion style videos for book visualization.

## Requirements

- Python 3.8+
- OpenAI API key
- Poppler fpr pdf2image
- Tesseract for pytesseract

## Installation

Create a virtual environment and install the pip libraries using requirements.txt

## Usage

python main.py

## Cost Estimates

It's about $0.20 per frame. For a 60 frames per story with 12 stories, it would be about $144. It's quite expensive!

# Demo Reflections Blog Post
https://www.linkedin.com/posts/gilberto-guadiana_smallleverslab-softwareengineering-openai-activity-7358936991356342272-5bZD 

## License

MIT License