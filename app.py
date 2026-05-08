# to run: chainlit run app.py -w

import os
import uuid
import asyncio
import httpx
import re
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")
ROLL_PATTERN = re.compile(r"\b2\dK-\d{4}\b", re.IGNORECASE)
ROLL_PLACEHOLDER_PATTERN = re.compile(r"\b2xk-xxxx\b", re.IGNORECASE)


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


def _format_seating_response(payload: dict) -> str:
    records = payload.get("records", [])
    if not records:
        return "Seating plan nahi mila. Roll number dobara check karein."

    roll_no = records[0].get("roll_no", "")
    name = records[0].get("name", "")
    header = f"Seating plan for {name} ({roll_no}):"
    lines = [header, ""]

    for idx, r in enumerate(records, start=1):
        lines.append(f"{idx}. {r.get('course_code', '')} - {r.get('course_name', '')}")
        lines.append(f"   Day: {r.get('day', '')}")
        lines.append(f"   Time: {r.get('time', '')}")
        lines.append(f"   Seat: {r.get('seat', '')}")
        teacher = r.get("teacher", "")
        if teacher:
            lines.append(f"   Teacher: {teacher}")
        lines.append("")

    return "\n".join(lines).strip()


async def get_seating_plan(user_input: str) -> str:
    if ROLL_PLACEHOLDER_PATTERN.search(user_input):
        return "Please replace X with digits. Example: 24K-0867"
    match = ROLL_PATTERN.search(user_input)
    if not match:
        return ""

    roll_no = match.group(0).upper()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(f"{BACKEND_URL}/exam/seat/{roll_no}")
        response.raise_for_status()
        data = response.json()

    if "records" not in data:
        return "Seating plan nahi mila. Roll number dobara check karein."

    return _format_seating_response(data)


@cl.on_chat_start
async def on_chat_start():
    # Generate unique session ID once per user conversation
    cl.user_session.set("session_id", str(uuid.uuid4()))


@cl.on_message
async def process_user_message(message: cl.Message):

    llm_message = cl.Message(content="Thinking...")
    await llm_message.send()

    try:
        seating_reply = await get_seating_plan(message.content)
        if seating_reply:
            final_reply = seating_reply
        else:
            final_reply = await get_llm_answer(message.content)

    except httpx.TimeoutException:
        final_reply = "⏱️ Backend response timeout. Please try again."

    except httpx.ConnectError:
        final_reply = f"❌ Backend se connect nahi ho pa raha. Check karo ke backend {BACKEND_URL} pe chal raha hai."

    except Exception as e:
        final_reply = f"❌ Kuch ghalat hua: {str(e)}"

    llm_message.content = final_reply
    await llm_message.update()
