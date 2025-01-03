import tkinter
from weather_api import get_weather
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk


# Function for the city entry button.
def entry_btn_fun(city_str, city_label, status_label, number_label, image_label, loading_label) -> None:
  """
  This function's purpose is to handle the click of the `entry_button` button.
  First it checks if the entry field is empty. If it is, it throws an error
  messagebox.
  Then it makes the `loading_label` visible. It takes the weather data from the
  `get_weather` function and checks if there are any. If not, it throws an
  error messagebox. If there are, it updates the UI with the current weather
  data at a specific city. Then it proceeds to load and update the appropriate
  image. Once all of this is complete, it hides the `loading_label`.

  Parameters:
    -`city_str`: The StringVar of the `city_entry`.
    -`city_label`: The label that contains the name of the current city.
    -`status_label`: The label that contains the current weather condition.
    -`number_label`: The label that contains the current temperature.
    -`image_label`: The label that contains the appropriate image for the
      current weather condition.
    -`loading_label`: The label that shows up only when the weather data is
      loading into the labels.
  """


  city = city_str.get()
  if not city.strip():
    messagebox.showerror("Error", "City name cannot be empty!")
    return
  
  # Make the loading label visible.
  loading_label.grid()
  
  # Fetch weather data.
  weather_data= get_weather(city)
  if weather_data:
    # Update the UI with new weather data.
    city_label.config(text=weather_data["city"])
    status_label.config(text=weather_data["condition"])
    number_label.config(text=f"{weather_data['temperature']} °C")

    weather_status = weather_data["condition"]

    # Load the appropriate image.
    if weather_status == "Sunny":
      status_photo = Image.open("sun.png").resize((264, 264))
    elif weather_status == "Cloudy":
      status_photo = Image.open("cloud.png").resize((264, 264))
    elif weather_status == "Rainy":
      status_photo = Image.open("rain.png").resize((264, 264))
    elif weather_status == "Partly cloudy":
      status_photo = Image.open("partly_cloudy.png").resize((264, 264))
    else:
      # Default photo in case of an error.
      status_photo = Image.open("sun.png").resize((264, 264))

    # Update the image.
    status_photo = ImageTk.PhotoImage(status_photo)
    image_label.config(image=status_photo)
    image_label.image = status_photo

  else:
    # Display error.
    messagebox.showerror("Error", "Failed to fetch weather data. Please check the city name and try again.")

  # Hide the loading label after the operation.
  loading_label.grid_remove()