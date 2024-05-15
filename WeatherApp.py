import tkinter as tk
from tkinter import font as tkfont
import requests
import threading
from PIL import Image, ImageTk
import os

app = tk.Tk()
app.title("Dynamic Weather Forecaster")

# Constants for the application
HEIGHT = 500
WIDTH = 600
FONT_NAME = 'Helvetica'
FONT_SIZE = 12
FONT_STYLE = tkfont.Font(family=FONT_NAME, size=FONT_SIZE, weight='bold')

# Create and pack the main canvas
C = tk.Canvas(app, height=HEIGHT, width=WIDTH)
C.pack()

# Set the initial background image
initial_bg = ImageTk.PhotoImage(file='img/default.jpeg')
background_label = tk.Label(app, image=initial_bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Function to format the weather response
def format_response(weather_json):
    try:
        city = weather_json['name']
        conditions = weather_json['weather'][0]['description']
        temp = weather_json['main']['temp']
        final_str = f'City: {city} \nConditions: {conditions} \nTemperature (°C): {temp}'
    except KeyError:
        final_str = 'There was a problem retrieving that information'
    return final_str

# Function to get weather data from the OpenWeatherMap API
def get_weather(city):
    weather_key = '7a108ed20684ed2ae4c04d00d115f80a'  # Your API key
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': city, 'units': 'metric'}
    try:
        response = requests.get(url, params=params)
        weather_json = response.json()
        print(weather_json)

        if 'weather' in weather_json:
            results['text'] = format_response(weather_json)
            icon_name = weather_json['weather'][0]['icon']
            update_background(weather_json['weather'][0]['main'].lower())
            open_image(icon_name)
        else:
            if 'message' in weather_json:
                error_message = weather_json['message']
            else:
                error_message = 'Weather data not found. Check city name or API key.'
            results['text'] = error_message
    except requests.exceptions.RequestException as e:
        results['text'] = f"API request failed: {e}"

# Function to open and display the weather icon
def open_image(icon):
    base_dir = '/Users/yuvraj/Documents/WeatherApp/img'
    default_icon = 'default.png'
    icon_path = os.path.join(base_dir, f'{icon}.png')
    if not os.path.exists(icon_path):
        icon_path = os.path.join(base_dir, default_icon)
        print(f"Warning: {icon}.png not found. Using default icon.")
    size = int(lower_frame.winfo_height() * 0.25)
    try:
        img = Image.open(icon_path)
        img_resized = img.resize((size, size), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)
        weather_icon.delete("all")
        weather_icon.create_image(0, 0, anchor='nw', image=img_tk)
        weather_icon.image = img_tk
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to update the background image based on weather conditions
def update_background(condition):
    background_paths = {
        'clear': 'sunny.jpeg',
        'clouds': 'cloudy.jpeg',
        'rain': 'rainy.jpeg',
        'snow': 'snowy.jpeg',
        'mist': 'misty.jpeg',
        'haze': 'hazy.jpeg',
        'default': 'default.jpeg'
    }
    img_path = background_paths.get(condition, 'default.jpeg')
    background_image = ImageTk.PhotoImage(file=f'./img/{img_path}')
    background_label.config(image=background_image)
    background_label.image = background_image

# Function to automatically update the weather every 30 minutes
def auto_update_weather():
    city = textbox.get()
    if city:
        get_weather(city)
    threading.Timer(1800, auto_update_weather).start()

# Frame for the input box and submit button
frame = tk.Frame(app, bg='#42c2f4', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
textbox = tk.Entry(frame, font=FONT_STYLE)
textbox.place(relwidth=0.65, relheight=1)
submit = tk.Button(frame, text='Get Weather', font=FONT_STYLE, command=lambda: [get_weather(textbox.get()), auto_update_weather()])
submit.place(relx=0.7, relheight=1, relwidth=0.3)

# Frame for displaying the weather results and icon
lower_frame = tk.Frame(app, bg='#42c2f4', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
results = tk.Label(lower_frame, anchor='nw', justify='left', bd=4, bg='white', font=FONT_STYLE)
results.place(relwidth=1, relheight=1)
weather_icon = tk.Canvas(results, bg='white', bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)

# Run the main loop of the application
app.mainloop()
