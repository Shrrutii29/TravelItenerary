import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Load Cohere API key from environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize Cohere client
co = cohere.Client(api_key)

# App Title
st.title("AI-Powered Travel Planner")
st.write("Plan your dream trip with a personalized, AI-generated itinerary!")

# Collect User Input
st.header("Tell us about your trip")

# Input fields
destination = st.text_input("Destination (City or Country)")
trip_duration = st.slider("Trip Duration (in days)", 1, 30, 5)
budget = st.selectbox("Budget", ["Low", "Moderate", "High"])
trip_type = st.selectbox(
    "Type of Trip",
    ["Relaxation", "Adventure", "Cultural Exploration", "Food Tourism", "Mixed"]
)
dietary_preferences = st.text_input("Dietary Preferences (optional)")
mobility = st.selectbox("Mobility Concerns (optional)", ["None", "Low Tolerance", "Moderate", "High Tolerance"])
accommodation = st.selectbox(
    "Accommodation Preference", ["Luxury", "Budget", "Central Location", "No Preference"]
)
seasonal_preferences = st.selectbox("Seasonal Preferences", ["Summer", "Winter", "Any"])
avoid_areas = st.text_input("Areas to avoid (optional)")

# Edge cases
warnings = []

# Validate mandatory fields
if not destination:
    warnings.append("Please specify a destination for your trip.")
if trip_duration < 1:
    warnings.append("Trip duration should be at least 1 day.")
if not budget:
    warnings.append("Please specify your budget.")
if not trip_type:
    warnings.append("Please select a trip type.")
if accommodation == "Luxury" and budget == "Low":
    warnings.append("Your selected accommodation preference (Luxury) might not align with a low budget. Please reconsider.")
if not dietary_preferences and mobility == "High Tolerance":
    warnings.append("Consider specifying dietary preferences if you have special requirements.")

# Display warnings
if warnings:
    for warning in warnings:
        st.warning(warning)

# Button to confirm inputs and generate itinerary
if st.button("Generate Itinerary"):

    if warnings:
        st.warning("Please address the issues above before generating the itinerary.")
    else:
        # System Prompt
        system_prompt = f"""
        You are a highly efficient AI assistant tasked with creating personalized itineraries for travelers. Your goal is to ensure that each itinerary is:
        - Well-organized, with clear morning, afternoon, and evening activities.
        - Tailored to the user's preferences (e.g., trip type, budget, dietary restrictions, etc.).
        - Engaging, including unique local experiences and hidden gems.
        - Respectful of the user's mobility concerns and seasonal preferences.
        - Concise, easy to follow, and aligned with the user's duration and budget.
        Always consider any user input provided (e.g., destination, trip duration, etc.), and refine the trip plan accordingly.
        """

        # Refinement Prompt
        refinement_prompt = f"""
        Destination: {destination}
        Duration: {trip_duration} days
        Budget: {budget}
        Trip Type: {trip_type}
        Dietary Preferences: {dietary_preferences if dietary_preferences else 'None'}
        Mobility Concerns: {mobility}
        Accommodation: {accommodation}
        Seasonal Preferences: {seasonal_preferences}
        Areas to Avoid: {avoid_areas if avoid_areas else 'None'}

        Please refine these inputs to ensure they are clear, actionable, and consistent. Clarify any contradictions or vague details (e.g., 'low budget' with 'luxury accommodation'). Based on this, suggest improvements or considerations to enhance the trip plan.
        """

        try:
            with st.spinner("Refining your inputs..."):
                refinement_response = co.generate(
                    model="command-xlarge-nightly",
                    prompt=system_prompt + "\n" + refinement_prompt,
                    temperature=0.7,
                    max_tokens=4000
                )
                refined_inputs = refinement_response.generations[0].text.strip()

            # Itinerary Generation
            chunk_size = 5
            num_chunks = (trip_duration // chunk_size) + (1 if trip_duration % chunk_size != 0 else 0)
            itinerary = []

            with st.spinner("Generating your itinerary..."):
                for chunk in range(num_chunks):
                    start_day = chunk * chunk_size + 1
                    end_day = min((chunk + 1) * chunk_size, trip_duration)

                    # Chunk-specific prompt
                    itinerary_prompt = f"""
                    Create a personalized itinerary for {destination} from day {start_day} to day {end_day}. Include in concise manner:
                    - Morning activities, including recommendations for transportation.
                    - Afternoon activities with lunch recommendations.
                    - Evening activities with dinner recommendations.
                    - Highlight unique local experiences, fun activities, hidden gems, and top-rated landmarks.
                    - Ensure the itinerary aligns with a {budget} budget and the {trip_type} theme.
                    - Consider dietary preferences ({dietary_preferences}) and mobility concerns ({mobility}).
                    - Align with seasonal preferences ({seasonal_preferences}).
                    - Avoid {avoid_areas} if specified.
                    """

                    # Generate response
                    response = co.generate(
                        model='command-xlarge-nightly',
                        prompt=itinerary_prompt,
                        temperature=0.7,
                        max_tokens=4000
                    )

                    # Append chunk to the full itinerary
                    itinerary.append(f"### Days {start_day}-{end_day}:\n" + response.generations[0].text.strip())

            # Display final itinerary
            st.header("Your Personalized Itinerary")
            for chunk_text in itinerary:
                st.write(chunk_text)

        except Exception as e:
            # Display errors
            st.error(f"An error occurred while generating the itinerary: {e}")
