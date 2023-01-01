import config
import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 75
HEIGHT_CM = 168
AGE = 37

user_exercise = input("Which exercises did you do today? ")

# API request to the website Nutritionix, takes natural language as input, calculated exercise estimate stats, and
# add them as a new row to the Google sheet
nutriix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = "https://api.sheety.co/e1aee1dc8dd8788a0cdf172a250534f9/workoutTracking/workouts"

header = {
    "x-app-id": config.NUTRIIX_ID,
    "x-app-key": config.NUTRIIX_KEY,
}
nutriix_params = {
    "query": user_exercise,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=nutriix_endpoint, headers=header, json=nutriix_params)
exercise_data = response.json()
exercise_name = exercise_data["exercises"][0]["name"]

# Getting current date and time and formatting in the sheet format
now = datetime.now()
date = now.strftime("%d/%m/%Y")
hour = now.strftime("%X")

sheety_params = {
    "workout": {
        "date": date,
        "time": hour,
        "exercise": exercise_name.title(),
        "duration": exercise_data["exercises"][0]["duration_min"],
        "calories": exercise_data["exercises"][0]["nf_calories"],
    },
}
sheety_headers = {
    "Authorization": config.SHEETY_AUTH,
}

sheety_response = requests.post(url=sheety_endpoint, json=sheety_params, headers=sheety_headers)
