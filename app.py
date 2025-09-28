import streamlit as st
import random

st.set_page_config(page_title="AI Quiz Prototype", layout="centered")

# ------------------------------
# Sample Question Bank
# ------------------------------
QUESTION_BANK = {
    "Math": [
        {"q": "What is 2 + 2?", "options": ["3", "4", "5"], "a": "4"},
        {"q": "Solve: 5 × 6", "options": ["11", "30", "25"], "a": "30"},
        {"q": "Derivative of x²?", "options": ["x", "2x", "x²"], "a": "2x"}
    ],
    "General Knowledge": [
        {"q": "Capital of France?", "options": ["London", "Paris", "Berlin"], "a": "Paris"},
        {"q": "Who invented the light bulb?", "options": ["Einstein", "Edison", "Newton"], "a": "Edison"},
        {"q": "What is the national animal of India?", "options": ["Lion", "Tiger", "Elephant"], "a": "Tiger"}
    ],
    "Science": [
        {"q": "What planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus"], "a": "Mars"},
        {"q": "SI unit of force?", "options": ["Joule", "Newton", "Pascal"], "a": "Newton"},
        {"q": "What gas do plants absorb?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen"], "a": "Carbon Dioxide"}
    ]
}

# ------------------------------
# Helper: Generate Quiz
# ------------------------------
def generate_quiz(topic, num_qs=3):
    return random.sample(QUESTION_BANK.get(topic, QUESTION_BANK["General Knowledge"]), k=num_qs)

# ------------------------------
# Pages
# ------------------------------
def home():
    st.title("AI-Powered Quiz Platform 🎓 (Prototype)")
    st.subheader("Fast • Simple • No Heavy Models 🚀")
    st.markdown("""
    Welcome to the demo!  

    Choose a mode to continue:  
    - 📝 **Test Mode** → Quick practice  
    - 📘 **Learner Mode** → With hints  
    - ⏳ **Exam Mode** → Timed simulation  
    - 🚀 **Future Scope** → Coming soon features  
    """)

    if st.button("Test Mode"): st.session_state.mode, st.session_state.page = "test", "input"
    if st.button("Learner Mode"): st.session_state.mode, st.session_state.page = "learner", "input"
    if st.button("Exam Mode"): st.session_state.mode, st.session_state.page = "exam", "input"
    if st.button("Future Scope"): st.session_state.page = "future"

def input_page():
    st.header(f"Teacher Input ({st.session_state.mode.capitalize()} Mode)")
    topic = st.selectbox("Choose a Topic", list(QUESTION_BANK.keys()))
    num_qs = st.slider("Number of Questions", 1, 3, 2)
    st.session_state.topic = topic
    st.session_state.num_qs = num_qs

    if st.button("Generate Quiz"):
        st.session_state.quiz = generate_quiz(topic, num_qs)
        st.session_state.page = "quiz"

def quiz_page():
    st.header(f"Student Quiz – {st.session_state.mode.capitalize()} Mode")
    score = 0
    answers = []
    for i, q in enumerate(st.session_state.quiz):
        ans = st.radio(q["q"], q["options"], key=f"q{i}")
        answers.append((q["q"], ans, q["a"]))
        if st.session_state.mode == "learner":
            st.caption("💡 Hint: Think about basics you studied!")
    if st.button("Submit"):
        for _, ans, correct in answers:
            if ans == correct: score += 1
        st.session_state.score = score
        st.session_state.answers = answers
        st.session_state.page = "result"

def result_page():
    st.header("Results ✅")
    st.success(f"Your Score: {st.session_state.score}/{len(st.session_state.quiz)}")
    st.subheader("Answer Review")
    for q, ans, correct in st.session_state.answers:
        st.write(f"Q: {q}")
        st.write(f"- Your Answer: {ans}")
        st.write(f"- Correct Answer: {correct}")
        st.markdown("---")
    if st.session_state.mode == "exam":
        st.subheader("Leaderboard (Demo)")
        st.write("🥇 Student A – 3/3")
        st.write("🥈 You – {}/{}".format(st.session_state.score, len(st.session_state.quiz)))
        st.write("🥉 Student B – 1/3")
    if st.button("Back to Home"): st.session_state.page = "home"

def future_page():
    st.header("Future Scope 🚀")
    st.markdown("""
    ✅ PDF-to-Quiz (Upload notes, auto-generate quiz)  
    ✅ AI-powered grading for descriptive answers  
    ✅ Live leaderboard with class analytics  
    ✅ Mobile app & LMS integration  
    ✅ Cloud security + anti-cheating  
    """)
    if st.button("Back to Home"): st.session_state.page = "home"

# ------------------------------
# Page Router
# ------------------------------
if "page" not in st.session_state: st.session_state.page = "home"
if "mode" not in st.session_state: st.session_state.mode = None

if st.session_state.page == "home": home()
elif st.session_state.page == "input": input_page()
elif st.session_state.page == "quiz": quiz_page()
elif st.session_state.page == "result": result_page()
elif st.session_state.page == "future": future_page()
