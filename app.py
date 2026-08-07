import streamlit as st
import random
import pandas as pd
import os

# ------------------ PAGE CONFIG -----------------
st.set_page_config(
    page_title="Class 8 Science Quiz – Curiosity 2025",
    page_icon="🧪",
    layout="centered"
)

# ------------------ LEADERBOARD ------------------
LEADERBOARD_FILE = "leaderboard.csv"

def save_score(name, score):
    if os.path.exists(LEADERBOARD_FILE):
        df = pd.read_csv(LEADERBOARD_FILE)
    else:
        df = pd.DataFrame(columns=["Name", "Score"])

    df = pd.concat([df, pd.DataFrame([[name, score]], columns=["Name", "Score"])])
    df.to_csv(LEADERBOARD_FILE, index=False)

# ------------------ QUESTIONS ------------------
questions = [
    {
        "q": "Scientific investigation begins with:",
        "options": ["Observation", "Conclusion", "Guess", "Result"],
        "ans": "Observation"
    },
    {
        "q": "Which tool is used to see microorganisms?",
        "options": ["Microscope", "Telescope", "Binoculars", "Magnifying glass"],
        "ans": "Microscope"
    },
    {
        "q": "Balanced diet contains:",
        "options": ["Only fruits", "Only rice", "All nutrients", "Only milk"],
        "ans": "All nutrients"
    },
    {
        "q": "Vitamin C deficiency causes:",
        "options": ["Rickets", "Scurvy", "Anaemia", "Beriberi"],
        "ans": "Scurvy"
    },
    {
        "q": "Microorganisms live in:",
        "options": ["Air", "Water", "Soil", "All of these"],
        "ans": "All of these"
    },
]

random.shuffle(questions)

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "start"
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.name = ""

# ------------------ START PAGE ------------------
if st.session_state.page == "start":
    st.markdown(
        """
        <h1 style='text-align:center;'>🧪 Class 8 Science Quiz</h1>
        <h3 style='text-align:center;'>Curiosity 2025</h3>
        """,
        unsafe_allow_html=True
    )

    st.write("👋 Welcome young scientist!")
    st.write("📚 NCERT Based • 🎮 Game Style • 🧠 Learn with Fun")

    name = st.text_input("Enter your name to start")

    if st.button("🚀 Start Quiz"):
        if name.strip() == "":
            st.warning("Please enter your name")
        else:
            st.session_state.name = name
            st.session_state.page = "quiz"
            st.rerun()

# ------------------ QUIZ PAGE ------------------
elif st.session_state.page == "quiz":
    q = questions[st.session_state.q_index]

    st.progress((st.session_state.q_index) / len(questions))

    st.markdown(
        """
        <div style="padding:20px;border-radius:15px;background:#1f2933;">
        <h3 style="color:#60a5fa;">🧠 Question Time</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader(q["q"])
    choice = st.radio("Choose your answer:", q["options"])

    if st.button("✅ Submit Answer"):
        if choice == q["ans"]:
            st.session_state.score += 1
            st.success("Correct! Great job 👏")
            st.balloons()
        else:
            st.error(f"Wrong! Correct answer: {q['ans']}")

        st.session_state.q_index += 1

        if st.session_state.q_index >= len(questions):
            st.session_state.page = "result"

        st.rerun()

# ------------------ RESULT PAGE ------------------
elif st.session_state.page == "result":
    score = st.session_state.score
    total = len(questions)

    save_score(st.session_state.name, score)

    st.markdown("## 🎉 Quiz Completed!")

    st.metric("Your Score", f"{score} / {total}")

    if score == total:
        st.success("🏆 PERFECT SCORE! You are a Science Champion!")
        st.balloons()
    elif score >= total * 0.6:
        st.success("👏 Great job! Keep learning!")
    else:
        st.warning("🙂 Good effort! Try again to improve.")

    st.subheader("🏆 Science Champions Hall of Fame")

    if os.path.exists(LEADERBOARD_FILE):
        df = pd.read_csv(LEADERBOARD_FILE)
        df = df.sort_values(by="Score", ascending=False)
        st.dataframe(df.head(10), use_container_width=True)

    if st.button("🔁 Play Again"):
        st.session_state.page = "start"
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.rerun()
