import os
import sys
from dotenv import load_dotenv
from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic
import whisper

# Load environment variables from .env file
load_dotenv()

# Initialize Anthropic
anthropic = Anthropic()

# Function to transcribe audio
def transcribe_audio(audio_file, model_name="base"):
    model = whisper.load_model(model_name)  # Load the model
    result = model.transcribe(audio_file, fp16=False)  # Transcribe the audio file
    print("Audio to text done")
    print(". ".join(result["text"].split(". ")[:5]))  # Print the first 5 lines of the transcription

    # Store the transcription in a .txt file with the same name as the audio file
    with open(os.path.splitext(audio_file)[0] + "_raw.txt", "w") as f:
        f.write(result["text"])

    return result["text"]

# Function to create completion
def create_completion(prompt_text):
    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=100000,
        prompt=prompt_text,
    )
    print(". ".join(completion.completion.split(". ")[:5]))  # Print the first 5 sentences of the completion
    return completion.completion

# Function to split conversation
def split_convo(raw_text):
    prompt_text = f"{HUMAN_PROMPT} This is a conversation transcript between two people. Transcript: {raw_text}\n\nBreak it down by speaker, without modifying the content{AI_PROMPT}"
    return create_completion(prompt_text)

# Function to summarize conversation
def summarize(split_text):
    prompt_text = f"{HUMAN_PROMPT} This is a conversation transcript between two people. Transcript: {split_text}\n\nSummarize the conversation by speaker using bullet points{AI_PROMPT}"
    return create_completion(prompt_text)

# Function to create follow up message
def follow_up(split_text):
    prompt_text = f"{HUMAN_PROMPT} This is a conversation transcript between two people. Transcript: {split_text}\n\nBased on the conversation, write a follow up thank you email to the interviewert{AI_PROMPT}"
    return create_completion(prompt_text)

def read_or_create_file(file_path, creation_func, *args):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
    else:
        content = creation_func(*args)
        with open(file_path, "w") as f:
            f.write(content)
    return content

def write_results(audio_file):
    raw_file = os.path.splitext(audio_file)[0] + "_raw.txt"
    result = read_or_create_file(raw_file, transcribe_audio, audio_file)

    split_file = os.path.splitext(audio_file)[0] + "_split.txt"
    split = read_or_create_file(split_file, split_convo, result)

    # Generate Summary based on split
    summary_file = os.path.splitext(audio_file)[0] + "_summary.txt"
    summary = summarize(split)
    follow_up_message = follow_up(split)

    with open(summary_file, "a") as f:
        f.write("\nSummary:\n")
        f.write(summary)
        f.write("\nFollow Up:\n")
        f.write(follow_up_message)

# Main function
if __name__ == "__main__":
    audio_file = sys.argv[1]
    print("Transcribing and summarizing: " + audio_file)
    write_results(audio_file)
