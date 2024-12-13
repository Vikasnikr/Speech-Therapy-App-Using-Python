from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
import pyttsx3
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.uix.video import Video
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget 
import threading 
from pydub import AudioSegment
import numpy as np
from kivy.uix.label import Label
from scipy.spatial import distance
import librosa
from scipy.spatial import distance
from kivy.uix.filechooser import FileChooser
from kivy.utils import platform
import sounddevice as sd
import wavio
from kivy.uix.progressbar import ProgressBar
import soundfile as sf
from scipy.signal import correlate
import speech_recognition as sr
from pydub import AudioSegment
import spacy
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from db_config import users_collection
from functools import partial

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        welcome_label = Label(text='Welcome to the Speech Therapy App', font_size='24sp', color=(0.2, 0.6, 0.8, 1), bold=True)
        login_button = Button(text='Login', size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        login_button.bind(on_press=self.go_to_login)
        layout.add_widget(welcome_label)
        layout.add_widget(login_button)
        layout.add_widget(Label(size_hint=(1, 1)))  # Filler to push the button upwards
        self.add_widget(layout)

    def go_to_login(self, instance):
        self.manager.current = 'login'


class LoginScreen(Screen):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        back_button = Button(text='<', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'y': 1})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        layout.add_widget(Label(text='Login', font_size='32sp', color=(0.1, 0.6, 0.8, 1)))

        self.username_input = TextInput(hint_text='Username', multiline=False, size_hint_y=None, height=40, background_color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.username_input)

        self.password_input = TextInput(hint_text='Password', password=True, multiline=False, size_hint_y=None, height=40, background_color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.password_input)

        login_button = Button(text='Login', size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        login_button.bind(on_press=self.validate_login)
        layout.add_widget(login_button)

        register_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, pos_hint={'center_x': 0.5})
        
        register_label = Label(text='Don\'t have an account? ', color=(0, 0, 0, 1))
        register_link = Button(text='Register here', size_hint=(None, None), size=(100, 30), background_color=(1, 1, 1, 0), color=(0.1, 0.6, 0.8, 1), underline=True)
        register_link.bind(on_press=self.go_to_register)

        register_layout.add_widget(register_label)
        register_layout.add_widget(register_link)

        layout.add_widget(register_layout)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'welcome'

    def validate_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            self.manager.current = 'home'
        else:
            self.show_popup('Login Failed', 'Invalid username or password!')

    def go_to_register(self, instance):
        self.manager.current = 'register'
        
    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, color=(1, 0, 0, 1))
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=[100, 0])
        popup_button = Button(text='OK', size_hint=(None, None), size=(100, 40), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        button_layout.add_widget(popup_button)
        
        popup_content.add_widget(popup_label)
        popup_content.add_widget(button_layout)
        
        popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(400, 200))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()


class RegisterScreen(Screen):
    username_input = ObjectProperty(None)
    email_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    confirm_password_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        back_button = Button(text='<', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'y': 1})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        layout.add_widget(Label(text='Create an Account', font_size='32sp', color=(0.1, 0.6, 0.8, 1)))

        self.username_input = TextInput(hint_text='Username', multiline=False, size_hint_y=None, height=40, background_color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.username_input)

        self.email_input = TextInput(hint_text='Email', multiline=False, size_hint_y=None, height=40, background_color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text='Password', password=True, multiline=False, size_hint_y=None, height=40, background_color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.password_input)

        self.confirm_password_input = TextInput(hint_text='Confirm Password', password=True, multiline=False, size_hint_y=None, height=40, background_color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.confirm_password_input)

        register_button = Button(text='Register', size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        register_button.bind(on_press=self.register_user)
        layout.add_widget(register_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'login'

    def register_user(self, instance):
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text
        
        if not username or not email or not password or not confirm_password:
            self.show_popup('Error', 'All fields are required!')
            return
        
        if password != confirm_password:
            self.show_popup('Error', 'Passwords do not match!')
            return

        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            self.show_popup('Error', 'Username already exists!')
            return

        users_collection.insert_one({"username": username, "email": email, "password": password})
        self.show_popup('Success', 'Account created successfully!')

        self.manager.current = 'login'

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, color=(1, 0, 0, 1))
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=[100, 0])
        popup_button = Button(text='OK', size_hint=(None, None), size=(100, 40), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        button_layout.add_widget(popup_button)
        
        popup_content.add_widget(popup_label)
        popup_content.add_widget(button_layout)
        
        popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(400, 200))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()






