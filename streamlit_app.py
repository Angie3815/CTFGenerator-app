import streamlit as st
import random
import time
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="AI-Powered CTF Game")

# ----------------------
# Question Bank
# ----------------------
sample_questions = {
    "Cryptography": {
        "Beginner": [
            {"question": "What is the plaintext of 'Uifsf jt b tfdsfu nfttbhf' using Caesar cipher?", "flag": "There is a secret message", "hint": "Shift each letter back by 1"},
            {"question": "Decode this Base64: 'SGVsbG8gQ1RGLg=='", "flag": "Hello CTF.", "hint": "Use a Base64 decoder"},
            {"question": "ROT13 of 'Pnrfne pvcure' is?", "flag": "Caesar cipher", "hint": "ROT13 is Caesar with a shift of 13"},
            {"question": "Find the ASCII for hex 41 42 43", "flag": "ABC", "hint": "Convert hex to ASCII"},
            {"question": "XOR 1010 with 1100 (binary result)?", "flag": "0110", "hint": "XOR = 1 if bits differ"},
            {"question": "What is the Caesar decryption of 'Khoor' with shift 3?", "flag": "Hello", "hint": "Shift each letter back 3"},
            {"question": "Base64 decode 'U2VjdXJpdHkgSXMgS2V5'", "flag": "Security Is Key", "hint": "Online Base64 tool"},
            {"question": "Find the flag in the string: 'This_is_not_the_flag_but_this_is:Flag{EasyWin}'", "flag": "Flag{EasyWin}", "hint": "Look after ':'"},
            {"question": "Hex 43 54 46 equals what in ASCII?", "flag": "CTF", "hint": "Convert hex to text"},
            {"question": "ROT13 decode 'Clguba vf sha!'", "flag": "Python is fun!", "hint": "ROT13 decode it"}
        ],
        "Intermediate": [
            {"question": "Decrypt Caesar cipher: 'Gur dhvpx oebja sbk' with ROT13", "flag": "The quick brown fox", "hint": "ROT13 is symmetric"},
            {"question": "Find the Vigenere key: 'HELLO' -> 'RIJVS'", "flag": "KEY", "hint": "Check Vigenere cipher tools"},
            {"question": "RSA: e=3, n=55, ciphertext=27. Decrypt.", "flag": "3", "hint": "Cube root mod n"},
            {"question": "Base32 decode: 'IFBEGRCFIZDUQSKKJNGE===='", "flag": "CTFChallenge", "hint": "Use online decoder"},
            {"question": "Hex 4D 44 35 equals?", "flag": "MD5", "hint": "Hex to ASCII"},
            {"question": "XOR 0x41 (A) with 0x20 = ? (char)", "flag": "a", "hint": "XOR flips case"},
            {"question": "Binary to text: 01000011 01010100 01000110", "flag": "CTF", "hint": "Convert binary to ASCII"},
            {"question": "Encrypted: XOR each char in 'flag' with 0x01", "flag": "gleh", "hint": "Use ord and chr in Python"},
            {"question": "MD5 hash: 5f4dcc3b5aa765d61d8327deb882cf99", "flag": "password", "hint": "Classic default"},
            {"question": "Find Base64 of 'TryHarder'", "flag": "VHJ5SGFyZGVy", "hint": "Use base64 encoder"}
        ]
    },
    "Networking": {
        "Beginner": [
            {"question": "Which port is used by HTTP?", "flag": "80", "hint": "Default web port"},
            {"question": "What does DNS stand for?", "flag": "Domain Name System", "hint": "Resolves domain names"},
            {"question": "Loopback IP address?", "flag": "127.0.0.1", "hint": "Localhost"},
            {"question": "Default port for HTTPS?", "flag": "443", "hint": "Secure HTTP"},
            {"question": "Protocol for assigning IPs?", "flag": "DHCP", "hint": "Dynamic host config"},
            {"question": "Command to test connectivity?", "flag": "ping", "hint": "Send ICMP packets"},
            {"question": "OSI layer for TCP?", "flag": "Transport", "hint": "Layer 4"},
            {"question": "Device to connect networks?", "flag": "Router", "hint": "Gateway device"},
            {"question": "Full form of LAN?", "flag": "Local Area Network", "hint": "Opposite of WAN"},
            {"question": "Which protocol uses port 22?", "flag": "SSH", "hint": "Remote shell"}
        ],
        "Intermediate": [
            {"question": "Tool for SYN scan?", "flag": "nmap", "hint": "Port scanner"},
            {"question": "What does traceroute show?", "flag": "Path to host", "hint": "Hops"},
            {"question": "What is TTL?", "flag": "Time To Live", "hint": "Limits packet lifetime"},
            {"question": "Command to show open ports on Linux?", "flag": "netstat -tuln", "hint": "Terminal tool"},
            {"question": "Sniff packets with GUI?", "flag": "Wireshark", "hint": "Packet inspector"},
            {"question": "Which protocol sends email?", "flag": "SMTP", "hint": "Email sending"},
            {"question": "Subnet mask for /24?", "flag": "255.255.255.0", "hint": "Class C"},
            {"question": "Secure file transfer protocol?", "flag": "SFTP", "hint": "Over SSH"},
            {"question": "Find flag in packet: 'Flag{Sniffed}'", "flag": "Flag{Sniffed}", "hint": "Look inside packet"},
            {"question": "DNS works on which OSI layer?", "flag": "Application", "hint": "Top of the stack"}
        ]
    }
}

