# run: chainlit run app.py -w

import chainlit as cl

@cl.on_message
async def process_user_message(message: cl.Message):
    reply_text = f"You said: {message.content}"
    
    await cl.Message(content=reply_text).send()  
