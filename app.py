# to run: chainlit run app.py -w

import chainlit as cl
import asyncio


async def get_llm_answer(user_input: str) -> str:

    # TODO: Replace this with a real API call to your FastAPI backend

    # 1 second delay to test frontend
    await asyncio.sleep(2)
    
    # fake response for testing
    return f"[Backend] You said: '{user_input}'"


@cl.on_message
async def process_user_message(message: cl.Message):
    
    llm_message = cl.Message(content="Thinking...")
    await llm_message.send()
    
    final_reply = await get_llm_answer(message.content)
    
    llm_message.content = final_reply
    await llm_message.update()
