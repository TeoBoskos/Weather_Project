import tkinter as tk
import tkinter.font as font

from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
from weather_api import get_weather
from button_fun import entry_btn_fun

root = tk.Tk()
root.title("Weather App")
root.geometry("1400x600")

# Preload the images at startup.
images = {
  "Sunny": ImageTk.PhotoImage(Image.open("sun.png").resize((264, 264))),
  "Rainy": ImageTk.PhotoImage(Image.open("rain.png").resize((264, 264))),
  "Cloudy": ImageTk.PhotoImage(Image.open("cloud.png").resize((264, 264))),
  "Partly cloudy": ImageTk.PhotoImage(Image.open("partly_cloudy.png").resize((264, 264)))
}

# Current date.
current_date = datetime.now().strftime("%d/%m/%Y")

# City.
city = ""

# Get live weather data from the API.
weather_data = get_weather(city)

if weather_data:
  # Use live weather data if available.
  degrees_cel = weather_data["temperature"]
  weather_status = weather_data["condition"]
  city_name = weather_data["city"]
else:
  # Use default values if there's an error.
  degrees_cel = "N/A"
  weather_status = "Error"
  city_name = "Unknown"

# Creating the frames.
frame_number = ttk.Frame(root, padding=(100, 50))
frame_info = ttk.Frame(root, padding=(15, 20))
frame_image = ttk.Frame(root, padding=(15, 20))

frame_number.grid(row=0, column=0)
frame_info.grid(row=0, column=1)
frame_image.grid(row=0, column=2)

# Widgets for the first frame.
number_label = ttk.Label(frame_number, text=f"{degrees_cel} °C", font=("Segoe UI", 60, "bold"))
number_label.grid()

# Widgets for the second frame.
city_str = tk.StringVar()

city_label = ttk.Label(frame_info, text=f"{city_name}", font=("Segoe UI", 30), padding=(0, 0, 0, 10))

entry_label = ttk.Label(frame_info, text="Please input a city name: ", font=("Segoe UI", 14))
city_entry = ttk.Entry(frame_info, textvariable=city_str, font=("Segoe UI", 14), width=15)
entry_button = ttk.Button(frame_info, text="Go", command=lambda: entry_btn_fun(city_str, city_label, status_label, number_label, image_label, loading_label))

status_label = ttk.Label(frame_info, text=f"{weather_status}", font=("Segoe UI", 20), padding=(0, 10))
loading_label = ttk.Label(frame_info, text="Loading...", style="Loading.TLabel")
date_label = ttk.Label(frame_info, text=current_date, font=("Segoe UI", 14), padding=(0, 10, 0, 50))

city_label.grid(row=0, column=0, sticky="W")

entry_label.grid(row=1, column=0, sticky="W")
city_entry.grid(row= 1, column=1, sticky="W")
entry_button.grid(row=1, column=2, sticky="NSW")

status_label.grid(row=2, column=0, sticky="W")
loading_label.grid_remove() # Keep it hidden.
date_label.grid(row=4, column=0, sticky="W")

# Bind the enter key to the city_entry.
city_entry.bind("<Return>", lambda event: entry_btn_fun(city_str, city_label, status_label, number_label, image_label, loading_label))
city_entry.focus()

# Widgets for the third frame.
if weather_status in images:
  status_photo = images[weather_status]
else:
  status_photo = images["Sunny"]

image_label = ttk.Label(frame_image, image=status_photo, padding=5)
image_label.grid()

# Styles.
style = ttk.Style()

# Custom style for the loading label.
style.configure("Loading.TLabel", foreground="gray", font=("Segoe UI", 8))

# Configure rows.
root.rowconfigure(0, weight=1)

# Configure columns.
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Wrap the frames if the window gets too small.
layout_wrapped = None

def wrapped(event) -> None:
  """
  The purpose of this function is to wrap the three frames,
  `frame_number`, `frame_info`, and `frame_image`, on top of
  each other when the width of the window becomes less than
  1200. It also checks when the width becomes more than or
  equal to 1200. In that case, the frames are unwrapped.

  Parameters: 
    -`event`: An object containing details about the event
      that triggered the function.

  Returns: None
  """


  global layout_wrapped

  # Get the current window width.
  width = root.winfo_width()

  if width < 1200 and layout_wrapped != "wrapped":
    frame_number.grid(row=0, column=0, sticky="EW")
    frame_info.grid(row=1, column=0, sticky="EW")
    frame_image.grid(row=2, column=0, sticky="EW")
    layout_wrapped = "wrapped"

  elif width >= 1200 and layout_wrapped != "unwrapped":
    frame_number.grid(row=0, column=0, sticky="EW")
    frame_info.grid(row=0, column=1, sticky="EW")
    frame_image.grid(row=0, column=2, sticky="EW")
    layout_wrapped = "unwrapped"

# Bind the event to the window resize.
root.bind("<Configure>", wrapped)

root.mainloop()