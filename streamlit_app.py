import streamlit as st
import random
import time
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="AI-Powered CTF Game")

# Question Bank
sample_questions = {
    "Cryptography": {
        "Beginner": [
            {"question": "What is the plaintext of 'Uifsf jt b tfdsfu nfttbhf' using Caesar cipher?", "flag": "There is a secret message", "hint": "Shift each letter back by 1"},
            # ... (rest of the questions)
        ],
        "Intermediate": [
            {"question": "Decrypt Caesar cipher: 'Gur dhvpx oebja sbk' with ROT13", "flag": "The quick brown fox", "hint": "ROT13 is symmetric"},
            # ... (rest of the questions)
        ]
    },
    "Networking": {
        "Beginner": [
            {"question": "Which port is used by HTTP?", "flag": "80", "hint": "Default web port"},
            # ... (rest of the questions)
        ],
        "Intermediate": [
            {"question": "Tool for SYN scan?", "flag": "nmap", "hint": "Port scanner"},
            # ... (rest of the questions)
        ]
    }
}

# Game Initialization
def initialize_game():
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if "started" not in st.session_state:
        st.session_state.started = True
    if "category" not in st.session_state:
        st.session_state.category = ""
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = ""
    if "question_number" not in st.session_state:
        st.session_state.question_number = 1
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "max_questions" not in st.session_state:
        st.session_state.max_questions = 10
    if "used_questions" not in st.session_state:
        st.session_state.used_questions = []
    if "start_time" not in st.session_state:
        st.session_state.start_time = datetime.now()
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None

# Fetch Question
def get_next_question():
    category = st.session_state.category
    level = st.session_state.difficulty
    if category and level:
        pool = sample_questions[category][level]
        unused = [q for q in pool if q not in st.session_state.used_questions]
        if unused:
            q = random.choice(unused)
            st.session_state.used_questions.append(q)
            return q
    return None

# Timer Logic
def time_left():
    elapsed = datetime.now() - st.session_state.start_time
    total = timedelta(minutes=15)
    remaining = total - elapsed
    return max(remaining, timedelta(seconds=0))

def show_timer():
    remaining = time_left()
    mins, secs = divmod(remaining.seconds, 60)
    st.write(f"⏳ Time Left: {mins:02}:{secs:02}")
    if remaining <= timedelta(minutes=1):
        st.warning("⚠️ Less than 1 minute remaining!")

# Final Score Summary
def show_summary():
    st.subheader("🏁 Game Over")
    st.write(f"Final Score: {st.session_state.score}")
    st.subheader("Review Missed Questions:")
    for q, user_ans, correct_ans, is_correct in st.session_state.answers:
        if not is_correct:
            st.write(f"❓ **{q}**")
            st.write(f"🔴 Your answer: {user_ans}")
            st.write(f"✅ Correct answer: {correct_ans}")
    if st.button("🔁 Restart Game"):
        initialize_game()
        st.rerun()

# Main Game UI
def run_game():
    # Display player name input if not set
    if "player_name" not in st.session_state or not st.session_state.player_name:
        st.title("🎯 AI-Powered CTF Game - Welcome!")
        name = st.text_input("Enter your name to begin:")
        if st.button("Start Game") and name.strip():
            st.session_state.player_name = name.strip()
            st.session_state.started = True
            st.session_state.category = ""
            st.session_state.difficulty = ""
            st.rerun()

    # Show category and difficulty selection only after the player's name is entered
    if st.session_state.started and not st.session_state.category and not st.session_state.difficulty:
        st.title(f"🎯 Let's go, {st.session_state.player_name}!")
        category
