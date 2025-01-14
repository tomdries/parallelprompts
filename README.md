
Adaptation of parallel processing approach from OpenAI Cookbook, now allowing for parallel image processing.

## for vision:
 ```
python "C:\Users\Tom\Projects\openai-cookbook\examples\api_request_parallel_processor.py" --requests_filepath "input.jsonl" --save_filepath "output4.jsonl" --request_url "https://api.openai.com/v1/chat/completions" --api_key "KEY HERE" --max_requests_per_minute "250" --max_tokens_per_minute "120000" --token_encoding_name "cl100k_base" --max_attempts "5" --logging_level "20" --sort_results    
python api_request_parallel_processor.py --requests_filepath "input.jsonl" --save_filepath "output4.jsonl" --request_url "https://api.openai.com/v1/chat/completions" --api_key "KEY HERE" --max_requests_per_minute "250" --max_tokens_per_minute "120000" --token_encoding_name "cl100k_base" --max_attempts "5" --logging_level "20" --sort_results    
```
