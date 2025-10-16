import streamlit as st
from database import get_user_demographics
from diet_generator import generate_kidney_friendly_diet, get_kidney_health_tips, calculate_bmi, get_bmi_category

def show_page():
    """Display the diet chart page"""
    st.title("🍽️ Personalized Diet Chart")
    st.subheader("Kidney-friendly nutrition recommendations tailored for you")
    
    # Get user demographics
    demographics = get_user_demographics(st.session_state.username)
    
    if not demographics:
        st.warning("⚠️ Please complete your demographics first to get personalized diet recommendations!")
        if st.button("📝 Go to Demographics", use_container_width=True):
            st.session_state.current_page = "Demographics"
            st.rerun()
        return
    
    # Generate personalized diet
    diet_plan = generate_kidney_friendly_diet(demographics)
    
    # Display user health overview
    st.markdown("### 👤 Your Health Profile")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        age = demographics.get('age')
        st.metric("Age", f"{age} years" if age else "Not set")
    
    with col2:
        gender = demographics.get('gender')
        st.metric("Gender", gender if gender else "Not set")
    
    with col3:
        water_intake = demographics.get('daily_water_intake')
        st.metric("Daily Water", f"{water_intake} glasses" if water_intake else "Not set")
        if water_intake and water_intake < 8:
            st.caption("⚠️ Below recommended")
    
    with col4:
        weight = demographics.get('weight')
        height = demographics.get('height')
        if weight and height:
            bmi = calculate_bmi(weight, height)
            if bmi:
                st.metric("BMI", f"{bmi}", help=f"Category: {get_bmi_category(bmi)}")
        else:
            st.metric("BMI", "Not calculated")
    
    # Display diet plan
    st.markdown("---")
    st.markdown("### 🥗 Your Personalized Meal Plan")
    
    # Create tabs for different meals
    breakfast_tab, lunch_tab, dinner_tab, snacks_tab = st.tabs(["🌅 Breakfast", "☀️ Lunch", "🌙 Dinner", "🍎 Snacks"])
    
    with breakfast_tab:
        st.markdown("#### Recommended Breakfast Options")
        for item in diet_plan["breakfast"]:
            st.write(f"• {item}")
        
        st.markdown("**💡 Breakfast Tips:**")
        st.info("Start your day with low-sodium options. Avoid processed breakfast meats and opt for fresh fruits.")
    
    with lunch_tab:
        st.markdown("#### Recommended Lunch Options")
        for item in diet_plan["lunch"]:
            st.write(f"• {item}")
        
        st.markdown("**💡 Lunch Tips:**")
        st.info("Focus on lean proteins and fresh vegetables. Control portion sizes and avoid high-sodium seasonings.")
    
    with dinner_tab:
        st.markdown("#### Recommended Dinner Options")
        for item in diet_plan["dinner"]:
            st.write(f"• {item}")
        
        st.markdown("**💡 Dinner Tips:**")
        st.info("Keep dinner light and avoid eating late. Choose easily digestible proteins and vegetables.")
    
    with snacks_tab:
        st.markdown("#### Healthy Snack Options")
        for item in diet_plan["snacks"]:
            st.write(f"• {item}")
        
        st.markdown("**💡 Snack Tips:**")
        st.info("Choose fresh fruits and vegetables over processed snacks. Stay hydrated with water or herbal teas.")
    
    # General guidelines
    st.markdown("---")
    st.markdown("### 📋 General Dietary Guidelines")
    
    guideline_col1, guideline_col2 = st.columns(2)
    
    with guideline_col1:
        st.markdown("#### ✅ Kidney-Friendly Foods")
        kidney_friendly = [
            "🐟 Fresh fish (salmon, mackerel)",
            "🍎 Fresh fruits (apples, berries)",
            "🥒 Fresh vegetables (cucumber, cabbage)",
            "🍚 White rice and quinoa",
            "🥛 Low-fat dairy products",
            "💧 Plenty of water",
            "🌿 Fresh herbs and spices"
        ]
        
        for food in kidney_friendly:
            st.write(food)
    
    with guideline_col2:
        st.markdown("#### ❌ Foods to Limit/Avoid")
        limit_foods = [
            "🧂 High-sodium processed foods",
            "🥩 Red meat (limit portions)",
            "🥜 Nuts and seeds (high phosphorus)",
            "🍌 High-potassium fruits (bananas)",
            "🥤 Sodas and sugary drinks",
            "🍟 Fast food and fried foods",
            "🧀 High-sodium cheeses"
        ]
        
        for food in limit_foods:
            st.write(food)
    
    # Personalized notes
    st.markdown("---")
    st.markdown("### 👩‍⚕️ Personalized Health Notes")
    
    # Display personalized notes from diet generator
    notes = []
    if "general_notes" in diet_plan:
        notes.append(("General", diet_plan["general_notes"]))
    if "portion_control" in diet_plan:
        notes.append(("Portion Control", diet_plan["portion_control"]))
    if "diabetes_note" in diet_plan:
        notes.append(("Diabetes Management", diet_plan["diabetes_note"]))
    if "hypertension_note" in diet_plan:
        notes.append(("Blood Pressure", diet_plan["hypertension_note"]))
    if "kidney_stones_note" in diet_plan:
        notes.append(("Kidney Stones", diet_plan["kidney_stones_note"]))
    if "hydration_note" in diet_plan:
        notes.append(("Hydration", diet_plan["hydration_note"]))
    
    if notes:
        for note_type, note_content in notes:
            st.warning(f"**{note_type}:** {note_content}")
    
    # Guidelines from diet plan
    if "guidelines" in diet_plan:
        st.markdown("### 📝 Key Dietary Guidelines")
        for guideline in diet_plan["guidelines"]:
            st.write(f"• {guideline}")
    
    # Weekly meal planning
    st.markdown("---")
    st.markdown("### 📅 Weekly Meal Planning Tips")
    
    planning_tips = [
        "🗓️ **Meal Prep:** Prepare kidney-friendly meals in advance for the week",
        "🛒 **Shopping:** Make a grocery list focusing on fresh, unprocessed foods",
        "💧 **Hydration:** Set reminders to drink water throughout the day",
        "📱 **Tracking:** Keep a food diary to monitor your nutrition",
        "👨‍⚕️ **Consultation:** Review your diet plan with your healthcare provider",
        "⚖️ **Portions:** Use measuring cups to control portion sizes",
        "🥗 **Variety:** Rotate different vegetables and proteins to avoid monotony"
    ]
    
    for tip in planning_tips:
        st.info(tip)
    
    # Download diet plan
    st.markdown("---")
    st.markdown("### 📥 Download Your Diet Plan")
    
    # Generate downloadable content
    diet_text = f"""
LIFELens-AI Personalized Diet Plan
Generated for: {st.session_state.username}
Date: {st.datetime.datetime.now().strftime("%Y-%m-%d")}

BREAKFAST OPTIONS:
{chr(10).join(['• ' + item for item in diet_plan["breakfast"]])}

LUNCH OPTIONS:
{chr(10).join(['• ' + item for item in diet_plan["lunch"]])}

DINNER OPTIONS:
{chr(10).join(['• ' + item for item in diet_plan["dinner"]])}

SNACK OPTIONS:
{chr(10).join(['• ' + item for item in diet_plan["snacks"]])}

GUIDELINES:
{chr(10).join(['• ' + guideline for guideline in diet_plan.get("guidelines", [])])}

Note: This plan is generated based on your demographics and should be reviewed with your healthcare provider.
"""
    
    st.download_button(
        label="📄 Download Diet Plan (TXT)",
        data=diet_text,
        file_name=f"lifelens_diet_plan_{st.session_state.username.split('@')[0]}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    # Disclaimer
    st.markdown("---")
    st.error("""
    ⚠️ **Important Disclaimer**
    
    This diet plan is generated based on general kidney health principles and your provided demographics. 
    It is not a substitute for professional medical advice. Always consult with your healthcare provider 
    or a registered dietitian before making significant changes to your diet, especially if you have 
    kidney disease or other medical conditions.
    """)
