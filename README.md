# TravelItenerary

# AI-Powered Travel Planner

A personalized travel itinerary generator that helps you plan your dream trip. The app uses Cohere's API to create tailored itineraries based on your preferences, such as destination, trip duration, budget, and more.

## Features

- Personalized travel itineraries based on user inputs.
- Option to specify trip preferences like budget, mobility concerns, and seasonal preferences.
- AI-generated day-by-day itinerary with activities, meals, and local experiences.
- Built with Streamlit for a simple and intuitive user interface.
- Free-tier deployment on Streamlit Cloud for easy access.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Cohere API
- **Environment Variables**: `.env` file to store sensitive information like API keys.

## How It Works

1. **User Input**: 
   The app collects key information about your trip, including:
   - Destination
   - Trip duration
   - Budget
   - Trip type (e.g., relaxation, adventure)
   - Dietary preferences
   - Mobility concerns
   - Accommodation preferences
   - Seasonal preferences
   - Areas to avoid

2. **Refinement of Inputs**: 
   The app will refine your inputs to ensure that they are clear, actionable, and consistent. For example, it checks if the trip budget aligns with the type of accommodation selected.

3. **Itinerary Generation**: 
   Based on your preferences, the app uses Cohere's API to generate a personalized travel itinerary. The itinerary is divided into day-by-day activities:
   - Morning activities with transportation recommendations.
   - Afternoon activities with lunch suggestions.
   - Evening activities with dinner recommendations.
   - Special focus on unique local experiences and top-rated landmarks.
   - The itinerary adapts to your dietary preferences, mobility concerns, and seasonal preferences.

4. **Result Display**: 
   The app displays the final itinerary on your screen.

## Installation

### Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.7+
- Streamlit
- Pip (Python package manager)

### Steps to Set Up

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Shrrutii29/TravelItenerary.git
   ```
2  **Navigate into the Project Directory**:
   ```bash
   cd TravelItenerary
   ```
3  **Install depedency**:
   ```bash
      pip install -r requirements.txt
   ```
4 **Set Up Environment Variables: Create a .env file in the root directory to store your API key for Cohere. The file should look like this**:
  ```bash
    API_KEY=your_cohere_api_key_here
   ```
5 **Run the Application**:
   ```bash
      streamlit run travelplanner.py
   ```

## Deployment
- The app is deployed on Streamlit Cloud and can be accessed via the following link:
- [Travel Itinerary App](https://travelitenerary-rahegdrxcpl8krjgrvae5m.streamlit.app/)
- Note: Due to the free-tier version of the app, it may take some time to load on the first request.
