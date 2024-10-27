from openai import AsyncOpenAI

from keys import api_key

client = AsyncOpenAI(api_key=api_key)

# # @dp.message(F.content_type.in_({'text'}))
async def question_openai(text, model):
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": text}],
        )

        gpt_response = response.choices[0].message.content.strip()
        total_tokens = response.usage.total_tokens
        return {"gpt_response": gpt_response, "total_tokens": total_tokens}#, "model": model}
    except:
        return {"gpt_response": gpt_response.text, "total_tokens": 0}#, "model": model}
    
 
    
# async def question_openai(text, model):
#     try:
#         response = await client.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": text}]
#         )
#         gpt_response = response.choices[0].message["content"]
#         total_tokens = response.usage["total_tokens"]
#         return {"gpt_response": gpt_response, "total_tokens": total_tokens}
#     except Exception as e:
#         print(f"Error during OpenAI API call: {e}")
#         return {"gpt_response": None, "total_tokens": 0}
