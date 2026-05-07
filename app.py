# to run: chainlit run app.py -w

import os
import uuid
import asyncio
import httpx
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")


async def get_llm_answer(user_input: str) -> str:

    session_id = cl.user_session.get("session_id")

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BACKEND_URL}/api/chat",
            json={
                "message": user_input,
                "session_id": session_id,
            }
        )
        response.raise_for_status()
        data = response.json()

    # Save updated session_id back to user session
    cl.user_session.set("session_id", data["session_id"])

    return data["reply"]


@cl.on_chat_start
async def on_chat_start():
    # Generate unique session ID once per user conversation
    cl.user_session.set("session_id", str(uuid.uuid4()))


@cl.on_message
async def process_user_message(message: cl.Message):

    llm_message = cl.Message(content="Thinking...")
    await llm_message.send()

    try:
        final_reply = await get_llm_answer(message.content)

    except httpx.TimeoutException:
        final_reply = "⏱️ Backend response timeout. Please try again."

    except httpx.ConnectError:
        final_reply = f"❌ Backend se connect nahi ho pa raha. Check karo ke backend {BACKEND_URL} pe chal raha hai."

    except Exception as e:
        final_reply = f"❌ Kuch ghalat hua: {str(e)}"

    llm_message.content = final_reply
    await llm_message.update()
