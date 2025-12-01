import streamlit as st
import pandas as pd

st.set_page_config(page_title="Exercise Recommendation", page_icon="🏋️‍♂️")

# ---------------- Header ---------------- #
html_temp = """
<div style="background-color:#748c08;padding:1.5px">
<h1 style="color:white;text-align:center;">Exercise Guidance for Diabetes 🚴</h1>
</div><br>"""
st.markdown(html_temp, unsafe_allow_html=True)

# ---------------- Section: Personalized Exercise Plan ---------------- #
st.subheader("📌 Personalized Exercise Recommendation")

age = st.number_input("Enter your Age", min_value=5, max_value=100, step=1)
weight = st.number_input("Enter your Weight (kg)", min_value=10.0, max_value=250.0, step=0.1)
height = st.number_input("Enter your Height (cm)", min_value=50.0, max_value=250.0, step=0.1)

diabetes_status = st.selectbox("Do you have diabetes?", 
                               ["Not Sure", "Yes (Diabetic)", "No (Non-Diabetic)"])

activity = st.selectbox(
    "Current activity level",
    ["Sedentary (No exercise)", "Light (1-2 days/week)", "Moderate (3-4 days/week)", "Heavy (5+ days/week)"]
)

health_issue = st.text_input("Any health issue? (optional, e.g., Back pain, BP, Knee pain)")

if height > 0:
    bmi = weight / ((height / 100) ** 2)
else:
    bmi = None

if st.button("Generate Exercise & Calorie Plan"):
    if bmi is None or bmi <= 0:
        st.error("Enter valid weight & height!")
    else:
        st.success(f"Your BMI: **{bmi:.2f}**")

        # ------------- Exercise Logic ---------------- #
        if bmi < 18.5:
            plan = "Underweight → Focus on muscle gain & strength."
            exercises = [
                "🏋️ Strength training (4 days/week)",
                "🚶 20–30 min walking daily",
                "🧘 Posture correction yoga",
            ]
            calories = 2300 + (age * 2)

        elif 18.5 <= bmi < 24.9:
            plan = "Normal BMI → Maintain fitness with balanced routine."
            exercises = [
                "🏃 Jogging 30 minutes",
                "🚴 Cycling twice weekly",
                "💪 Weight training (3 days/week)",
                "🧘 Yoga on weekends"
            ]
            calories = 2000 + (age * 1.5)

        elif 25 <= bmi < 29.9:
            plan = "Overweight → Fat loss + stamina building."
            exercises = [
                "🚶 Brisk walking 45 minutes daily",
                "🏊 Swimming / cycling (3 days/week)",
                "🔥 Light HIIT workouts",
                "🧘 Flexibility yoga"
            ]
            calories = 1800 + (age * 1.2)

        else:
            plan = "Obesity → Low-impact workouts & high consistency."
            exercises = [
                "🚶 Walking 45–60 minutes (once or twice daily)",
                "🚴 Static cycling",
                "🔥 Beginner HIIT",
                "🧘 Breathing & posture yoga"
            ]
            calories = 1600 + (age * 1)

        if diabetes_status == "Yes (Diabetic)":
            exercises.append("🩸 15-minute walk after meals to control sugar spikes")
        if health_issue.strip():
            exercises.append(f"⚠ Avoid stress due to: **{health_issue}**")

        st.subheader("🎯 Personalized Workout Plan")
        st.write(plan)
        for item in exercises:
            st.write("✔", item)

        # ---------------- Calorie Intake ---------------- #
        st.subheader("🔥 Recommended Daily Calorie Intake")
        st.write(f"➡ You should consume approximately **{int(calories)} calories per day**.")

        st.info("Protein-rich balanced meals are ideal for diabetes & fitness management.")

        # Save user report (optional)
        try:
            df = pd.DataFrame([{
                "Age": age, "Weight": weight, "Height": height, "BMI": round(bmi, 2),
                "Diabetes": diabetes_status, "Activity": activity,
                "Calorie_Target": int(calories), "HealthIssue": health_issue
            }])
            df.to_csv("data/exercise_logs.csv", mode="a", header=False, index=False)
        except Exception:
            pass

# ---------------- Section: 10 Exercises Info ---------------- #
st.markdown("---")
st.header("💪 Top 10 Effective Exercises for Diabetes")

sections = [
    ("1. Walking", "Walking 30 min/day 5 days/week improves HbA1c, BP, and BMI."),
    ("2. Cycling", "Low-impact exercise ideal for diabetes & joint pain."),
    ("3. Swimming", "Aqua exercise lowers sugar levels and protects joints."),
    ("4. Team sports", "Motivation & enjoyment increase exercise consistency."),
    ("5. Aerobic dance", "Fast-paced workout (e.g., Zumba) boosts stamina & helps weight loss."),
    ("6. Weightlifting", "Builds muscle mass → increases calories burned."),
    ("7. Resistance band", "Improves strength & helps stabilize blood sugar."),
    ("8. Calisthenics", "Uses body weight — squats, pushups, pulls, etc."),
    ("9. Pilates", "Improves core balance & better sugar control in older adults."),
    ("10. Yoga", "Reduces blood sugar & cholesterol; enhances sleep & mood.")
]

for title, desc in sections:
    st.subheader(title)
    st.markdown(desc)
