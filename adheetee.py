# -*- coding: utf-8 -*-
__author__ = "Syed Mohidul Islam, Fowziya Akther, Syed Mynul Islam"
__copyright__ = "Copyright (C) 2004 Syed Mohidul Islam, Fowziya Akther, Syed Mynul Islam"
__license__ = "Public Domain"
__version__ = "1.0"


import importlib
import sys
from apixu.client import ApixuClient, ApixuException
from PyQt5.QtWidgets import QSplitter, QApplication,QVBoxLayout, QWidget,QTextEdit,QHBoxLayout, QMainWindow, QLabel, QLineEdit,QPushButton,QPlainTextEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPixmap, QFont, QFontDatabase
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QCoreApplication, pyqtSignal,QUrl
import random
import requests
import json
from PyQt5 import QtWebEngineWidgets
from weather import Weather, Unit
import speech_recognition as sr
from google.cloud import translate
from gtts import gTTS
import pyglet
from datetime import datetime
import os
import bangla
import smtplib
import httplib2
import os,re
import oauth2client
from oauth2client import client, tools
import base64
import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import urllib.request, json
import importlib
import time

module = importlib.import_module("contry and currency")
country_information = module.country_information()

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

from PyQt5.QtWebEngineWidgets import QWebEngineSettings
import aiml
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\fowzi\Desktop\BanglaAIAssistant\Bangla AI assistant-1998417a0834.json"
translate_client = translate.Client()


class window(QMainWindow):
    def __init__(self,parent=None):
        #print('1 hi')
        #self.data = datam
        super(window, self).__init__(parent)

    def widget(self,search):
        self.centralwid = QWidget(self)
        self.vlayout = QVBoxLayout()
        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.webview.setUrl(QUrl(search))
        self.vlayout.addWidget(self.webview)
        self.centralwid.setLayout(self.vlayout)
        self.setCentralWidget(self.centralwid)



    def youtube_search(self,data):
        query = ""
        for i in data:
            query += i
            query += '+'
        #print(query[:-1])

        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        search = "https://www.youtube.com/results?search_query="+ query[:-1]
        #search = "https://www.google.com/maps/dir/Lane+No+12,+Dhaka+1216/Govt.+Teachers'+Training+College,+New+Market+-+Pilkhana+Rd,+Dhaka+1205"
        self.widget(search)



    def google_search(self,data):
       # print(query[:-1])
        print("q",data)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        search = "https://www.google.com/search?q="+ data
        self.widget(search)

    def map_search(self,origin,destination):
        orgn = ""
        dest = ""
        for i in origin:
            orgn += i
            orgn += '+'
        #print(orgn[:-1])
        for i in destination:
            dest += i
            dest += '+'
        #print(dest[:-1])
        map_url ="https://www.google.com/maps/dir/"
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        search = map_url + origin + '/'+destination

        response = requests.get(
            'https://maps.googleapis.com/maps/api/directions/json?origin=mirpur+10&destination=dhanmondi+27&key=AIzaSyBl0LiJQvtWY97ZCcT5myjiRyP6W7iV6vE')
        json_data = json.loads(response.text)

        s = json_data['routes'][0]["legs"][0]["steps"]
        clean_text = []
        #print(len(json_data['routes'][0]["legs"][0]["steps"]))
        for i in range(len(json_data['routes'][0]["legs"][0]["steps"])):
            clean_text.append(((((s[i]['html_instructions']).replace('<b>', '')).replace('</b>', '')).replace(
                '<div style="font-size:0.9em">', ' ')).replace('</div>', '')+'.')
        #print('clean text',clean_text)
        c = ''
        raw_text = []
        for i in range(len(clean_text)):
            k = clean_text[i]
            for j in range(len(k)):
                if k[j] != ' ' :
                    c += k[j]
                else:
                    raw_text.append(c)
                    c = ''
            raw_text.append(c)
        self.widget(search)
        return raw_text




