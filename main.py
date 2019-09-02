import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow
import random
import json
import pickle
import os.path  # to check if the file already exist
import glob
import speech as voice
import weather
from termcolor import colored
import os
import pyttsx3
import requests
import datetime
import calendar
import matplotlib as plt


#  Variables #
training = []
output = []
retrain_Var = True  # To force train the model (Set to False by Default)
global history
##################### Functions

# Main functions
def AI_Brain(s, words):  # The brain processing the responses
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

def chat():
    print("Start typing to Theo (type 'quit') to stop. To use voice detection type 'voice detection'")
    voice_detection = False
    search_active = False
    weather_active = False
    while True:
        if(voice_detection and check_internet()):  # Voice Input
            print(colored("You are now using voice detection. Say 'Stop Detecting' to deactivate", "blue"))
            while True:
                voiceInput = voice.speechMain()
                if(voiceInput is not None): # prevents the model to not interpret "None" from voiceInput
                    print("You: ", colored(voiceInput, "green"))
                    results = model.predict([AI_Brain(voiceInput, words)])[0]
                    results_index = np.argmax(results)
                    tag = labels[results_index]
                    confidence = results[results_index] * 100
                    if (("search for" in voiceInput) or ("make a search for" in voiceInput)):
                        if (confidence > 80):
                            search_active = True
                            make_search(voiceInput)
                    if (tag == "Asking_about_the_time"):
                        if (confidence > 80):
                            hour, minute, second = get_time()
                            print(hour, ":", minute, ":", second)
                            speak.say(
                                "The time is " + str(hour) + " " + str(minute) + " and " + str(second) + " seconds")

                    if (tag == "Doing_math"):
                        if (confidence > 80):
                            equation = do_math_parse(inp.lower())
                            result = do_math((inp.lower()))
                            print(result)
                            speak.say("The answer to " + str(equation) + " is " + str(result))

                    if (tag == "Asking_about_the_date"):
                        if (confidence > 80):
                            month, day, year = get_date()
                            print("Month: ", month, " Day: ", day, " Year: ", year)
                            speak.say("The date is " + str(month) + " " + str(day) + " " + str(year))
                    if (tag == "Asking_about_the_weather"):
                        if (confidence > 80):
                            try:
                                weather_active = True
                                weather_info, city = weatherParse(voiceInput)
                                gathered_weather_info = weather.get_weather(weather_info, city)
                            except:
                                weather_active = False
                                print("Sorry, I couldn't get the weather information there")
                                speak.say("Sorry, I couldn't get the weather information there")

                    if (retrain_Var == False):  # So it doesn't break when retraining
                        if (confidence > 80):
                            for tg in data["intents"]:
                                if tg['tag'] == tag:
                                    responses = tg['responses']
                            response = random.choice(responses)
                            print("Tag: ",tag," Confidence: ",confidence,"%") # Debug
                            if (search_active):
                                print(response, searchingParse(voiceInput))
                            elif (weather_active):
                                print("In " + city + "," + gathered_weather_info)
                            else:
                                print(response)
                            speak = pyttsx3.init()
                            if (search_active):  # Make it seem more user friendly
                                speak.say(response + searchingParse(voiceInput))
                                search_active = False
                            elif (weather_active):
                                speak.say("In " + city + "," + gathered_weather_info)
                                weather_active = False
                            else:
                                speak.say(response)
                            speak.runAndWait()
                        else:
                            sorry = "Sorry I didn't get that. Could you try typing or saying it in another way?"
                            print("Sorry I didn't get that. Could you try typing or saying it in another way?")
                            lowConfidenceInput(voiceInput)
                            speak = pyttsx3.init()
                            speak.say(sorry)
                            speak.runAndWait()
                            # print(tag) # Debugging
                    if ((voiceInput == "stop detecting") or (voiceInput == "stop listening")):
                        voice_detection = False
                        results = model.predict([AI_Brain(voiceInput, words)])[0]
                        results_index = np.argmax(results)
                        tag = labels[results_index]
                        if results[results_index] > 0.7:
                            for tg in data["intents"]:
                                if tg['tag'] == tag:
                                    responses = tg['responses']
                            response = random.choice(responses)
                            print(response)
                            speak = pyttsx3.init()
                            speak.say(response)
                            speak.runAndWait()
                        else:
                            sorry = "Sorry I didn't get that. Could you try typing or saying it in another way?"
                            print("Sorry I didn't get that. Could you try typing or saying it in another way?")
                            lowConfidenceInput(voiceInput)
                            speak = pyttsx3.init()
                            speak.say(sorry)
                            speak.runAndWait()
                            # print(tag) # Debugging
                        print(colored("You are now using typed input. To use voice detection type 'voice detection'", "blue"))
                        break

                    if(voiceInput == "quit"):
                        exit()
                    '''
                    if(voiceInput == "retrain"):
                        retrain_Var = True
                        retrain_Model_Check(retrain_Var)
                    '''



        if(not voice_detection):  # Typed Input
            inp = input("You: ")
            internet_check = check_internet()

            results = model.predict([AI_Brain(inp, words)])[0]
            results_index = np.argmax(results)
            tag = labels[results_index]
            confidence = results[results_index]*100
            speak = pyttsx3.init()
            if inp.lower() == "quit":
                quit()
            '''
            if(inp.lower() == "retrain"):
                retrain_Var = True
                retrain_Model_Check(retrain_Var)
                print("HI")
            '''
            if (tag == "Making_a_Search"):
                if(confidence > 80):
                    search_active = True
                    make_search(inp.lower())
            if (tag == "Asking_about_the_time"):
                if(confidence > 80):
                    hour, minute, second = get_time()
                    print(hour, ":", minute, ":", second)
                    speak.say("The time is " + str(hour) + " " + str(minute) + " and " + str(second) + " seconds")

            if (tag == "Asking_about_the_date"):
                if(confidence > 80):
                    month, day, year = get_date()
                    print("Month: ", month, " Day: ", day, " Year: ", year)
                    speak.say("The date is " + str(month) + " " + str(day) + " " + str(year))
            if (tag == "Doing_math"):
                if(confidence > 80):
                    equation = do_math_parse(inp.lower())
                    result = do_math((inp.lower()))
                    print(result)
                    speak.say("The answer to " + str(equation) + " is " + str(result))
            if(tag == "Asking_about_the_weather"):
                if(confidence > 80):
                    try:
                        weather_active = True
                        weather_info, city = weatherParse(inp.lower())
                        gathered_weather_info = weather.get_weather(weather_info, city)
                    except:
                        weather_active = False
                        print("Sorry, I couldn't get the weather information there")
                        speak.say("Sorry, I couldn't get the weather information there")

            if ((tag == "Voice_Detection_Activate") and (internet_check)):
                voice_detection = True
            elif(tag == "voice detection"):
                print(colored("There is no internet connection", "red"))

            if(retrain_Var == False):  # So it doesn't break when retraining
                if results[results_index] > 0.7:
                    for tg in data["intents"]:
                        if tg['tag'] == tag:
                            responses = tg['responses']
                    response = random.choice(responses)
                    print("Tag: ",tag," Confidence: ",confidence,"%") # Debug
                    if (search_active):
                        print(response,searchingParse(inp.lower()))
                    elif(weather_active):
                        print("In " + city.capitalize() + "," + str(gathered_weather_info))
                    else:
                        print(response)
                    speak = pyttsx3.init()
                    if(search_active):  # Make it seem more user friendly
                        speak.say(response+searchingParse(inp.lower()))
                        search_active = False
                    elif(weather_active):
                        speak.say("In " + city + "," + gathered_weather_info)
                        weather_active = False
                    else:
                        speak.say(response)
                    speak.runAndWait()
                else:
                    sorry = "Sorry I didn't get that. Could you try typing or saying it in another way?"
                    print("Sorry I didn't get that. Could you try typing or saying it in another way?")
                    lowConfidenceInput(inp)
                    speak = pyttsx3.init()
                    speak.say(sorry)
                    speak.runAndWait()
                    # print(tag) # Debugging

