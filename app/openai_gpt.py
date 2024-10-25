from openai import AsyncOpenAI

from keys import api_key

client = AsyncOpenAI(api_key=api_key)

default_model = 'gpt-4o-mini-2024-07-18'

# price = {                              # при курсе 1$ = 100 руб.
#     'gpt-4-turbo': 0.08,               # 7.22 руб.
#     'gpt-4-turbo-2024-04-09': 0.08,    # 7.22 руб.
#     'tts-1': 0.01,                     # 1 руб.
#     'tts-1-1106': 0.01,                # 1 руб.
#     'chatgpt-4o-latest': 0.04,         # 4 руб.
#     'dall-e-2': 0.08,                  # 7.22 руб.
#     'whisper-1': 0.006,                # 0.6 руб.
#     'gpt-4-turbo-preview': 0.08,       # 7.22 руб.
#     'gpt-3.5-turbo-instruct': 0.005,   # 0.5 руб.
#     'gpt-4-0125-preview': 0.08,        # 7.22 руб.
#     'gpt-3.5-turbo-0125': 0.004,       # 0.4 руб.
#     'gpt-4o-2024-08-06': 0.04,         # 4 руб.
#     'gpt-3.5-turbo': 0.0015,           # 0.15 руб.
#     'gpt-4o': 0.04,                    # 4 руб.
#     'babbage-002': 0.002,              # 0.2 руб.
#     'davinci-002': 0.03,               # 3 руб.
#     'gpt-4o-realtime-preview-2024-10-01': 0.05,  # 5 руб.
#     'dall-e-3': 0.09,                  # 8.13 руб.
#     'gpt-4o-realtime-preview': 0.05,   # 5 руб.
#     'gpt-4o-mini': 0.0015,             # 0.15 руб.
#     'gpt-4o-2024-05-13': 0.04,         # 4 руб.
#     'gpt-4o-mini-2024-07-18': 0.0015,  # 0.15 руб.
#     'gpt-4o-audio-preview-2024-10-01': 0.02,  # 2 руб.
#     'gpt-4o-audio-preview': 0.02,      # 2 руб.
#     'tts-1-hd': 0.015,                 # 1.5 руб.
#     'tts-1-hd-1106': 0.015,            # 1.5 руб.
#     'gpt-4-1106-preview': 0.08,        # 7.22 руб.
#     'text-embedding-ada-002': 0.0008,  # 0.08 руб.
#     'gpt-3.5-turbo-16k': 0.004,        # 0.4 руб.
#     'text-embedding-3-small': 0.0005,  # 0.05 руб.
#     'text-embedding-3-large': 0.003,   # 0.3 руб.
#     'gpt-3.5-turbo-1106': 0.004,       # 0.4 руб.
#     'gpt-4-0613': 0.18,                # 16.24 руб.
#     'gpt-4': 0.18,                     # 16.24 руб.
#     'gpt-3.5-turbo-instruct-0914': 0.005,  # 0.5 руб.
# }




# @dp.message(F.content_type.in_({'text'}))
async def question_openai(text, model):
    if not model:
        model = default_model
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": text}],
        )

        gpt_response = response.choices[0].message.content.strip()
        total_tokens = response.usage.total_tokens
        
    except Exception as e:
        print(f"Ошибка: {str(e)}") 
    
    # return gpt_response
    return {"gpt_response": gpt_response, "total_tokens": total_tokens, "model": model}