class App(QMainWindow):

    def __init__(self,parent=None):
        super(App,self).__init__(parent)
        self.title = 'Bangla Virtual AI Assistant'
        #window position set
        self.left = 10
        self.top = 300
        self.width = 440
        self.height = 430
        self.user_name = ""
        self.micon = 0
        self.mic_input = ""
        self.weather_api_call()
        self.initUI()
        self.messages = []



    def weather_api_call(self):
        ip = requests.get('https://api.ipify.org').text

        get_location_data = requests.get(
            "http://api.ipstack.com/" + ip + "?access_key=e790f7d801cff8e96c401511babdd640")
        get_location_json = json.loads(get_location_data.text)

        city = get_location_json['city']
        self.city = translate_client.translate(city , target_language='bn')['translatedText']
        zip = get_location_json['zip']
        self.city += "-" + str(bangla.convert_english_digit_to_bangla_digit(zip))
        latitude = get_location_json['latitude']
        longitude = get_location_json['longitude']
        get_weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather?&zip=" + str(
            zip) + ",bd&APPID=f36cd282a633b2eca9174bfb9d8335a3")  

        get_weather_json = json.loads(get_weather_data.text)
        js_data = json.dumps(get_weather_json, indent=2)

        description = get_weather_json['weather'][0]['description']
        self.description = translate_client.translate(description , target_language='bn')['translatedText']
        #print(self.description)
        temp = get_weather_json['main']['temp']
        temp = int(temp)
        self.temp = bangla.convert_english_digit_to_bangla_digit(temp - 273)
        temp_min = get_weather_json['main']['temp_min']
        temp_min = int(temp_min)
        self.temp_min = bangla.convert_english_digit_to_bangla_digit(temp_min -273)
        temp_max = get_weather_json['main']['temp_max']
        temp_max = int(temp_max)
        self.temp_max = bangla.convert_english_digit_to_bangla_digit(temp_max -273)
        humidity = get_weather_json['main']['humidity']
        self.humidity = bangla.convert_english_digit_to_bangla_digit(humidity)+'%'
        wind = get_weather_json['wind']['speed']
        self.wind_speed = bangla.convert_english_digit_to_bangla_digit(wind)+' কি.মি./ঘন্টা'
        sunrise = get_weather_json['sys']['sunrise']

        sunrise = datetime.fromtimestamp(sunrise).strftime("%A, %B %d, %Y %I:%M:%S")
        self.sunrise = translate_client.translate(sunrise, target_language='bn')['translatedText']

        self.date = self.sunrise[:27]
        self.date = bangla.convert_english_digit_to_bangla_digit(self.date)

        self.sunrise = bangla.convert_english_digit_to_bangla_digit(self.sunrise[27:])

        sunset = get_weather_json['sys']['sunset']
        sunset = datetime.fromtimestamp(sunset).strftime("%A, %B %d, %Y %I:%M:%S")
        self.sunset = translate_client.translate(sunset, target_language='bn')['translatedText']
        self.sunset = bangla.convert_english_digit_to_bangla_digit(self.sunset[27:])

        #print(self.temp," ",self.temp_max," ",self.humidity," ",self.wind_speed,' ', self.sunrise,' ',self.date)
    def initUI(self):
        #set window title
        self.setWindowTitle(self.title)
         #Set window size
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.chatBody = QVBoxLayout(self)

        self.chatRead = QTextEdit(self)
        self.chatRead.setReadOnly(True)
        self.chatRead.resize(430,360)
        self.chatRead.move(5,0)
        font = self.chatRead.fontPointSize()
        #print(font)
        # self.chatRead.setFont(font)
        self.chatRead.setStyleSheet("QTextEdit { border: 1px solid black;}"
                                   )

        self.textbox = QTextEdit(self)

        font = self.textbox.font()  # lineedit current font
        font.setPointSize(11)  # change it's size
        self.textbox.setFont(font)  # set font

        #textbox design details
        self.textbox.setStyleSheet("QTextEdit { border: 1px solid black;"
                                             "border-radius: 10px;}")
        self.textbox.move(10, 379)
        #textbox position
        self.textbox.resize(335, 40)




        #button example
        button = QPushButton(self)
        #show suggestion after hovering
        button.setToolTip('This is an example button')
        button.move(382, 373)
        button.resize(50,50)

        #change button's default design
        #Microphone button's details
        button.setStyleSheet("QPushButton{border-image: url(mic1.png);"
                             "border-style: outset;"
                                "border-width: 2px;"
                                "border-radius: 25px;"
                                "border-color: black;"
                                "padding: 4px;}"
                                "QPushButton:pressed { border-image: url(mic2.png);}")

        #button.clicked.connect(self.mic_pressed)
        button.pressed.connect(self.mic_pressed)

        #Send Button's details
        sbutton = QPushButton(self)
        sbutton.setToolTip('This is an example button')
        sbutton.move(350, 379)
        sbutton.resize(40, 40)
        sbutton.setStyleSheet(  "QPushButton{border-image: url(send5.png);"
                                "border-style: outset;"
                                "border-width: 2px;"
                                "border-radius: 25px;"
                                "border-color: black;"
                                "padding: 4px;}"
                                "QPushButton:pressed { border-image: url(send.png);}")

        sbutton.clicked.connect(self.button_pressed)


        horizontal_box_top = QHBoxLayout()
        horizontal_box_top.addWidget(self.chatRead)

        horizontal_box_bottom = QHBoxLayout()
        horizontal_box_bottom.addWidget(self.textbox)
        horizontal_box_bottom.addWidget(button)
        horizontal_box_bottom.addWidget(sbutton)



        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        painter.setPen(QPen(Qt.white, 4, Qt.SolidLine))

        painter.drawRect(0,370,440,430)


        painter2 = QPainter(self)

        painter2.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        painter2.setPen(QPen(Qt.white, 4, Qt.SolidLine))

        painter2.drawRect(10, 1, 440, 430)

    def allignment(self, data):
        words = data.split()
        space = ""
        text = ""
        flag = 1
        length = len(words)
        demo = words[0] + " "
        line_size = 25
        char_length = len(demo)

        for i in range(1,length):
            if((char_length + len(words[i])+1)<= line_size):
                demo += words[i] +" "
                char_length = len(demo)
            else:
                #sp = 65 - char_length
                space =""
                #print(sp)
                for j in range(43):
                    space = space + " "
                #print(len(space))
                demo = space + demo
                text += demo + '\n'
                demo = words[i] + " "
                char_length = len(demo)
                #print(char_length)
                flag = 0


        if (flag):
            sp = 75 - char_length
            space = ""
            for j in range(43):
                space += " "

            demo = space + demo
            demo += "\n"
            #print(flag)

            return demo

        sp = 75 - char_length
        space = ""
        for j in range(43):
            space += " "

        return text+space+demo


    def find_country(self,string):
        flag = 0
        s = []
        for i in range(len(string)):
            #print('5',string[i]+" " )
            if string[i] == 'of' or string[i] == 'in' or string[i] == 'about' or string[i] == "report":
                #print('6', string[i] + " ")
                flag =1
                return string[i+1 :]
        if flag == 0:
            for i in range(len(string)):
                if string[i] == 'capital' or string[i] == 'currency' or string[i] == 'language' or string[i] == 'continent':
                    #print()
                    pass
                else:
                    s.append(string[i])
            return s

        self.chatRead.append("দুঃখিত, আপনি যা বলেছেন\nআমি তা বুঝতে পারি নাই।")


    def mail_api(self,string):
       # print(string)
        # to = "pcapstone63@gmail.com"
        sender = "pcapstone63@gmail.com"
        subject = "subject"
        temp = 0
        for i in range(len(string)):
            receiver =  string[i]
            if('@' in receiver):
                receiver = string[i]
                temp = i
                break

        #print(receiver)
        to = ''.join(receiver)
        #print(to)

        body_str = string[temp+1:]
        #print(body_str)
        raw_body = ''
        for i in range(len(body_str)):
            raw_body += body_str[i]+" "
        translt = translate_client.translate(raw_body, target_language='en')
        source_language = translt['detectedSourceLanguage']
        #print(source_language)
        # string = string['translatedText']
        #print(translt)

        for i in range(len(string)):
            if string[i] == 'that':
                body =  string[i+1: ]
                break
            elif string[i] == 'মেইল':
                if string[i+2] == 'যে':
                    body =  string[i+3: ]
                else:
                    body = string[i+2:]
                break
        #print(body)
        msgHtml = ''
        for i in range(len(body)):
            msgHtml += ''.join(body[i])
            msgHtml += ' '

        #print(msgHtml)
        #msgHtml = "Hi<br/>Html Email"
        msgPlain = "Hi\nPlain Email"

        def get_credentials():
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
            store = oauth2client.file.Storage(credential_path)
            credentials = store.get()
            if not credentials or credentials.invalid:
                flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
                flow.user_agent = APPLICATION_NAME
                credentials = tools.run_flow(flow, store)
                #print('Storing credentials to ' + credential_path)
            return credentials

        def SendMessage(sender, to, subject, msgHtml, msgPlain):
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('gmail', 'v1', http=http)
            message1 = CreateMessage(sender, to, subject, msgHtml, msgPlain)
            SendMessageInternal(service, "me", message1)

        def SendMessageInternal(service, user_id, message):
            try:
                message = (service.users().messages().send(userId=user_id, body=message).execute())
                #print('Message Id: %s' % message['id'])
                self.chatRead.append("সফলভাবে আপনার মেইলটি\nপাঠানো হয়েছে")
                return message
            except errors.HttpError as error:
                #print('An error occurred: %s' % error)
                self.chatRead.append("একটি ত্রুটি দেখা দিয়েছে।")

        def CreateMessage(sender, to, subject, msgHtml, msgPlain):
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = to
            msg.attach(MIMEText(msgPlain, 'plain'))
            msg.attach(MIMEText(msgHtml, 'html'))
            raw = base64.urlsafe_b64encode(msg.as_bytes())
            raw = raw.decode()
            body = {'raw': raw}
            return body

        SendMessage(sender, to, subject, msgHtml, msgPlain)

    def break_words(self,str):
        #print(str [0])
        char_count = 0

        text = ''
        for i in range(len(str)):
            if char_count + len(str[i]) + 1 <= 30:
                text += str[i] + ' '
                char_count += len(str[i]) + 1
            else:
                text += '\n'
                text += str[i] + " "
                char_count = 0
                char_count += len(str[i]) + 1

        return text

    def mic_pressed(self):
        r = sr.Recognizer()
        self.micon = 1

        with sr.Microphone() as source:
            #print("Please wait. Calibrating microphone...")
            # listen for 5 seconds and create the ambient noise energy level
            # r.adjust_for_ambient_noise(source, duration=5)
            #print("Say something!")
            audio = r.listen(source)

            # recognize speech using Sphinx
        try:
            self.mic_input = r.recognize_google(audio, language='bn-BD')
            #print("Google thinks you said '" + self.mic_input + "'")

            # translate_text(text)
        except sr.UnknownValueError:
            self.chatRead.append("আপনার কথা বোঝা যাচ্ছেনা।\n অনুগ্রহ করে আবার বলুন।")
        except sr.RequestError as e:
            pass
            #print("Request error; {0}".format(e))
        self.button_pressed()


    def button_pressed(self):
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("SolaimanLipi_20-04-07.ttf")
        # families = font_db.applicationFontFamilies(font_id)
        fontb = QFont("SolaimanLipi",13)

        if self.micon == 0:
            data = self.textbox.toPlainText()
        elif self.micon == 1:
            print(self.mic_input)
            data = self.mic_input

        font = self.chatRead.font()  # lineedit current font
        self.chatRead.setFont(fontb)  # set font
        alligned_text = self.allignment(data)
        self.chatRead.append(alligned_text)
        # self.chatRead.append()
        data = data.lower()
        data = data.replace(","," ")

        words = data.split()
        # split the sentence into individual words

        if 'আবহাওয়া' in words or 'weather' in words or 'আবহাওয়ার' in words: # see if one of the words in the sentence is the word we want
            # self.chatRead.append(self.cur_city)
            # print('city name: '+ self.cur_city)
            self.chatRead.append(self.city)
            self.chatRead.append(self.date)
            textFormatted = '{:>5}'.format('তাপমাত্রা :\n'  + self.temp + ' ডিগ্রী সেলসিয়াস')
            self.chatRead.append(textFormatted)
            self.chatRead.append('সর্বনিম্ন তাপমাত্রা ' + ' :\n' + self.temp_min + ' ডিগ্রী সেলসিয়াস')
            self.chatRead.append('সর্বোচ্চ তাপমাত্রা' + ' :\n' + self.temp_max + ' ডিগ্রী সেলসিয়াস')
            textFormatted = '{:>5}'.format( 'আদ্রতা :  ' + self.humidity)
            self.chatRead.append(textFormatted)
            self.chatRead.append('বাতাসের বেগ '+' :\n'+ self.wind_speed)
            self.chatRead.append('আকাশের অবস্থা ' + ' :  ' + self.description)
            self.chatRead.append('সূর্যোদয়' + ' :\n' +'ভোর ' +self.sunrise)
            self.chatRead.append('সূর্যাস্ত' + ' :\n' + 'বিকাল '+self.sunset)
            # self.chatRead.append(self.date)
            #print("help")

        elif'তাপমাত্রা' in words:
             textFormatted = '{:>5}'.format(self.city + 'র তাপমাত্রা :  ' + self.temp + ' ডিগ্রী সেলসিয়াস')

        #     self.chatRead.append(textFormatted)

        elif 'youtube' in words or 'video' in words or 'ইউটিউব' in words or 'ভিডিও' in words:
            self.youtube = window(self)
            self.youtube.youtube_search(words)
            self.youtube.show()



        elif 'map' in words or 'maps' in words or 'location' in words or ('show' in words and 'direction' in words) or 'রাস্তা' in words or 'ম্যাপ' in words or 'যাব' in words:
            data = translate_client.translate(data, target_language='en')
            data = data['translatedText']
            #print("map: ", data)
            words = data.split()
            if 'to' in words:
                o_count = 0
                d_count = 0
                origin = ''
                destination = ''
                for i in range(len(words)):
                    if words[i] == 'from':
                        for o in range(i,len(words)):
                            if words[o] == 'to':
                                for k in range(o,len(words)):
                                    destination += words[k]+' '
                                break
                            origin += words[o] + ' '

                origin = origin[5:]
                destination = destination[3:]

                print("originm = " , origin)
                print("destination = ", destination)
                self.map = window(self)
                string = self.map.map_search(origin, destination)
                msg = 'Here is the steps you \nneed to follow : ' + '\n'
                string = self.break_words(string)
                self.chatRead.append(string)

                self.map.show()


            else:
                self.chatRead.append("দয়া করে আপনি কোথায় আছেন\nএবং কোথায় যাবেন তা বলুন")

        elif 'mail' in words or 'gmail' in words or 'মেইল' in words or 'জিমেইল' in words:

            # data = translate_client.translate(data, target_language='en')
            # data = data['translatedText']
            #print(data)
            words = data.split()
            #print(words)
            self.mail_api(words)



        elif ('country' in words and 'information') or 'তথ্য' in words :
            flag = 0
            country =""
            data = translate_client.translate(data, target_language='en')
            data = data['translatedText']
            #print('1' + data)
            data = re.sub('[?&#;1234567890]+', '', data)
            #print('2' + data)
            words = data.split()
            # U = self.find_country(words)
            # print("bandor", U)
            # country = ""
            # print("length ",len(U))
            # for i  in range(len(U)):
            #     D = U[i]
            #     print("Unda ", U)
            #     c = D[0].upper()
            #     print(c)
            #     country += c + D[1:]+" "
            # country = country[:-1]
            # print("country : ",country +" lomba ",len(country))
            fl = 0
            for key in country_information.keys():
               c = key.split()

               for i in range(len(words)):
                   if words[i]== c[0]:
                       for j in range(len(c)):
                           if(words[i+j] == c[j]):
                               #print(j," ",c[j]+"\n")
                               country += c[j]+" "
                       if(len(country) == len(key)+1):
                           #print(len(country),' ',len(key))
                           fl = 1
                           break
                       else:
                            country = ""
               if fl == 1:
                   break
            if(country==""):
                self.chatRead.append("দেশের নাম সঠিক হয়নি")
            country = country[:-1]
            #print(country)

            if country in country_information:
                a = "রাজধানী: " + country_information[country][0] + ' '
                a = a.split()
                a = self.break_words(a)
                text = a+'\n'
                b = "মুদ্রা: " + country_information[country][1] + ' '
                b = b.split()
                b = self.break_words(b)
                text += b + '\n'
                c = "ভাষা: " + country_information[country][2] + ' '
                c = c.split()
                c = self.break_words(c)
                text += c + '\n'
                d = "মহাদেশ: " + country_information[country][3]
                d = d.split()
                d = self.break_words(d)
                text += d
                self.chatRead.append(text)

            else:
                self.chatRead.append("দয়া করে সঠিক\nদেশের নাম লিখুন।")



        elif 'capital' in words or 'currency' in words or 'continent' in words or 'language' in words or 'মুদ্রা' in words or 'রাজধানী' in words or 'ভাষা' in words or 'মহাদেশ' in words or 'মুদ্রার' in words or 'রাজধানীর' in words or 'ভাষার' in words or 'মহাদেশের' in words or 'মহাদেশে' in words:
            flag = 0
            if 'অবস্থিত' in data:
                flag = 1
            data = translate_client.translate(data, target_language='en')
            data = data['translatedText']
            #print('1'+data)
            data = re.sub('[?&#;1234567890]+', '', data)
            #print('2'+data)
            words = data.split()
            for i in range(len(words)):
                if words[i] =='Comoros' or words[i] == 'Philippines' or words[i] == 'Netherlands' or words[i] == 'Kitts' or words[i] == 'Nevis':
                    #print("")
                    pass
                else:
                    l = len(words[i])
                    s = words[i]
                    if s[l - 1] == 's':
                        words[i] = words[i][:-1]


            print('3', words)
            if flag == 0:
                U = self.find_country(words)
                #print('4',U)
                country = ""
                for i in range(len(U)):
                    if U[i] != "the" :
                        #print(U[i])
                        if U[0] == 'Cote':
                            country = 'Cote D\'ivoire'
                            break;
                        country += U[i][0].upper() + U[i][1:]
                        if (i < len(U) - 1):
                            country += " "
                # print(country)
            else:
                country = words[0]
                #print("মহাদেশঃ",country)
                #print(country_information[country][3])
            print("4", country)
            if country in country_information:
                if 'capital' in words or 'Capital' in words:
                    text = "রাজধানী : " + country_information[country][0]
                    text = text.split()
                    text = self.break_words(text)
                    self.chatRead.append(text)
                if 'currency' in words or 'Currency' in words:
                    text = "মুদ্রা: " + country_information[country][1]
                    text = text.split()
                    text = self.break_words(text)
                    self.chatRead.append(text)
                if 'ভাষা' in words or 'language' in words or 'Language' in words:
                    text = "ভাষা: " + country_information[country][2]
                    text = text.split()
                    text = self.break_words(text)
                    self.chatRead.append(text)
                if 'মহাদেশ' in words or 'continent'in words or 'Continent' in words:
                    text = "মহাদেশ: " + country_information[country][3]
                    text = text.split()
                    text = self.break_words(text)
                    self.chatRead.append(text)

            else:
                self.chatRead.append('দেশের নাম ভুল\nসঠিক নাম দিন।')

        elif ('open' in words and 'browser' in words) or ('launch' in words and 'browser' in words) or ('ওপেন' in words and 'ব্রাউজার' in words) or ('খোল' in words and 'ব্রাউজার' in words) \
                or 'firefox'  in words or 'ফায়ারফক্স' in words or 'opera' in words or 'অপেরা' in words or 'chrome' in words or 'ক্রম' in words or 'ক্রোম' in words \
                        or 'edge' in words or 'এজ' in words or 'সাফারি' in words:
            urL = "www.google.com"
            chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
            opera_path = r"C:\Users\fowzi\AppData\Local\Programs\Opera\launcher.exe"

            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path), 1)
            webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path), 1)
            webbrowser.register('opera', None, webbrowser.BackgroundBrowser(opera_path), 1)
            if 'firefox' not in words or  'ফায়ারফক্স' not in words or 'opera' not in words or 'অপেরা' not in words or 'chrome' not in words or 'ক্রম' not in words or 'ক্রোম' not in words \
                    or 'edge' not in words or 'এজ' not in words or 'সাফারি' not in words :
                self.chatRead.append("কাঙ্ক্ষিত ব্রাউজার এর\nনাম বলুন")

            if 'firefox' in words or  'ফায়ারফক্স' in words or ('ফায়ার'in words and 'ফক্স' in words):
                self.chatRead.append("কাঙ্ক্ষিত ব্রাউজারটি চালু\nহচ্ছে")
                webbrowser.get('firefox').open_new(urL)
            elif 'opera' in words or 'অপেরা' in words :
                self.chatRead.append("কাঙ্ক্ষিত ব্রাউজারটি চালু\nহচ্ছে")
                webbrowser.get('opera').open_new(urL)
            elif 'chrome' in words or 'ক্রম' in words or 'ক্রোম' in words:
                self.chatRead.append("কাঙ্ক্ষিত ব্রাউজারটি চালু\nহচ্ছে")
                webbrowser.get('chrome').open_new(urL)
            elif 'edge' in words or 'এজ' in words:
                self.chatRead.append("কাঙ্ক্ষিত ব্রাউজারটি চালু\nহচ্ছে")
                webbrowser.open_new(urL)
            else:
                self.chatRead.append("কাঙ্ক্ষিত ব্রাউজারটি \nপাওয়া যায় নি।")


        elif ('hi' in words or 'hello' in words or 'হাই' in words or 'হ্যালো' in words) and len(words) == 1 :
            text = 'হ্যালো বন্ধু, আমি অধীতী।\nবল কিভাবে সাহায্য করতে পারি?'
            self.chatRead.append(text)
        elif 'নাম' in words and 'আমার' in words and 'কি' not in words and 'কি?' not in words:
            for i, word in enumerate( words):

                if word == 'নাম':

                    if int(i) == (len(words) -1):
                        self.user_name = words[i-2]+" "
                    elif words[i+1] != 'আমার':
                        self.user_name = words[i+1]+" "

                    else:
                        self.user_name = words[i+2]+" "
                    break

            self.chatRead.append("হ্যালো, "+self.user_name +"আমি অধীতী।\nবলো কিভাবে সাহায্য করতে পারি?")

        elif 'তোমার' in words and 'নাম' in words:
            self.chatRead.append('হ্যালো, '+self.user_name + "\nআমার নাম অধীতী")

        elif 'আমার' in words and 'নাম' in words and ('কি' in words or 'কি?' in words):
            if self.user_name != "":
                self.chatRead.append('তোমার নাম ' + self.user_name)
            else:
                self.chatRead.append('তোমার নাম জানিনা')

        # elif 'তোমাকে' in words and 'কে' in words and 'তৈরি' in words:
        #     self.chatRead.append('')
        elif 'বাংলাদেশের' in words and 'বিভাগ' in words and 'কয়টি' in words:
            self.chatRead.append('বাংলাদেশের বিভাগ ৮ টি')

        elif 'বাংলাদেশের' in words and 'পূর্ণ' in words and  'নাম' in words:
            text = 'গণপ্রজাতন্ত্রী বাংলাদেশ'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and 'ঋতু' in words and  'কয়টি' in words:
            text = '৬ টি'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('ঋতুর' in words or 'ঋতুগুলোর' in words or 'ঋতুগুলো' in words) :
            text = 'গ্রীষ্ম\nবর্ষা\nশরৎ\nহেমন্ত\nশীত\nবসন্ত'
            self.chatRead.append(text)

        elif 'সর্বোচ্চ' in words and 'চূড়া' in words :
            text ='তাজিংডং\n(১৩১০ মিটার)'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and 'আয়তন' in words :
            text ='১,৪৭,৬১০ বর্গকিলোমিটার.'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('বড়' in words or 'বৃহত্তম' in words) and 'জেলা' in words:
            text ='রাঙ্গামাটি \n(৫৪৬.৪৯ বর্গকিলোমিটার)'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('বড়' in words or 'বৃহত্তম' in words) and 'বিভাগ' in words :
            text ='চট্টগ্রাম \n(৩৩৭৭১ বর্গকিলোমিটার)'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('বড়' in words or 'বৃহত্তম' in words) and 'দ্বীপ' in words :
            text ='ভোলা\n()'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('লম্বা' in words or 'দীর্ঘতম' in words) and 'নদ' in words :
            text ='ব্রহ্মপুত্র\n(২৮৫০ কি.মি)'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('লম্বা' in words or 'দীর্ঘতম' in words) and 'নদী' in words :
            text ='সুরমা\n(৩৯৯ কি.মি.)'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('লম্বা' in words or 'দীর্ঘতম' in words) and 'সমুদ্র' in words and 'সৈকত' in words:
            text ='সুরমা\n(৩৯৯ কি.মি.)'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and 'সর্বমোট' in words and 'গ্রাম' in words:
            text = '৮৭৩১৯ টি'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('ছোট' in words or 'ক্ষুদ্রতম' in words) and 'বিভাগ' in words :
            text ='সিলেট\n(১২৫৯৬ বর্গকিলোমিটার)'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('ছোট' in words or 'ক্ষুদ্রতম' in words) and 'জেলা' in words :
            text ='মেহেরপুর\n(৭১৬ বর্গকিলোমিটার)'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('শ্রেষ্ঠ' in words) and 'চিত্রশিল্পী' in words :
            text ='শিল্পাচার্য জয়নুল আবেদীন'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('শ্রেষ্ঠ' in words) and 'কবি' in words :
            text ='কাজী নজরুল ইসলাম'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('শ্রেষ্ঠ' in words) and 'মহিলা' in words and 'কবি' in words :
            text ='বেগম সুফিয়া কামাল'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('শ্রেষ্ঠ' in words) and 'কার্টুনিস্ট' in words :
            text ='রফিকুন্নবী(রনবী)'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('শ্রেষ্ঠ' in words) and 'বিজ্ঞানী' in words :
            text ='ড. কুদরত-এ-খুদা '
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('শ্রেষ্ঠ' in words) and 'সংগীত' in words and 'সাধক' in words :
            text ='ওস্তাদ আলাউদ্দিন খাঁ'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('শ্রেষ্ঠ' in words) and 'চলচ্চিত্রকর' in words :
            text ='জহির রায়হান'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('প্রথম' in words) and 'রাষ্ট্রপতি' in words :
            text ='শেখ মুজিবুর রহমান'
            self.chatRead.append(text)

        elif 'বাংলাদেশের' in words and ('প্রথম' in words) and 'প্রধানমন্ত্রী' in words :
            text ='তাজউদ্দীন আহমেদ'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('প্রথম' in words) and 'অস্থায়ী' in words and 'রাষ্ট্রপতি' in words :
            text ='সৈয়দ নজরুল ইসলাম'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('প্রথম' in words) and 'পররাষ্ট্রমন্ত্রী' in words:
            text = 'খন্দকার মোশতাক আহমেদ'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('প্রথম' in words) and 'স্পিকার' in words:
            text = 'মোহাম্মদ উল্ল্যাহ'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('প্রথম' in words) and 'বিচারপতি' in words:
            text = 'এ.এস.এম. সায়েম'
            self.chatRead.append(text)
        elif 'বাংলাদেশের' in words and ('প্রথম' in words) and 'গভর্নর' in words:
            text = 'এ.এন. হামিদুল্লাহ'
            self.chatRead.append(text)

        elif ('ঢাকার' in words or 'ঢাকা') and ('প্রথম' in words) and 'মেয়র' in words:
            text = 'মোহাম্মদ হানিফ'
            self.chatRead.append(text)
        elif  ('প্রথম' in words) and 'পতাকা' in words and 'উত্তোলনকারী'in words:
            text = 'আ.স.ম. আবদুর রব'
            self.chatRead.append(text)

        elif ('বাংলাদেশকে') and ('প্রথম' in words) and 'স্বীকৃতি' in words:
            text = 'ভুটান'
            self.chatRead.append(text)

        elif 'জাতির' in words and 'জনক' in words:
            text = 'বঙ্গবন্ধু শেখ মুজিবুর রহমান '
            self.chatRead.append(text)

        elif  ('প্রথম' in words) and 'পতাকা' in words and 'উত্তোলন'in words and 'করা' in words and 'হয়' in words and 'কবে'in words :
            text = '২ মার্চ, ঢাকা বিশ্ববিদ্যালয়'
            self.chatRead.append(text)

        elif  'কয়টি' in words and 'সেক্টর' in words:
            text = '১১ টা'
            self.chatRead.append(text)
        elif 'রাষ্ট্রীয়' in words and 'খেতাব' in words and ('কতজন' in words or 'কয়জন' in words):
            text = '৬৭৭ জন'
            self.chatRead.append(text)
        elif 'বীরশ্রেষ্ঠ' in words:
            text = "বীরশ্রেষ্ঠ ৭ জন\nরুহুল আমিন\nমতিউর রহমান\nহামিদুর রহমান\nসিপাহী মোস্তফা কামাল\nমহিউদ্দিন জাহাঙ্গীর\nমুন্সি আব্দুর রউফ" \
                   "\nনূর মোহাম্মদ শেখ"
            self.chatRead.append(text)
        elif 'বীরউত্তম' in words:
            text = '৬৯ জন'
            self.chatRead.append(text)

        elif 'বীরবিক্রম'in words:
            text = '১৭৫ জন'
            self.chatRead.append(text)
        elif 'স্বাধীন' in words and 'বাংলাদেশের' in words and 'স্থপতি' in words:
            text = 'বঙ্গবন্ধু শেখ মুজিবর রহমান'
            self.chatRead.append(text)
        elif 'স্বাধীনতার'in words and 'ঘোষক' in words:
            text = 'মেজর জেনারেল জিয়াউর রাহমান\nবঙ্গবন্ধু শেখ মুজিবর রহমান এর পক্ষে\n স্বাধীনতার ঘোষণা করেন'
            self.chatRead.append(text)
        elif 'স্বাধীনতা' in words and 'দিবস' in words:
            text = '২৬ শে মার্চ'
            self.chatRead.append(text)

        elif 'বিজয়' in words and 'দিবস' in words:
            text = '১৬ই ডিসেম্বর'
            self.chatRead.append(text)
        elif ('শহীদ' in words or 'মাতৃভাষা' in words) and 'দিবস' in words and 'স্বীকৃতি' not in words :
            text = '২১শে ফেব্রুয়ারি'
            self.chatRead.append(text)
        elif 'শোক' in words and 'দিবস' in words:
            text = '১৫ই আগস্ট'
            self.chatRead.append(text)
        elif 'আন্তর্জাতিক' in words and 'মাতৃভাষা' in words and 'স্বীকৃতি' in words:
            text = 'ইউনেস্কো ১৭ই নভেম্বর\n১৯৯৯ সালে ২১শে ফেব্রুয়ারিকে\nআন্তর্জাতিক মাতৃভাষা দিবস\n হিসেবে স্বীকৃতি দেয়'
            self.chatRead.append(text)
        elif ('স্মৃতিসৌধ' in words or 'স্মৃতিসৌধের' in words) and 'স্থপতি' in words :
            text = 'মইনুল হোসেন'
            self.chatRead.append(text)
        elif 'শহীদ' in words and ('মিনার' in words or 'মিনারের' in words) and 'স্থপতি' in words :
            text = 'হামিদুর রহমান'
            self.chatRead.append(text)

        elif 'স্মৃতিসৌধ' in words and 'উদ্বোধন' in words:
            text = '১৬ ই ডিসেম্বর, ১৯৮২'
            self.chatRead.append(text)

        elif 'শহীদ' in words and 'উদ্বোধন' in words:
            text = '২৩ ফেব্রুয়ারি, ১৯৫২'
            self.chatRead.append(text)

        elif 'বর্তমান' in words and 'প্রধানমন্ত্রী' in words:
            text = 'শেখ হাসিনা'
            self.chatRead.append(text)
        elif 'কততম' in words and 'প্রধানমন্ত্রী' in words:
            text = '১১তম প্রধানমন্ত্রী'
            self.chatRead.append(text)
        elif ('বিরোধীদলের' in words or 'বিরোধীদলীয়') and 'নেতা' in words:
            text = 'হুসেইন মুহাম্মদ এরশাদ'
            self.chatRead.append(text)
        elif 'বর্তমান' in words and 'জনসংখ্যা' in words:
            text = 'ষোল কোটি তেষট্টি লাখ\nআটষট্টি হাজার একশ উনপঞ্চাশ'
            self.chatRead.append(text)

        elif 'জনসংখ্যা' in words and 'বৃদ্ধির' in words:
            text = '১.০ (২০১৭)'
            self.chatRead.append(text)

        elif 'গড়' in words and 'আয়ু' in words:
            text = '৭২.৭০ বছর\nপুরুষ ৭১.১০ বছর\nমহিলা ৭৪.৪০ বছর'
            self.chatRead.append(text)

        elif 'নারী' in words and 'পুরুষ' in words and 'অনুপাত' in words:
            text = '০.৯৭ (পুরুষ/নারী)'
            self.chatRead.append(text)
        elif ('স্বাক্ষরতা' in words or 'স্বাক্ষরতার' in words) and 'হার' in words:
            text = '৭২.৭৬%(২০১৬)'
            self.chatRead.append(text)
        elif ('জন্ম' in words or 'জন্মের' in words) and 'হার' in words:
            text = '১৮.৮০(প্রতি ১০০০ জনে)(২০১৭)'
            self.chatRead.append(text)
        elif ('মৃত্যু' in words or 'মৃত্যুর' in words) and 'হার' in words:
            text = '৫.৪০(প্রতি ১০০০ জনে)(২০১৭)'
            self.chatRead.append(text)
        elif 'কততম' in words and 'জাতীয়' in words and 'নির্বাচন' in words:
            text = '১১ তম'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'ফুল' in words:
            text = 'শাপলা'
            self.chatRead.append(text)

        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'প্রতীক' in words:
            text = 'উভয় পাশে ধানের শীষ \nবেষ্টিত পানিতে ভাসমান শাপলা\nতার মাথায়' \
                   'পাট গাছের \nপরস্পর সংযুক্ত তিনটি পাতা \nএবং উভয় পাশে দুটি\nকরে তারকা।'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'ফল' in words:
            text = 'কাঠাল'
            self.chatRead.append(text)

        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'মাছ' in words:
            text = 'ইলিশ'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'গাছ' in words:
            text = 'বট গাছ'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'পশু' in words:
            text = 'রয়েল বেঙ্গল টাইগার'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'কবি' in words:
            text = 'কাজী নজরুল ইসলাম'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'সংগীত' in words:
            text = 'আমার সোনার বাংলা'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'রণসঙ্গীত' in words:
            text = 'চল চল চল'
            self.chatRead.append(text)
        elif (('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'বন' in words) \
                or 'ম্যানগ্রোভ'in words:
            text = 'সুন্দরবন'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'সংগীতের' in \
                words and 'রচয়িতা' in words:
            text = 'রবীন্দ্রনাথ ঠাকুর'
            self.chatRead.append(text)
        elif ('বাংলাদেশের' in words or ('বাংলাদেশ' in words and 'এর' in words ))and 'জাতীয়' in words and 'রণসংগীতের' in \
                words and 'রচয়িতা' in words:
            text = 'কাজী নজরুল ইসলাম'
            self.chatRead.append(text)
        elif ('বাংলার' in words)and 'বাঘ' in words :
            text = 'শের ই বাংলা এ.কে. ফজলুল হক'
            self.chatRead.append(text)
        else:

            text = ""
            for x in words:
                text+= x+" "
            print(text)
            self.chatRead.append("গুগল এ সার্চ হচ্ছে")
            self.google = window(self)
            self.google.google_search(text[:-1])
            print(text)
            self.google.show()

        self.textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())