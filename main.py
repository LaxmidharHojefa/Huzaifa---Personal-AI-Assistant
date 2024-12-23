import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import json
from gtts import gTTS
import os
from dotenv import load_dotenv
import time
import re
import yt_dlp
from datetime import datetime, timedelta

# This environment variable hides the Pygame welcome message when Pygame is imported
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# import pygame without showing the welcome message
import pygame

# Initialize text-to-speech engine
engine = pyttsx3.init()

# newsapi = ""

# This will load variables from the .env file
load_dotenv("C:/Main Project/Huzaifa/api.env")

newsapi = os.getenv("NEWS_API_KEY")

# Gemini api_key = AIzaSyBU4K2x6II408dOrqdPWdKwh7LQn3in4kQ
gemini_api = os.getenv("gemini_api")

# if gemini_api:
#     print(f"Gemini API: {gemini_api}")
# else:
#     print("Error: 'gemini_api' is not found. Check your api.env file and its path.")

def speak_old(text):
    # Get available voices
    voices = engine.getProperty('voices')

    # Set voice to female (for example, voices[1] may correspond to a female voice & voices[0] may correspond to a male voice)
    engine.setProperty('voice', voices[1].id)  # Change index to switch between male and female

    # Set the speech rate (optional)
    engine.setProperty('rate', 150)

    engine.say(text)
    engine.runAndWait()

# Function to convert text to speech and save as mp3
def speak(text):
    retries = 3
    delay = 2
    filename = "speech.wav"
    rate = 175

    # tts = gTTS(text=text, lang='en', slow=False)
    # tts.save(filename)
    # print(f"Speech saved to {filename}")

    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties for speech rate
    # Set the speed of the speech
    engine.setProperty('rate', rate)
    engine.setProperty('volume', 1)


    for i in range(retries):
        try:
            # Save to mp3
            engine.save_to_file(text, filename)
            # Wait until speech is saved
            # engine.say(text)
            engine.runAndWait()

            # tts = gTTS(text=text, lang='en', slow=False)
            # filename = "speech.mp3"
            # tts.save(filename)
            # print(f"Speech saved to {filename}")
            # os.system(f"start {filename}")
            
            # Speech saved successfully, break out of the loop
            # print(f"Speech saved to {filename}")

            break

        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < retries - 1:
                time.sleep(delay)
            else:
                print("All retries failed.")
                return
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    try:
        # Load the mp3 file
        pygame.mixer.music.load(filename)

        # Play the mp3 file
        pygame.mixer.music.play()

        # Wait until the audio is done playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Ensures the program doesn't exit before the speech is done

    except pygame.error as e:
        print(f"Error playing sound: {e}")

    finally:
        # Stop the music and uninitialize the mixer
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # Now, it's safe to delete the file
        if os.path.exists(filename):
            os.remove(filename)
            # print(f"{filename} deleted.")



def aiProcess(command):
    headers = {
    'Content-Type': 'application/json'
    }

    # Append the request for a short response to the command
    modified_command = command + " Please provide a short response."

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": modified_command
                    }
                ]
            }
        ]
    }

    # Make the POST request
    response = requests.post(gemini_api, headers=headers, data=json.dumps(data))

    # Check the status and print the result
    if response.status_code == 200:
        # data = response.json()
        # print(response.json())  # The JSON response
        response_data = response.json()
        # Extract and print the text from the response
        text = response_data['candidates'][0]['content']['parts'][0]['text']
        # print(text)
        # speak(text)
        return text
    else:
        print(f"Error: {response.status_code}")


# def processCommand(c):
#     if "open google" in c.lower():
#         print("Google is Opening")
#         speak("Google is Opening")
#         webbrowser.open("https://google.com")
#     elif "open facebook" in c.lower():
#         print("Facebook is Opening")
#         speak("Facebook is Opening")
#         webbrowser.open("https://facebook.com")
#     elif "open youtube" in c.lower():
#         print("YouTube is Opening")
#         speak("YouTube is Opening")
#         webbrowser.open("https://youtube.com")
#     elif "open linkedin" in c.lower():
#         print("Linkedin is Opening")
#         speak("Linkedin is Opening")
#         webbrowser.open("https://linkedin.com")
#     elif c.lower().startswith("play"):
        # song = c.lower().split(" ")[1]
        # link = musicLibrary.music[song]
        # print("YouTube is Opening")
        # speak("YouTube is Opening")
        # print(f"Starting to Playing Song {song}")
        # speak(f"Starting to Playing Song")
        # webbrowser.open(link)

