from openai import AsyncOpenAI

from keys import api_key

client = AsyncOpenAI(api_key=api_key)

default_model = 'gpt-4o-mini-2024-07-18'



# @dp.message(F.content_type.in_({'text'}))
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
    
 
    

