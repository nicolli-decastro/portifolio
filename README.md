# Text Summarizer using OpenAI

Welcome to my text summarization project! This Python script utilizes OpenAI's API, specifically the GPT-3 model, to automatically summarize large texts. By breaking down large volumes of text and intelligently summarizing them, this tool showcases how state-of-the-art AI models can simplify vast information.

## Highlights

- **Chunking Texts:** The script chunks large texts into smaller sections to better handle them using the OpenAI API.
- **Overlap Mechanism:** To ensure continuity and context, there's an overlap mechanism in place.
- **Batch Summarization:** Can summarize multiple .txt files present in a directory.
- **Summary of Summaries:** After summarizing individual files, the script can also provide a "summary of summaries" for an overarching perspective.

## Technical Prerequisites and Libraries
Python 3.x
Required Python libraries: os, glob, requests, tqdm, openai, and nltk.

## Code
The script for the text summarization can be found here: [text_summarizer.py](./text_summarizer.py).

## How It Works
- **API Integration:** This project requires an OpenAI API key. The script fetches this from an environment variable to authenticate and interact with OpenAI's platform.
- **Text Tokenization:** Leveraging the Natural Language Toolkit (NLTK), the script tokenizes input texts, preparing them for processing.
- **Iterative Summarization:** For each .txt file in the specified directory, the script breaks down the text, summarizes each chunk, and then compiles the results into a cohesive summary.
- **Output Generation:** Individual summaries are saved, and finally, a comprehensive "summary of summaries" is generated.

## Portfolio Context
This project serves as a demonstration of integrating external AI-powered services into Python applications and effectively processing large datasets. The overarching aim is to showcase the potential of AI in simplifying and condensing information, making it more accessible and digestible.

## Feedback & Contact
I appreciate your interest in my work! If you have feedback, questions, or just want to connect, feel free to reach out at nicolli.decastro@gmail.com.