class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Back button
        back_button = Button(text='<', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'y': 1})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        layout.add_widget(Label(text='Welcome to Home Page!', font_size='32sp', color=(0.1, 0.6, 0.8, 1)))
        
        # Pronunciation Practice button
        pronunciation_button = Button(text='Pronunciation Practice', size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        pronunciation_button.bind(on_press=self.go_to_pronunciation_practice)
        layout.add_widget(pronunciation_button)

        # Recorded Audios button
        recorded_audios_button = Button(text='Text-To-Speech', size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        recorded_audios_button.bind(on_press=self.go_to_recorded_audios)
        layout.add_widget(recorded_audios_button)

        # Recorded Videos button
        recorded_videos_button = Button(text='Exercise Videos', size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        recorded_videos_button.bind(on_press=self.go_to_recorded_videos)
        layout.add_widget(recorded_videos_button)

        # Nlp button
        nlp_button = Button(text='Audio Analysing', size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        nlp_button.bind(on_press=self.go_to_nlp)
        layout.add_widget(nlp_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'login'
        
    def go_to_pronunciation_practice(self, instance):
        self.manager.current = 'levels'
        
    def go_to_recorded_audios(self, instance):
        self.manager.current = 'recorded_audios'

    def go_to_recorded_videos(self, instance):
        self.manager.current = 'recorded_videos'

    def go_to_nlp(self, instance):
        print("Nlp button clicked!")
        self.manager.current = 'feedback'


class RecordedAudiosScreen(Screen):
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RecordedAudiosScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        back_button = Button(text='<', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'y': 1})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        layout.add_widget(Label(text='Text-to-speech', font_size='32sp', color=(0.1, 0.6, 0.8, 1)))

        self.text_input = TextInput(hint_text='Enter text to convert to speech', multiline=True, size_hint_y=None, height=200, background_color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.text_input)

        convert_button = Button(text='Convert to Speech', size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        convert_button.bind(on_press=self.convert_text_to_speech)
        layout.add_widget(convert_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

    def convert_text_to_speech(self, instance):
        text = self.text_input.text
        if text:
            # Run the speak method in a separate thread to avoid blocking the main thread
            threading.Thread(target=self.speak, args=(text,)).start()

    def speak(self, text):
        # Initialize pyttsx3 engine
        engine = pyttsx3.init()
        # Convert text to speech
        engine.say(text)
        # Run the engine
        engine.runAndWait()



class LevelsScreen(Screen):
    def __init__(self, **kwargs):
        super(LevelsScreen, self).__init__(**kwargs)

        # Create a layout for the screen (using FloatLayout for free positioning)
        layout = FloatLayout()

        # Create the Back button and position it at the top-left corner
        back_button = Button(
            text="<", 
            size_hint=(None, None), 
            size=(50, 50), 
            background_color=(0.1, 0.6, 0.8, 1), 
            color=(1, 1, 1, 1), 
            font_size='30sp', 
            bold=True, 
            pos_hint={'top': 1, 'left': 0}
        )
        back_button.bind(on_press=self.go_home)

        # Add the Back button to the layout
        layout.add_widget(back_button)

        # Add a label for the heading at the top of the screen
        heading = Label(
            text="Select Level", 
            font_size=30, 
            size_hint=(None, None),
            size=(self.width, 60),  # Set a fixed height for the heading
            color=(0.1, 0.6, 0.8, 1),
            halign='center',
            valign='middle',
            pos_hint={'top': 1, 'center_x': 0.5}
        )
        layout.add_widget(heading)

        # Create buttons for Easy, Medium, and Hard
        easy_button = Button(
            text="Beginner", 
            size_hint=(None, None), 
            size=(200, 50),
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        medium_button = Button(
            text="Intermediate", 
            size_hint=(None, None), 
            size=(200, 50),
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        hard_button = Button(
            text="Advanced", 
            size_hint=(None, None), 
            size=(200, 50),
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )

        # Bind the easy button to navigate to the EasyWordsScreen
        easy_button.bind(on_press=self.go_to_easy_words)
        
        # Bind the medium button to navigate to the MediumWordsScreen
        medium_button.bind(on_press=self.go_to_medium_words)
        
        # Bind the hard button to navigate to the HardWordsScreen
        hard_button.bind(on_press=self.go_to_hard_words)

        # Add the buttons to the layout
        layout.add_widget(easy_button)
        layout.add_widget(medium_button)
        layout.add_widget(hard_button)

        # Add the layout to the screen
        self.add_widget(layout)

    def go_home(self, instance):
        # Navigate to the Home screen explicitly
        self.manager.current = 'home'  # Assuming 'home' is the name of your home screen

    def go_to_easy_words(self, instance):
        # Navigate to the EasyWordsScreen
        self.manager.current = 'easy_words'

    def go_to_medium_words(self, instance):
        # Navigate to the MediumWordsScreen
        self.manager.current = 'medium_words'

    def go_to_hard_words(self, instance):
        # Navigate to the HardWordsScreen
        self.manager.current = 'hard_words'

class EasyWordsScreen(Screen):
    def __init__(self, **kwargs):
        super(EasyWordsScreen, self).__init__(**kwargs)

        # Create the main layout, a BoxLayout with vertical orientation
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Create the back button at the top left corner
        back_button = Button(text="<", size_hint=(None, None), size=(50, 50),
                             background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1),
                             font_size='24sp', bold=True, pos_hint={'top': 1, 'left': 0})
        back_button.bind(on_press=self.go_back)  # Bind the back button to go back to LevelsScreen

        # Create the heading and align it to the center
        heading = Label(text="Beginner Words", font_size=32, size_hint_y=None, height=50, halign='center')
        heading.bind(size=heading.setter('text_size'))  # Ensure the text is centered

        # Add the back button and heading to the layout
        layout.add_widget(back_button)
        layout.add_widget(heading)

        # Add a spacer widget to create more space between the heading and the buttons
        spacer = Widget(size_hint_y=None, height=40)  # Adjust height for more space
        layout.add_widget(spacer)

        # Create a scrollable container for the word buttons
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)  # Increased spacing
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # List of easy words to display
        easy_words = ['Apple', 'Banana', 'Cat', 'Dog', 'Elephant', 'Fish', 'Grape', 'Hat', 'Ice', 'Jungle']

        # Create buttons for each word and add them to the scrollable layout
        for word in easy_words:
            button = Button(text=word, size_hint_y=None, height=50)
            button.bind(on_press=self.pronounce_word)  
            scroll_layout.add_widget(button)

        # Wrap the scroll_layout with a ScrollView to make it scrollable
        scroll_view = ScrollView()
        scroll_view.add_widget(scroll_layout)

        # Add the scroll view to the main layout
        layout.add_widget(scroll_view)

        # Set the layout as the root widget for this screen
        self.add_widget(layout)

    def go_back(self, instance):
        # Navigate back to the LevelsScreen
        self.manager.current = 'levels'

    def pronounce_word(self, instance):
        word = instance.text
        print(f"Pronouncing: {word}")
        # Run the pronunciation function in a new thread to prevent blocking the UI
        threading.Thread(target=self.speak, args=(word,)).start()

    def speak(self, word):
        # Initialize pyttsx3 engine
        engine = pyttsx3.init()
        # Pronounce the word
        engine.say(word)
        engine.runAndWait()


class MediumWordsScreen(Screen):
    def __init__(self, **kwargs):
        super(MediumWordsScreen, self).__init__(**kwargs)

        # Create the main layout, a BoxLayout with vertical orientation
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Create the back button at the top left corner
        back_button = Button(text="<", size_hint=(None, None), size=(50, 50),
                             background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1),
                             font_size='24sp', bold=True, pos_hint={'top': 1, 'left': 0})
        back_button.bind(on_press=self.go_back)  # Bind the back button to go back to LevelsScreen

        # Create the heading and align it to the center
        heading = Label(text="Intermediate Words", font_size=32, size_hint_y=None, height=50, halign='center')
        heading.bind(size=heading.setter('text_size'))  # Ensure the text is centered

        # Add the back button and heading to the layout
        layout.add_widget(back_button)
        layout.add_widget(heading)

        # Add a spacer widget to create more space between the heading and the buttons
        spacer = Widget(size_hint_y=None, height=40)  # Adjust height for more space
        layout.add_widget(spacer)

        # Create a scrollable container for the word buttons
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)  # Increased spacing
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # List of medium words to display
        medium_words = ['Abacus', 'Bicycle', 'Dolphin', 'Elephant', 'Hurricane', 
                        'Kangaroo', 'Lighthouse', 'Mountain',  
                        'Reliable', 'Snowstorm']

        # Create buttons for each word and add them to the scrollable layout
        for word in medium_words:
            button = Button(text=word, size_hint_y=None, height=50)
            button.bind(on_press=self.pronounce_word)  # Bind the button press to the pronounce_word method
            scroll_layout.add_widget(button)

        # Wrap the scroll_layout with a ScrollView to make it scrollable
        scroll_view = ScrollView()
        scroll_view.add_widget(scroll_layout)

        # Add the scroll view to the main layout
        layout.add_widget(scroll_view)

        # Set the layout as the root widget for this screen
        self.add_widget(layout)

    def go_back(self, instance):
        # Navigate back to the LevelsScreen
        self.manager.current = 'levels'

    def pronounce_word(self, instance):
        word = instance.text
        print(f"Pronouncing: {word}")
        # Run the pronunciation function in a new thread to prevent blocking the UI
        threading.Thread(target=self.speak, args=(word,)).start()

    def speak(self, word):
        # Initialize pyttsx3 engine
        engine = pyttsx3.init()
        # Pronounce the word
        engine.say(word)
        engine.runAndWait()



class HardWordsScreen(Screen):
    def __init__(self, **kwargs):
        super(HardWordsScreen, self).__init__(**kwargs)

        # Create the main layout, a BoxLayout with vertical orientation
        layout = BoxLayout(orientation='vertical', spacing=20, padding=[20, 50, 20, 20])

        # Create the Back button and position it at the top-left corner
        back_button = Button(
            text="<", 
            size_hint=(None, None), 
            size=(50, 50), 
            background_color=(0.1, 0.6, 0.8, 1), 
            color=(1, 1, 1, 1), 
            font_size='30sp', 
            bold=True
        )
        back_button.bind(on_press=self.go_back)

        # Create a layout for the heading and the back button
        heading_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        heading_layout.add_widget(back_button)

        # Create the heading and align it to the center
        heading = Label(text="Advanced Words", font_size=32, size_hint_y=None, height=50, halign='center', valign='middle')
        heading.bind(size=heading.setter('text_size'))  # Ensure the text is centered
        heading_layout.add_widget(heading)

        # Add the heading layout to the main layout
        layout.add_widget(heading_layout)

        # Create a scrollable container for the word buttons
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=[0, 20, 0, 0])
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # List of hard words to display
        hard_words = ['Unprecedented', 'Onomatopoeia', 'Phenomenon', 'Ambiguous', 'Resilience', 
                      'Quintessence', 'Melancholy', 'Epiphany', 'Petrichor', 'Serendipity']

        # Create buttons for each word and add them to the scrollable layout
        for word in hard_words:
            button = Button(text=word, size_hint_y=None, height=50)
            button.bind(on_press=self.pronounce_word)  # Bind the button press to the pronounce_word method
            scroll_layout.add_widget(button)

        # Wrap the scroll_layout with a ScrollView to make it scrollable
        scroll_view = ScrollView()
        scroll_view.add_widget(scroll_layout)

        # Add the scroll view to the main layout
        layout.add_widget(scroll_view)

        # Set the layout as the root widget for this screen
        self.add_widget(layout)

    def pronounce_word(self, instance):
        word = instance.text
        print(f"Pronouncing: {word}")
        # Run the pronunciation function in a new thread to prevent blocking the UI
        threading.Thread(target=self.speak, args=(word,)).start()

    def speak(self, word):
        # Initialize pyttsx3 engine
        engine = pyttsx3.init()
        # Pronounce the word
        engine.say(word)
        engine.runAndWait()

    def go_back(self, instance):
        # Navigate to the LevelsScreen
        self.manager.current = 'levels'



class RecordedVideosScreen(Screen):
    def __init__(self, **kwargs):
        super(RecordedVideosScreen, self).__init__(**kwargs)
        
        self.layout = FloatLayout()
        
        # Add a label for the heading at the top of the screen with more space from the top
        heading = Label(
            text="Recorded Videos", 
            font_size=30, 
            size_hint=(None, None),
            size=(self.width, 60),  # Set a fixed height for the heading
            color=(0.1, 0.6, 0.8, 1),
            halign='center',
            valign='middle',
            pos_hint={'top': 0.92, 'center_x': 0.5}  # Moved it higher
        )
        self.layout.add_widget(heading)
        
        # List of speech exercise videos
        self.video_list = [
            {"title": "Speech Exercise 1", "file": "Exercise1.mp4"},
            {"title": "Speech Exercise 2", "file": "Exercise2.mp4"},
            {"title": "Speech Exercise 3", "file": "Exercise3.mp4"},
            {"title": "Speech Exercise 4", "file": "Exercise4.mp4"},
            # Add more videos here
        ]
        
        # ScrollView to hold the video buttons
        self.scrollview = ScrollView(size_hint=(1, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.42})  # Adjusted the pos_hint for scrollview
        self.video_container = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.video_container.bind(minimum_height=self.video_container.setter('height'))
        self.scrollview.add_widget(self.video_container)
        
        # Add video buttons to the list
        for video in self.video_list:
            video_button = Button(
                text=video["title"],
                size_hint_y=None,
                height=40,
                background_color=(0.1, 0.6, 0.8, 1),
                color=(1, 1, 1, 1)
            )
            # Use partial to pass video title and file path correctly
            video_button.bind(on_press=partial(self.play_video, video["file"]))
            self.video_container.add_widget(video_button)
        
        self.layout.add_widget(self.scrollview)

        # Back button at the bottom
        back_button = Button(
            text='<', 
            size_hint=(None, None), 
            size=(50, 50), 
            pos_hint={'bottom': 0.05, 'left': 0},
            background_color=(0.1, 0.6, 0.8, 1), 
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)
    
    def go_back(self, instance):
        self.manager.current = 'home'
    
    def play_video(self, video_path, instance):
        # Create a popup layout to play the video
        popup_layout = BoxLayout(orientation='vertical')
        
        # Create the video widget
        video = Video(source=video_path, state='play', options={'eos': 'stop'}, size_hint=(1, 0.9))
        popup_layout.add_widget(video)
        
        # Close button to stop the video and close the popup
        close_button = Button(text='Close', size_hint=(1, 0.1), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        close_button.bind(on_press=lambda x: self.close_video(video, video_popup))
        popup_layout.add_widget(close_button)
        
        # Create the popup and open it
        video_popup = Popup(title='Play Video',
                            content=popup_layout,
                            size_hint=(0.9, 0.9))
        video_popup.open()
    
    def close_video(self, video, video_popup):
        # Stop the video and close the popup
        video.state = 'stop'
        video_popup.dismiss()



# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")

class FeedbackScreen(Screen):
    def __init__(self, **kwargs):
        super(FeedbackScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Back button
        back_button = Button(text='<', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'y': 1})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Title Label
        layout.add_widget(Label(text='Audio Analysing', font_size='32sp', color=(0.1, 0.6, 0.8, 1)))

        # Default recorded audios (displayed as buttons for example)
        recorded_audios_label = Label(text='Default Recorded Audios:', font_size='20sp', color=(0.1, 0.6, 0.8, 1))
        layout.add_widget(recorded_audios_label)

        # Example of default recorded audios buttons
        self.audio_1 = Button(text="Audio 1", size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        self.audio_1.bind(on_press=self.play_audio_1)
        layout.add_widget(self.audio_1)

        self.add_widget(layout)

        self.sound = None  # To store the current sound object

    def go_back(self, instance):
        self.manager.current = 'home'

    def play_audio_1(self, instance):
        self.play_audio('audio1.mp3', 'Audio 1')  # Replace with actual audio file path

    def play_audio_2(self, instance):
        self.play_audio('audio2.mp3', 'Audio 2')  # Replace with actual audio file path

    def play_audio_3(self, instance):
        self.play_audio('audio3.mp3', 'Audio 3')  # Replace with actual audio file path

    def play_audio(self, file_path, audio_name):
        # Load the audio
        self.sound = SoundLoader.load(file_path)

        if self.sound:
            self.sound.play()
            self.show_audio_popup(audio_name)
            self.update_audio_progress(0)  # Start progress update, initial value 0
        else:
            print("Error: Unable to load the audio file")
            # Handle the error and prevent the app from closing
            error_popup = Popup(title="Error", content=Label(text="Unable to load audio file. Please try again."), size_hint=(None, None), size=(300, 200))
            error_popup.open()

    def show_audio_popup(self, audio_name):
        # Create the content for the pop-up
        audio_popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Close button (X button at the top right of the pop-up)
        close_button = Button(text='X', size_hint=(None, None), size=(50, 50), pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=self.close_audio_popup)
        audio_popup_layout.add_widget(close_button)

        # Label to show the audio name with wrapping text
        audio_label = Label(
            text=f"Now Playing: {audio_name}",
            font_size='20sp',
            color=(0.1, 0.6, 0.8, 1),
            size_hint_y=None,
            height=40,
            text_size=(self.width * 0.8, None)  # Ensure the text wraps within the 80% width
        )
        audio_label.valign = 'middle'
        audio_label.halign = 'center'  # Align text to the center
        audio_popup_layout.add_widget(audio_label)

        # Duration label with spacing
        self.duration_label = Label(
            text=f"Duration: {self.sound.length:.2f} seconds",
            font_size='16sp',
            color=(0.1, 0.0, 0.8, 1),
            size_hint_y=None,
            height=30,
            text_size=(self.width * 0.8, None)  # Wrap text to fit within the 80% width
        )
        self.duration_label.valign = 'middle'
        self.duration_label.halign = 'center'  # Align text to the center
        audio_popup_layout.add_widget(self.duration_label)

        # Play/Pause button with improved alignment
        self.play_pause_button = Button(text="Play", size_hint=(None, None), size=(200, 50), background_color=(0.8, 0.8, 0.1, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        self.play_pause_button.bind(on_press=self.toggle_play_pause)
        audio_popup_layout.add_widget(self.play_pause_button)

        # Progress slider for audio
        self.progress_slider = Slider(min=0, max=self.sound.length, value=0, size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5})
        audio_popup_layout.add_widget(self.progress_slider)

        # Create the Popup
        self.audio_popup = Popup(title="Audio Player", content=audio_popup_layout, size_hint=(None, None), size=(self.width * 0.8, 350))  # Set pop-up width to 80% of screen width
        self.audio_popup.open()

    def update_audio_progress(self, dt):
        # Update the slider and duration label as the audio plays
        if self.sound:
            self.progress_slider.value = self.sound.get_pos()
            self.duration_label.text = f"Duration: {self.sound.length:.2f} seconds | Position: {self.sound.get_pos():.2f} seconds"

        # If audio is playing, schedule the update every 0.1 seconds
        if self.sound.state == 'play':
            Clock.schedule_once(self.update_audio_progress, 0.1)

    def toggle_play_pause(self, instance):
        # Pause the audio if it's playing, or play it if it's paused
        if self.sound.state == 'play':
            self.sound.stop()
            self.play_pause_button.text = "Play"
        else:
            self.sound.play()
            self.play_pause_button.text = "Pause"
            # Continue updating progress even after pause/play toggle
            Clock.schedule_once(self.update_audio_progress, 0)

    def close_audio_popup(self, instance):
        # Stop the sound and close the popup
        if self.sound:
            self.sound.stop()
        self.audio_popup.dismiss()

        # Show the new popup after closing the audio popup
        self.show_try_yourself_popup()

    def show_try_yourself_popup(self):
        # Create a new layout for the "Want to try yourself?" message and button
        try_yourself_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Label with the message
        try_yourself_label = Label(text="Want to try yourself?", font_size='20sp', color=(0.1, 0.6, 0.8, 1))
        try_yourself_layout.add_widget(try_yourself_label)

        # Buttons: "Later" and "Yes"
        button_layout = BoxLayout(size_hint=(None, None), size=(400, 50), spacing=20, pos_hint={'center_x': 0.5})
        later_button = Button(text="Later", background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        later_button.bind(on_press=self.close_try_yourself_popup)
        yes_button = Button(text="Yes", background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        yes_button.bind(on_press=self.go_to_record_screen)
        button_layout.add_widget(later_button)
        button_layout.add_widget(yes_button)
        try_yourself_layout.add_widget(button_layout)

        self.try_yourself_popup = Popup(title="Try Yourself", content=try_yourself_layout, size_hint=(None, None), size=(400, 300))
        self.try_yourself_popup.open()

    def go_to_record_screen(self, instance):
        # Transition to the new screen
        self.try_yourself_popup.dismiss()
        self.manager.current = 'record'

    def close_try_yourself_popup(self, instance):
        # Close the "Try Yourself" popup
        self.try_yourself_popup.dismiss()


nltk.data.path.append('C:/Users/jebap/AppData/Roaming/nltk_data')

nltk.download('punkt')  # Download punkt tokenizer for NLP


import threading
import numpy as np
import sounddevice as sd
import wavio
import librosa
import speech_recognition as sr
from nltk import word_tokenize, FreqDist
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

class RecordScreen(Screen):
    def __init__(self, **kwargs):
        super(RecordScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Back Button
        back_button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        back_button = Button(text="<", size_hint=(None, None), size=(50, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        back_button.bind(on_press=self.go_back)
        back_button_layout.add_widget(back_button)
        layout.add_widget(back_button_layout)

        # Title Label
        layout.add_widget(Label(text='Try Yourself', font_size='32sp', color=(0.1, 0.6, 0.8, 1)))

        # Record Button
        self.record_button = Button(text="Start Recording", size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1), pos_hint={'center_x': 0.5})
        self.record_button.bind(on_press=self.start_recording)
        layout.add_widget(self.record_button)

        self.add_widget(layout)

        self.is_recording = False
        self.recording_thread = None
        self.progress_popup = None
        self.stream = None

    def go_back(self, instance):
        self.manager.current = self.manager.previous()  # Navigate to the previous screen

    def start_recording(self, instance):
        if not self.is_recording:
            self.is_recording = True
            self.record_button.text = "Recording..."
            self.show_recording_progress()

            # Start the recording in a separate thread
            self.recording_thread = threading.Thread(target=self.record_voice)
            self.recording_thread.start()

    def record_voice(self):
        fs = 44100  # Sample rate
        duration = 10  # Duration in seconds
        self.recorded_data = []

        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.recorded_data.append(indata.copy())

        self.stream = sd.InputStream(samplerate=fs, channels=2, callback=callback)
        with self.stream:
            while self.is_recording:
                sd.sleep(100)

        self.save_recording()

    def save_recording(self):
        if self.recorded_data:
            wav_data = np.concatenate(self.recorded_data, axis=0)
            wavio.write("recording.wav", wav_data, 44100, sampwidth=2)
        self.record_button.text = "Start Recording"
        self.close_recording_progress()
        self.analyze_audio()

    def show_recording_progress(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text='Recording in progress...', font_size='18sp', color=(0.1, 0.6, 0.8, 1)))

        self.progress_bar = ProgressBar(max=10)
        layout.add_widget(self.progress_bar)

        stop_button = Button(text="Stop Recording", size_hint=(None, None), size=(200, 50), background_color=(0.1, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        stop_button.bind(on_press=self.stop_recording)
        layout.add_widget(stop_button)

        self.progress_popup = Popup(title="Recording", content=layout, size_hint=(None, None), size=(400, 200))
        self.progress_popup.open()

        Clock.schedule_interval(self.update_progress, 1)

    def update_progress(self, dt):
        if self.is_recording:
            self.progress_bar.value += dt
        else:
            Clock.unschedule(self.update_progress)

    def stop_recording(self, instance):
        if self.is_recording:
            self.is_recording = False
            if self.stream:
                self.stream.stop()
                self.stream.close()
            self.close_recording_progress()  # Close the popup when stopping recording

    def close_recording_progress(self):
        if self.progress_popup:
            self.progress_popup.dismiss()

    def analyze_audio(self):
        print("Analyzing audio...")  # Debug statement
        try:
            # Load the recorded audio
            user_audio, sampl_rate = librosa.load("recording.wav", sr=None)

            # Convert the audio to text using Speech Recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile("recording.wav") as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)

            # Analyze the transcribed text using NLP
            feedback = self.analyze_text(text)

            # Display feedback
            print(feedback)  # Debug statement
            Clock.schedule_once(lambda dt: self.show_feedback_popup(feedback))
        except Exception as e:
            print(f"Error analyzing audio: {e}")  # Debug statement
            Clock.schedule_once(lambda dt, err=str(e): self.show_feedback_popup(f"Error analyzing audio: {err}"))

    def analyze_text(self, text):
        # Tokenize the text and analyze it
        tokens = word_tokenize(text)
        word_freq = FreqDist(tokens)

        # Check for repeated words
        repeated_words = [word for word, count in word_freq.items() if count > 1]

        # Check for long pauses (based on gaps in the words)
        gaps_detected = False
        if len(tokens) > 1:
            # Check for large gaps between words
            for i in range(1, len(tokens)):
                if abs(len(tokens[i]) - len(tokens[i-1])) > 2:  # Threshold for gap detection
                    gaps_detected = True
                    break

        # Generate feedback based on analysis
        if gaps_detected or repeated_words:
            feedback = "\n\nFeedback:\nImprovement needed!\nAvoid gaps and repetition\nin your speech."
        else:
            feedback = "\n\nFeedback:\nGood job!\nNo significant gaps or repeated\nwords detected."

        return feedback

    def show_feedback_popup(self, feedback):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
    
        # Feedback Label to show the message
        feedback_label = Label(
            text=feedback,
            font_size='18sp',
            color=(0.1, 0.6, 0.8, 1),
            valign='middle',
            halign='center',
            size_hint_y=None,  # Allow the height to adjust dynamically
            height=200  # Set a minimum height for the feedback label
        )
    
        # Add feedback label to the layout
        layout.add_widget(feedback_label)

        # Close button to dismiss the popup
        close_button = Button(
            text="Close",
            size_hint=(None, None),
            size=(200, 50),
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        close_button.bind(on_press=self.close_feedback_popup)
        layout.add_widget(close_button)

        # Create the popup and set the layout
        self.feedback_popup = Popup(
            title="Analysis Feedback",
            content=layout,
            size_hint=(None, None),
            size=(400, 300)
        )
        self.feedback_popup.open()

    def close_feedback_popup(self, instance):
        if self.feedback_popup:
            self.feedback_popup.dismiss()



class SpeechTherapyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RecordedAudiosScreen(name='recorded_audios'))
        sm.add_widget(LevelsScreen(name='levels'))
        sm.add_widget(EasyWordsScreen(name='easy_words'))
        sm.add_widget(MediumWordsScreen(name='medium_words'))
        sm.add_widget(HardWordsScreen(name='hard_words')) 
        sm.add_widget(RecordedVideosScreen(name='recorded_videos')) 
        sm.add_widget(FeedbackScreen(name='feedback'))
        sm.add_widget(RecordScreen(name='record'))
        return sm

if __name__ == '__main__':
    SpeechTherapyApp().run()