def train():
    words_train = []
    labels_train = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:  # uses stemming to get to the root of the word so accurately train the bot
            wrds = nltk.word_tokenize(pattern)
            words_train.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            if intent["tag"] not in labels_train:
                labels_train.append(intent["tag"])

    words_train = [stemmer.stem(w.lower()) for w in words_train if w != "?"]
    words_train = sorted(list(set(words_train)))

    labels_train = sorted(labels_train)

    training_brain = []
    output = []

    out_empty = [0 for _ in range(len(labels_train))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words_train:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels_train.index(docs_y[x])] = 1

        training_brain.append(bag)
        output.append(output_row)

    training_brain = np.array(training_brain)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words_train, labels_train, training_brain, output), f)

def AI_model():
    #    AI Model  #########
    tensorflow.reset_default_graph()
    global net
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 10)  # have a hidden layer with 8 neurons might have to add more neurons ( or layers which ever one) if I add more intents to the json file and build this bot further
    net = tflearn.fully_connected(net, 10)
    net = tflearn.fully_connected(net, 10)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    global model
    model = tflearn.DNN(net)

    # model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    # model.save("model.tflearn")

    if (glob.glob("model.tflearn.*")):  # this works some how, don't know how =)
        if (os.path.exists(glob.glob("model.tflearn.*")[0])):
            model.load("model.tflearn")
        else:
            history = model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)  # history is never used
            model.save("model.tflearn")

    else:
        history = model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True) # history is never used
        model.save("model.tflearn")

