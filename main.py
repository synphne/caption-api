"""Streamlit front-end for SynPhNe GPT Assistant.
   Follows the API contract:
   caption_type -> one of {informative, carousel, event_announcement, event_summary}
   plus additional kwargs as required.
"""
import os
import streamlit as st
import openai
from dotenv import load_dotenv

from prompts import (
    linked_in_informative,
    linked_in_carousel,
    event_announcement,
    event_summary,
)

# -----------------------
# 1 · Config & Key
# -----------------------
load_dotenv()
openai.api_key= st.secrets["API_KEY"]

st.set_page_config(page_title="SynPhNe GPT Assistant", layout="centered")

SYSTEM_MESSAGE = (
    "You are SynPhNe’s brand voice and clinical marketing writer.\n"
    "SynPhNe is a U.S.-based medical device company that helps stroke and TBI patients recover beyond perceived plateaus.\n"
    "Our system is the only neuro-integrative wearable that trains cognition and motor function together in real time using EEG and EMG data.\n\n"
    "Your job is to write content that reflects our core values: scientific integrity, patient-first recovery, clinical clarity, and outcome-driven innovation.\n\n"
    "Always:\n"
    "• Sound clear, professional, and measured\n"
    "• Lead with facts, not hype\n"
    "• Emphasize objective data, functional recovery, and clinical use cases\n"
    "• Use plain English that clinicians, therapists, and patient advocates can understand\n"
    "• Reflect a hopeful but realistic tone grounded in evidence\n"
    "• Use American English spelling\n\n"
    "Never:\n"
    "• Use too many commas in the caption, it should be easy to read\n"
    "• Use the em dash\n"
    "• Use unsubstantiated claims or emotional buzzwords\n"
    "• Over-promise outcomes or exaggerate capabilities\n"
    "• Use casual emojis or overly casual language\n"
    "• Use phrases like 'According to Research', be specific and direct\n"
    "• Use words like 'game-changer' or 'breakthrough', it represents false promises\n"
    "• Use fluffy language like 'Together we can beat Stroke'\n"
    "• Reference holistic, spiritual, or futuristic themes\n\n"
)

# map caption_type → prompt-template function
TEMPLATE_MAP = {
    "informative": linked_in_informative,
    "carousel": linked_in_carousel,
    "event_announcement": event_announcement,
    "event_summary": event_summary,
}

# -----------------------
# 2 · UI
# -----------------------
st.title("🧠 SynPhNe Content Assistant")
st.markdown("Generate brand-perfect LinkedIn captions in seconds.")

caption_type = st.selectbox(
    "Select caption type",
    options=[
        "informative",
        "carousel",
        "event_announcement",
        "event_summary",
    ],
    format_func=lambda x: x.replace("_", " ").title(),
)

# universal field
topic = st.text_input("Topic (for informative or carousel)")

# event-specific inputs
if caption_type.startswith("event"):
    event_name = st.text_input("Event name")

if caption_type == "event_announcement":
    date = st.text_input("Date (e.g. 12 June 2025)")
    cta = st.text_input("Call-to-action text", value="Register now →")
else:
    date = cta = None

if caption_type == "event_summary":
    key_takeaway = st.text_input("Key takeaway")
else:
    key_takeaway = None

# -----------------------
# 3 · Build kwargs respecting the contract
# -----------------------
kwargs = {}
if topic:
    kwargs["topic"] = topic
if caption_type.startswith("event"):
    kwargs["event_name"] = event_name
if caption_type == "event_announcement":
    kwargs.update({"date": date, "cta": cta})
if caption_type == "event_summary":
    kwargs["key_takeaway"] = key_takeaway

# -----------------------
# 4 · Generate caption
# -----------------------
if st.button("Generate caption"):
    # quick validation
    missing = [k for k, v in kwargs.items() if v == ""]
    if caption_type.startswith("event") and not kwargs.get("event_name"):
        st.warning("Please enter an event name.")
    elif missing:
        st.warning("Please fill in all required fields.")
    else:
        prompt = TEMPLATE_MAP[caption_type](**kwargs)
        with st.expander("Prompt sent to GPT", expanded=False):
            st.code(prompt, language="text")

        with st.spinner("Writing in SynPhNe’s voice…"):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": SYSTEM_MESSAGE},
                        {"role": "user", "content": prompt},
                    ],
                )
                caption = response["choices"][0]["message"]["content"].strip()
                st.success("Caption ready!")
                st.text_area("Output", caption, height=180)
            except Exception as e:
                st.error(f"GPT error: {e}")
