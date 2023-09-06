# Text and Audio Summarizer using OpenAI
Welcome to my AI-powered transcription and summarization project! This set of Python scripts is designed to transcribe audio from customer interviews during exploratory research, followed by a summarization step to analyze the transcriptions without human bias, allowing for faster and more objective analysis of qualitative data.

## Highlights:
- **Audio Transcription:** Convert customer interviews in audio format into readable text using OpenAI's Whisper model.
- **Chunking Mechanism:** Large transcribed texts are broken down into smaller sections to maximize the efficiency and effectiveness of the OpenAI API.
- **Overlap Mechanism:** An overlap mechanism ensures continuity and maintains context between chunks of transcribed text.
- **Batch Summarization:** Designed to handle and summarize multiple .txt files from a specified directory.
- **Summary of Summaries:** After individual summaries are generated, the script crafts a "summary of summaries", offering a high-level perspective on all provided transcriptions.

## Technical Prerequisites and Libraries:
Python 3.x
Required Python libraries: os, glob, requests, tqdm, openai, and nltk.

## How It Works:
- **API Integration:** These projects require an OpenAI API key. The scripts fetch this key from an environment variable to authenticate and interact with OpenAI's platform.
- **Audio to Text:** The scripts transcribe audio interviews using OpenAI's Whisper model, converting voice data into text for further processing.
- **Text Tokenization:** Leveraging the Natural Language Toolkit (NLTK), the scripts tokenize the transcribed texts, preparing them for summarization.
- **Iterative Summarization:** For each transcribed .txt file, the script breaks down the text, summarizes each chunk, and then combines the results into a concise summary.
- **Output Generation:** Individual summaries are saved, and a comprehensive "summary of summaries" is produced.

## Portfolio Context:
This project serves as a showcase of integrating external AI-powered services into Python applications, effectively processing vast datasets from voice to summarized text. The primary goal is to highlight the potential of AI in transcribing, simplifying, and condensing information, turning a qualitative dataset into actionable insights.

## Feedback & Contact:
I appreciate your interest in my work! If you have feedback, or questions, or wish to connect, please don't hesitate to reach out.