def jsonCheck():
    global data
    global data_original
    if (glob.glob("intents.json") and glob.glob("intents_original.json")):
        if (os.path.exists(glob.glob("intents.json")[0]) and os.path.exists(glob.glob("intents_original.json")[0])):
            with open("intents.json") as file:
                data = json.load(file)
            with open("intents_original.json") as file:
                data_original = json.load(file)
        elif (os.path.exists(glob.glob("intents.json")[0]) and not os.path.exists(glob.glob("intents_original.json")[0])):
            with open("intents.json") as file:
                data = json.load(file)

            intents_original = open("intents_original.json", "a+")  # to save it as an original file to compare later
            intents_original.write(json.dumps(data, indent=1))
            intents_original.close()

            with open("intents_original.json") as file:
                data_original = json.load(file)
    elif (not (glob.glob("intents_original.json"))):
        with open("intents.json") as file:
            data = json.load(file)
        intents_original = open("intents_original.json", "a+")  # to save it as an original file to compare later
        intents_original.write(json.dumps(data, indent=1))
        intents_original.close()
        with open("intents_original.json") as file:
            data_original = json.load(file)



# Internet Functions
def check_internet():  # To check if you have a internet connection to connect to the Google API
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def searchingParse(user_input): # Parse the user intent from the search command
    parse_list = ["search for ", "make a search for "]  # connect this to the json file later
    parsed = user_input
    first_index = 1
    parse_out = ""
    for i in range(len(parse_list)):
        if (parse_list[i] in parsed):
            parse_out = parse_list[i]
    if(parse_out != ""):
        for phrase in range(1):
            #print("Before Parse: ", parsed)  # Debug
            parsed = parsed.replace(parse_out, "", first_index)
            #print("Remaining list: ", parsed)  # Debug

    return parsed

def searchingOnline(searchQuery):  # Uses google chrome by default, searchQuery is the parsed intent from searching Parse
    googleUrl = "https://google.com/search?q="
    url = 'http://google.com'
    searchQuery = searchQuery.replace(" ", "+")  # converts it into one search query
    os.system("Start Chrome.exe {}".format(googleUrl+searchQuery))  # this works

def make_search(user_search):  # puts together the online searching function (Call this)
    query = searchingParse(user_search)
    searchingOnline(query)



# Weather function
def weatherParse(user_input):
    parse_list = ["what is the ", "give me the "]  # connect this to the json file later
    weather_info_list = ["weather", "temperature", "max temperature", "min temperature", "humidity", "wind speed", "wind direction", "pressure"]
    parsed = user_input
    first_index = 1
    parse_out = ""
    weather_info = ""
    city_name = ""
    for i in range(len(parse_list)):
        if (parse_list[i] in parsed):
            parse_out = parse_list[i]
    if (parse_out != ""):
        for phrase in range(1):
            # print("Before Parse: ", parsed)  # Debug
            parsed = parsed.replace(parse_out, "", first_index)
            # print("Remaining list: ", parsed)  # Debug

        for assign in range(len(weather_info_list)):  # assign the correct weather info
            if (weather_info_list[assign] in parsed):
                weather_info = weather_info_list[assign]

        for info_takeout in range(1):  # first step to get the city
            # print("Before Parse: ", parsed)  # Debug
            parsed = parsed.replace(weather_info, "", first_index)
            # print("Remaining list: ", parsed)  # Debug

        for info_takeout in range(1):  # second step to get the city
            # print("Before Parse: ", parsed)  # Debug
            parsed = parsed.replace(" in ", "", first_index)
            # print("Remaining list: ", parsed)  # Debug
        city_name = parsed
    return weather_info,city_name