def processCommand(c):
    c = c.lower()

    # Specific website commands
    if "open" in c:
        print(f"Your Command is :- {c}")
        website_match = re.search(r'open (\w+)', c)
        if website_match:
            website = website_match.group(1)
            print(f"Attempting to open {website.capitalize()}")
            speak(f"Attempting to open {website.capitalize()}")
            webbrowser.open(f"https://{website}.com")
        else:
            print("No website specified.")
            speak("No website specified. Please say a valid website name after 'open'.")

    # If the command starts with 'play', assume it's a song request
    # elif c.startswith("play"):
    elif c.lower().startswith("play"):
        # song = c.lower().split(" ")[1]
        # link = musicLibrary.music[song]
        # print("YouTube is Opening")
        # speak("YouTube is Opening")
        # print(f"Starting to Playing Song {song}")
        # speak(f"Starting to Playing Song")
        # webbrowser.open(link)
        try:
            print(f"Your Command is :- {c}")
            # song = c.split(" ", 1)[1]  # Extract the song name
            parts = c.split(" ")
            
            if len(parts) > 1:
                song = parts[1]

                print(f"Searching for {song} song on YouTube")
                speak(f"Searching for {song} songon YouTube")

                video_url = search_youtube(song) # type: ignore
                if video_url:
                    print(f"Playing '{song}' on YouTube :- {video_url}")
                    speak(f"Playing {song} on YouTube")
                    webbrowser.open(video_url)
                else:
                    print(f"Sorry, I couldn't find the song '{song}'")
                    speak(f"Sorry, I couldn't find the song {song}")
            
            else:
                print("No song specified after 'play'")
                speak("You forgot to mention the song name. Please say 'play' followed by the song name.")

        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("An unexpected error occurred. Please try again.")
    # else:
    #     print("Sorry, I didn't understand the command.")
    #     speak("Sorry, I didn't understand the command. Please try again with a valid command.")


    elif "news" in c.lower():
        print(f"Your Command is :- {c}")

        try:
            # Add headers to avoid status 426
            # headers = {
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            # }

            # Make a GET request to NewsAPI
            # r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2024-12-22&sortBy=publishedAt&apiKey={newsapi}", headers = headers)  
            # r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2024-12-22&sortBy=publishedAt&apiKey={newsapi}")


            # Calculate the allowed date range
            # For example, 30 days ago from today
            allowed_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

            # Construct the API URL with the dynamic date
            r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from={allowed_date}&sortBy=publishedAt&apiKey={newsapi}")

            if r.status_code == 200:
                print("Fetching News")
                speak("Fetching News")
            
                # Parse the JSON response
                data = r.json()  

                # Extract the articles
                articles = data.get('articles', [])

                if not articles:
                    print("No articles found.")
                    speak("Sorry, I couldn't find any news articles.")

                else:
                    # Red up tp 5 articles    
                    newsno = 1
                    for article in articles:
                        if newsno == 6:
                            break
                        title = article['title']
                        print(f"Title No.{newsno}: {title}")
                        speak(f"News Number {newsno} : {title}")
                        newsno += 1
            
            else:
                print(f"Failed to fetch news. Status code: {r.status_code}")
                speak("Sorry, I couldn't fetch the news at the moment. Please try again later.")
        
        except Exception as e:
            print(f"An error occurred while fetching news: {e}")
            speak("An error occurred while fetching news. Please check your internet connection or API settings.")    

    else:
        output = aiProcess(c)
        print(f"Your Command is :- {c}")
        print(output)
        speak(output)

def search_youtube(query):
    # Replace with your yt_dlp implementation
    # Example logic
    from yt_dlp import YoutubeDL
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'skip_download': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in result and result['entries']:
                return result['entries'][0]['webpage_url']
    except Exception as e:
        print(f"Error during YouTube search: {e}")
    return None

if __name__ == "__main__":
    speak("Initializing Huzaifa...")

    while True:
        r = sr.Recognizer()

        # Adjust this value based on your environment
        r.energy_threshold = 300 

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source)  # Adjust for background noise
                audio = r.listen(source, timeout=2)  # Listen with a timeout of 5 seconds

            word = r.recognize_google(audio)  # Recognize speech using Google
            # print(f"Command: {word}")

            if(word.lower() == "huzaifa"):
                print("Yes, I am Listening...")
                speak("Yes, I am Listening...")

                # Listen for command
                with sr.Microphone() as source:
                    print("Huzaifa Active...")
                    # speak("Huzaifa Active")
                    r.adjust_for_ambient_noise(source)  # Adjust for background noise
                    audio = r.listen(source, timeout=2)  # Listen with a timeout of 5 seconds

                    command = r.recognize_google(audio)  # Recognize speech using Google
                    print(f"Command: {word}")

                    processCommand(command)

            if "stop" in word.lower() or "exit" in word.lower():
                print("Huzaifa Inactive")
                speak("Huzaifa Inactive")
                break

        except Exception as e:
            print(f"Error : {e}")  # Catch and print any errors
            speak(f"Error : {e}")
            
