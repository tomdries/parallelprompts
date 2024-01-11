from api_request_parallel_processor import process_api_requests_from_file
import asyncio
import os 
# load dotenv
from dotenv import load_dotenv
import logging
load_dotenv()

requests_filepath = 'example_requests_to_parallel_process.jsonl'
request_url = "https://api.openai.com/v1/embeddings"
api_key=os.getenv("OPENAI_API_KEY")
max_requests_per_minute=3_000 * 0.5
max_tokens_per_minute = 250_000 * 0.5
token_encoding_name = "cl100k_base"
max_attempts = 5
logging_level = logging.INFO
save_filepath = requests_filepath.replace(".jsonl", "_results.jsonl")

# run script
asyncio.run(
    process_api_requests_from_file(
        requests_filepath=requests_filepath,
        save_filepath=save_filepath,
        request_url=request_url,
        api_key=api_key,
        max_requests_per_minute=float(max_requests_per_minute),
        max_tokens_per_minute=float(max_tokens_per_minute),
        token_encoding_name=token_encoding_name,
        max_attempts=int(max_attempts),
        logging_level=int(logging_level),
    )
)