# Retrain model function
def retrain_Model_Check(retrain):
    if ((data != data_original) and retrain == False):
        response = input("The intents file has been changed. Would you like to retrain the model? y/n ")
        if (response == 'y'):
            if (glob.glob("data.pickle")):
                os.remove("data.pickle")
            if (glob.glob("checkpoint")):
                os.remove("checkpoint")
            if (glob.glob("intents_original.json")):
                os.remove("intents_original.json")
            if (glob.glob("model.*")):
                size = glob.glob("model.*")
                for file in range(len(size)):
                    os.remove(size[file])
            jsonCheck()
            try:  # force this try to skip if the intent.json file is altered so it retrains
                with open("data.pickle", "rb") as f:
                    words, labels, training, output = pickle.load(f)
            except:  # same thing as null pointer in C# & Java
                train()
    elif(retrain == True):
        response = input(colored("Are you sure you would like to retrain the model? y/n ", "red"))
        if (response == 'y'):
            if (glob.glob("data.pickle")):
                os.remove("data.pickle")
            if (glob.glob("checkpoint")):
                os.remove("checkpoint")
            if (glob.glob("intents_original.json")):
                os.remove("intents_original.json")
            if (glob.glob("model.*")):
                size = glob.glob("model.*")
                for file in range(len(size)):
                    os.remove(size[file])
            jsonCheck()
            try:  # force this try to skip if the intent.json file is altered so it retrains
                with open("data.pickle", "rb") as f:
                    words, labels, training, output = pickle.load(f)
            except:  # same thing as null pointer in C# & Java
                train()



# Date and time functions
def get_time():
    currentDT = datetime.datetime.now()
    hour = currentDT.hour % 12
    if(currentDT.minute < 10):
        currentDT.minute = "0" + currentDT.minute
    minute = currentDT.minute
    return hour,minute,currentDT.second

def get_date():
    currentDT = datetime.datetime.now()
    month = currentDT.month
    day = currentDT.day
    year  = currentDT.year
    return month, day, year



# Math functions
def do_math_parse(math_input):
    parse_list = ["what is ", "tell me ", "what's ", "hey avis, what's ", "hey avis, what is "]  # connect this to the json file later
    parsed = math_input
    first_index = 1
    parse_out = ""
    for i in range(len(parse_list)):
        if (parse_list[i] in parsed):
            parse_out = parse_list[i]
    if (parse_out != ""):
        for phrase in range(1):
            # print("Before Parse: ", parsed)  # Debug
            parsed = parsed.replace(parse_out, "", first_index)
            # print("Remaining list: ", parsed)  # Debug
    #parsed = parsed.split()


    return parsed

def do_math(input):
    result = do_math_parse(input)
    return round(eval(result))



#Low Confidence input

def make_Learn_Doc():
    LearningDoc = open("LearningDoc.json", "a+")
    LearningDoc.write(json.dumps("Hello", indent=1))
    LearningDoc.close()

def learnDocFormat(intentList): # Have it be able to append to an already existing tag in the correct spot.
    format = {
   "intents": intentList
  }
    return format

def lowConfidenceInput(input):
    lowConfidenceDoc = open("lowConfidenceInput.json", "a+")
    lowConfidenceDoc.write('\n')
    lowConfidenceDoc.write(json.dumps(input, indent=1))
    lowConfidenceDoc.close()

def increaseConfidence(): # useful retrain function (needs to delete already implemented phrases from the lowConfidenceInput.json) and also need to add when there is a new tag being made
    with open("lowConfidenceInput.json") as file:
        lowConfidenceData = json.load(file)
    for phrase in lowConfidenceData:
        print("Enter tag for "+"'"+phrase+"'")
        tag = input("tag: ")
        print(lowConfidenceData)
        print(data["intents"])
        dataTemp = data["intents"] # stores the whole intents file into this variable
        #print(dataTemp) # Debug
        for tags in data["intents"]: #checking if a the tag already exists
            index = dataTemp.index(tags) # get the index of the tag
            print("The index is: ", index)
            if tags["tag"] == tag:
                print("It is: ", dataTemp[index]) # Debug
                print("yaaayy") # append the new phrase here # Debug
                tags["patterens"] = tags["patterns"].append(phrase)
                print(tags["patterns"]) # make it properly append to the right spot in the intents.json file , might have to store the file in a variable and then append and then reformat it at the en
                print("\n")
                print("Here: ", dataTemp[index]["patterns"])
                intents = open("intents.json", "w")  # to save it as an original file to compare later
                intents.write(json.dumps(learnDocFormat(dataTemp), indent=1))
                intents.close()
            else:
                print("nope")


        # Code to auto format a brand new tag



        #print(learnDocFormat(tag, phrase))
##############################################################################################
#### ON Startup ######
jsonCheck()
retrain_Model_Check(retrain_Var)
retrain_Var = False  # So it doesn't cause an error of not responding back

try:
    AI_model()
except:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
    AI_model()



##########################

########## Run ########
#chat()
#make_Learn_Doc()
#print(learnDocFormat("blob"))
increaseConfidence()

#subprocess.Popen("C:\Program Files (x86)\Steam\Steam.exe")  # work on this later
