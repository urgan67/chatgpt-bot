from openai import AsyncOpenAI

from keys import api_key

client = AsyncOpenAI(api_key=api_key)

default_model = "gpt-3.5-turbo"

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
        
    except Exception as e:
        print(f"Ошибка: {str(e)}") 
    
    return gpt_response

    # return {"gpt_response": gpt_response, "used_tokens": used_tokens}

