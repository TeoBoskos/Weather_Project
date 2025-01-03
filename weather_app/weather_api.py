from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")
if not api_key:
  raise ValueError("API key not found. Please set it int the .env file.")

def get_weather(city) -> dict | None:
  """
  The purpose of this function is to fetch live weather data from the API.
  It gets the `base_url` and the API key. Then it handles API errors. If
  there aren't any it proceeds to fetching the current weather data and
  then it assigns them to variables. Then it checks if there are any errors.

  Parameters:
  -`city`: The name of the city for which weather data is retrieved.

  Returns: None
  """


  base_url = "http://api.weatherapi.com/v1/current.json"
  params = {"key": api_key, "q": city}

  try:
    response = requests.get(base_url, params=params)
    # Check if there is any problem with the API key.
    if response.status_code == 401:
      print("Invalid API key. Please check your .env file.")
      return None
    # Check if the user exceeds the rate of API requests per minute or per day.
    elif response.status_code == 429:
      print("Rate limit exceeded. Please wait before making more requests.")
      return None
    # Check if the city name is incorrect or if it's not supported by the API.
    elif response.status_code == 400:
      print("Invalid location. Please check the city name and try again.")
      return None

    response.raise_for_status()
    data = response.json()

    try:
      temp = data["current"]["temp_c"]
      condition = data["current"]["condition"]["text"]
      city_name = data["location"]["name"]
      return {"temperature": temp, "condition": condition, "city": city_name}
    # Unexpected API changes.
    except KeyError as e:
      print(f"Unexpected API response structure: Missing key {e}")
      return None
  
  # Internet connection error.
  except ConnectionError:
    print("Network error. Please check your Internet connection.")
    return None
  # API server being down.
  except requests.Timeout:
    print("The request timed out. Please try again later.")
    return None
  except requests.RequestException as e:
    print(f"An error occured: {e}")
    return None