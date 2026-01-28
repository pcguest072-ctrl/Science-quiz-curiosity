import streamlit as st
import pandas as pd
import os

# ---------------- SETTINGS ----------------
st.set_page_config(page_title="Science Quiz - Curiosity", page_icon="🧪")

LEADERBOARD_FILE = "leaderboard.csv"

# ---------------- LEADERBOARD FUNCTIONS ----------------
def save_score(name, score):
    if os.path.exists(LEADERBOARD_FILE):
        df = pd.read_csv(LEADERBOARD_FILE)
    else:
        df = pd.DataFrame(columns=["Name", "Score"])

    df.loc[len(df)] = [name, score]
    df.to_csv(LEADERBOARD_FILE, index=False)

def show_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        df = pd.read_csv(LEADERBOARD_FILE)
        df = df.sort_values(by="Score", ascending=False)
        st.subheader("🏆 Leaderboard")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("No leaderboard data yet.")

# ---------------- QUESTIONS ----------------
questions = [
    {
        "q": "Plants prepare their food by?",
        "options": ["Respiration", "Photosynthesis", "Digestion", "Transpiration"],
        "answer": "Photosynthesis"
    },
    {
        "q": "Force is measured in?",
        "options": ["Joule", "Pascal", "Newton", "Watt"],
        "answer": "Newton"
    },
    {
        "q": "Human heart has how many chambers?",
        "options": ["2", "3", "4", "5"],
        "answer": "4"
    },
    {
        "q": "The boiling point of water is?",
        "options": ["50°C", "100°C", "150°C", "0°C"],
        "answer": "100°C"
    },
    {
        "q": "True or False: Air has weight",
        "options": ["True", "False"],
        "answer": "True"
    }
]

# ---------------- SESSION STATES ----------------
if "page" not in st.session_state:
    st.session_state.page = "start"

if "score" not in st.session_state:
    st.session_state.score = 0

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# ---------------- START PAGE ----------------
if st.session_state.page == "start":
    st.title("🧪 Science Quiz – Curiosity")
    st.write("Class 8 Science Quiz")

    name = st.text_input("Enter Student Name")

    if st.button("Start Quiz"):
        if name.strip() == "":
            st.warning("Please enter your name")
        else:
            st.session_state.name = name
            st.session_state.page = "quiz"
            st.experimental_rerun()

# ---------------- QUIZ PAGE ----------------
elif st.session_state.page == "quiz":
    q = questions[st.session_state.q_index]

    st.subheader(f"Question {st.session_state.q_index + 1}")
    st.write(q["q"])

    choice = st.radio("Choose answer:", q["options"])

    if st.button("Submit Answer"):
        if choice == q["answer"]:
            st.success("Correct ✅")
            st.session_state.score += 1
        else:
            st.error(f"Wrong ❌ Correct answer: {q['answer']}")

        st.session_state.q_index += 1

        if st.session_state.q_index >= len(questions):
            st.session_state.page = "result"

        st.experimental_rerun()

# ---------------- RESULT PAGE ----------------
elif st.session_state.page == "result":
    st.title("📊 Result")

    total = len(questions)
    score = st.session_state.score

    st.write(f"**Student Name:** {st.session_state.name}")
    st.write(f"**Score:** {score} / {total}")

    percentage = (score / total) * 100
    st.write(f"**Percentage:** {percentage:.2f}%")

    if percentage >= 40:
        st.success("🎉 Pass")
    else:
        st.error("❌ Fail")

    save_score(st.session_state.name, score)

    show_leaderboard()

    if st.button("Restart Quiz"):
        st.session_state.page = "start"
        st.session_state.score = 0
        st.session_state.q_index = 0
        st.experimental_rerun()
﻿
