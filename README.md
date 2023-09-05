# audio_summary

 transcribe audio using whisper API, clean up the content using Claude2, and perform other tasks such as find action items, generate summary by speaker, and write follow-up emails

 add `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` to .env file

activate the virtual environment:
`source virtualenv/bin/activate`

run the script:
`python main.py "assets/xxx.mp3"`