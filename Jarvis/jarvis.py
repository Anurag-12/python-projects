import pyttsx3 #  pip install pyttsx3
import datetime 
import speech_recognition as sr # pip install speechRecognition   and pip install pipwin  & pipwin install pyaudio
import wikipedia  # pip install wikipedia
import webbrowser
import os
import random
import pywhatkit


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def sendEmail(to, content):  # first google and enable less secure app for using it 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning! I am Jarvis sir. Please tell me how may I help you ?")
    elif hour>=12 and hour<18:
        speak("Good Afternoon! I am Jarvis sir. Please tell me how may I help you ?")
    else:
        speak("Good evening! I am Jarvis sir. Please tell me how may I help you ?")

def takeCommand(): # this will take voice input from the user using microphone and give output as string 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language = "en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Say that again please....")
        return "None"
    return query

if __name__ == "__main__" :
    wishMe()
    #speak("Anurag is my hero")
    while True:
        query = takeCommand().lower()
         # logic based on query to execute the command
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            
            #chromePath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            #c = webbrowser.get(os.startfile(chromePath))
            #os.startfile(chromePath)
            #webbrowser.open_new_tab(url)
            urL='https://www.google.com'
            chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get('chrome').open_new_tab('https://www.youtube.com/')
            webbrowser.get('chrome').open_new_tab('https://eap.iags.ikea.com/logon/LogonPoint/index.html')
            #c.open("google.com")
            #c.open_new_tab("youtube.com")
            #c.open_new('youtube.com')
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            
        elif 'open code' in query:
            codePath = 'C:\\Users\\AnuragGupta\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
            os.startfile(codePath)
        elif 'play' in query:
            song = query.replace("play","")
            pywhatkit.playonyt(song)
        
        elif 'message' in query:
            speak("What should I say?")
            content = takeCommand()
            pywhatkit.sendwhatmsg(f"+91{**********}",content,14,44)


        elif 'exit' in query:
            exit()

        '''elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "harryyourEmail@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry bhai. I am not able to send this email")    

            elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0])) # to play first songs in the dir
            os.startfile(os.path.join(music_dir, random.choice(songs))) # to play random songs in the dir '''

        