# ----------------------
# Game Initialization
# ----------------------
def initialize_game():
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""  # Initialize player_name if not present
    if "started" not in st.session_state:
        st.session_state.started = True
    if "category" not in st.session_state:
        st.session_state.category = ""  # Set empty initially
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = ""  # Set empty initially
    if "question_number" not in st.session_state:
        st.session_state.question_number = 1  # Start at question 1
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

# ----------------------
# Fetch Question
# ----------------------
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

# ----------------------
# Timer Logic
# ----------------------
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

# ----------------------
# Final Score Summary
# ----------------------
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

# ----------------------
# Main Game UI
# ----------------------
def run_game():
    # Display player name input if not set
    if "player_name" not in st.session_state or not st.session_state.player_name:
        st.title("🎯 AI-Powered CTF Game - Welcome!")
        name = st.text_input("Enter your name to begin:")
        if st.button("Start Game") and name.strip():
            st.session_state.player_name = name.strip()
            st.session_state.started = True
            st.session_state.category = ""  # Category and difficulty should be empty initially
            st.session_state.difficulty = ""
            st.rerun()  # Restart the game flow with player name
            st.stop()

    # Show category and difficulty selection only after the player's name is entered
    if st.session_state.started and not st.session_state.category and not st.session_state.difficulty:
        st.title(f"🎯 Let's go, {st.session_state.player_name}!")
        category = st.selectbox("Select a Category", list(sample_questions.keys()))
        difficulty = st.selectbox("Select Difficulty", ["Beginner", "Intermediate"])

        if st.button("Load Question"):
            st.session_state.category = category
            st.session_state.difficulty = difficulty
            st.session_state.current_question = get_next_question()
            st.session_state.question_number = 1  # Ensure the first question is marked as question 1
            st.rerun()

    # Show the question once category and difficulty are selected
    if st.session_state.category and st.session_state.difficulty:
        st.title(f"🎯 AI-Powered CTF Game - Welcome, {st.session_state.player_name}!")

        show_timer()
        st.write(f"### Question {st.session_state.question_number} of {st.session_state.max_questions}")
        st.markdown(f"**Score:** {st.session_state.score}")

        if st.session_state.current_question is None:
            st.session_state.current_question = get_next_question()

        question = st.session_state.current_question
        if not question:
            st.write("No more questions available.")
            return

        st.write(f"**Question:** {question['question']}")

        if st.button("💡 Show Hint"):
            st.info(f"Hint: {question['hint']}")

        with st.form("answer_form"):
            answer = st.text_input("Enter your answer:", key="answer_input")
            submitted = st.form_submit_button("Submit")

            if submitted and answer.strip() != "":
                if answer.strip().lower() == question['flag'].strip().lower():
                    st.markdown("<span style='color:green; font-weight:bold'>✅ Correct!</span>", unsafe_allow_html=True)
                    st.session_state.score += 100
                    st.session_state.answers.append((question['question'], answer, question['flag'], True))
                    st.session_state.start_time += timedelta(seconds=10)  # bonus time
                    st.session_state.question_number += 1
                    st.session_state.current_question = None
                else:
                    st.markdown("<span style='color:red; font-weight:bold'>❌ Incorrect!</span>", unsafe_allow_html=True)

        # Move these buttons outside the form
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔁 Try Again"):
                st.rerun()
        with col2:
            if st.button("Next question"):
                st.session_state.answers.append((question['question'], answer, question['flag'], False))
                st.session_state.question_number += 1
                st.session_state.current_question = None
                st.rerun()
        with col3:
            if st.button("Go Back"):
                st.session_state.category = ""
                st.session_state.difficulty = ""
                st.session_state.current_question = None
                st.rerun()

# ----------------------
# Start the game
# ----------------------
if "started" not in st.session_state:
    initialize_game()

run_game()
