# Import necessary libraries
import os
import glob
import requests
from tqdm import tqdm
import openai
import nltk
from nltk.tokenize import word_tokenize

# Download the 'punkt' tokenizer models for the word_tokenize function from NLTK
nltk.download('punkt')

# Set OpenAI API key from environment variables
OPENAI_API_KEY = os.environ['open_ai']
openai.api_key = OPENAI_API_KEY


def break_up_file(tokens, chunk_size, overlap_size):
    """
    Yield chunks of tokens with a given size and overlap.

    Parameters:
    - tokens: list of tokens
    - chunk_size: size of each chunk
    - overlap_size: size of overlap between consecutive chunks
    """
    if len(tokens) <= chunk_size:
        yield tokens
    else:
        chunk = tokens[:chunk_size]
        yield chunk
        yield from break_up_file(tokens[chunk_size - overlap_size:], chunk_size, overlap_size)


def chunk_text(text, chunk_size=8000, overlap_size=0):
    """
    Breaks the given text into chunks using word_tokenize.

    Parameters:
    - text: input text
    - chunk_size: size of each chunk
    - overlap_size: size of overlap between consecutive chunks

    Returns:
    - List of chunked texts
    """
    tokens = word_tokenize(text)
    token_chunks = list(break_up_file(tokens, chunk_size, overlap_size))
    chunks = [" ".join(token_chunk) for token_chunk in token_chunks]
    return chunks


def summarize_text(text):
    """
    Summarizes the given text using OpenAI API.

    Parameters:
    - text: input text to be summarized

    Returns:
    - A summarized text
    """
    # Read prompt instructions from a file
    with open("prompt.txt", "r") as prompt_file:
        system_message = prompt_file.read()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[{
                "role": "system",
                "content": system_message},
                {"role": "user", "content": f"Avalie o texto a seguir com base nas suas instruções: {text}"}],
            max_tokens=700,
            temperature=0.7,
            # Additional potential parameters are commented out
            # top_p=0.95,
            # frequency_penalty=0,
            # presence_penalty=0,
            # stop=None
        )
        # Extract summarized content from the response
        summary = response.choices[0].message.content.strip()
        return summary


def generate_summary_of_summaries(summaries):
    """
    Generates a summary from a list of summaries.

    Parameters:
    - summaries: list of summarized texts

    Returns:
    - A summary of summaries
    """
    summaries_text = "\n\n".join(summaries)
    return summarize_text(summaries_text)


def main():
    """
    Main function to:
    1. Prompt user for directory containing text files
    2. Summarize each file
    3. Save individual summaries and a combined summary of summaries
    """
    # Get input directory from user
    input_folder = input("Digite o caminho da pasta contendo os arquivos .txt: ")

    # Ensure output directory exists
    os.makedirs("Output", exist_ok=True)

    all_summaries = []

    # Loop through each .txt file in the specified directory
    for input_file in glob.glob(os.path.join(input_folder, "*.txt")):
        with open(input_file, "r") as f:
            article_text = f.read()
            article_chunks = chunk_text(article_text)
            article_summary = ""

        # Summarize each chunk of the article
        for chunk in tqdm(article_chunks, desc=f"Summarizing {os.path.basename(input_file)}"):
            chunk_summary = summarize_text(chunk)
            article_summary += " " + chunk_summary
            all_summaries.append(article_summary.strip())

            # Save summarized article to the output directory
            output_file = os.path.join("Output", os.path.basename(input_file).replace(".txt", "_summary.txt"))
            with open(output_file, "w") as f:
                f.write(article_summary.strip())
                print(f"Article summary saved to {output_file}")

        # Create a combined summary from all article summaries
        summary_of_summaries = generate_summary_of_summaries(all_summaries)

    # Save the combined summary to the output directory
    with open(os.path.join
