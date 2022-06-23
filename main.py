import pyautogui  # https://github.com/asweigart/PyGetWindow/issues/26#issuecomment-945001903
import os
from tesse2 import *
from time import sleep
from PIL import ImageGrab
from datetime import datetime
import shutil
import pygetwindow as gw
import pytesseract
import numpy as np
import math
import re
import pandas as pd
from bs4 import BeautifulSoup
import random
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
import bert
import sys
from glob import glob

keywords = {"not-so-nice-words"}  # set, to avoid duplicates - fallback in case of a false negative
titleList = ['chrome', 'teams']  # Social media list
path = glob("tokenzier/*") #Because the tf model will be saved in a random subdirectory inside "tf/".
print("initializing")
os.environ["TFHUB_CACHE_DIR"] = "tokenzier/"  # Set tf model download path
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Filter out INFO & WARNING messages
FullTokenizer = bert.bert_tokenization.FullTokenizer  #This is where it takes long time
bert_layer = hub.KerasLayer(path[0], trainable=False) if os.path.isdir("tokenzier") else hub.KerasLayer(
    "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4", trainable=False) #Don't download again after initial setup
vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()  # Have access to vocab file for tokenizer
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = FullTokenizer(vocab_file, do_lower_case)
cwd = os.getcwd()
print("Ready.")


def encode_sentence(sent):
    return tokenizer.convert_tokens_to_ids(tokenizer.tokenize(sent))


def get_prediction(sentence):
    tokens = encode_sentence(sentence)
    inputs = tf.expand_dims(tokens, 0)
    model = tf.saved_model.load('model/')
    output = model(inputs, training=False)
    sentiment = math.floor(output * 2)
    if output < 0.7:
        # print("Output of the model: {}\nPredicted: NOT Toxic".format(output))
        return False

    elif output >= 0.7:
        # print("Output of the model: {}\nPredicted: TOXIC".format(output))
        return True


def supreme(interval):  # Create the directory, then call the screenshot/transcript process based on the interval.
    # Default number of times should be 86400, which is the number of seconds in a day.
    try:
        os.mkdir("process")
    except OSError as error:
        pass
    counter = 0
    for x in range(5):  # number of iterations to make before erasing everything (Idea: set to purge every 24 hours)
        counter += 1
        sleep(interval)
        process() if counter <= 4 else begin(interval)


def process():  # Take screenshots and transcript.

    # ADD condition: AND not minimzed (or isFocused is better)
    # I mean for gw.getWindowswithTitle() or gw.getAllTitles()
    # If whatsapp in gw.getAllTitles() and is not minimzed (Or and is focused()): Start taking screenshots and yada yada

    # im = ImageGrab.grab()
    # dt = datetime.now()
    # fname = "process/screenshot-{}.jpeg".format(dt.strftime('%Y%m%d-%H%M%S'))
    # im.save(fname, 'jpeg')
    # print(pytesseract.image_to_string(Image.open(fname)))

    # IDEA for taking cropped screenshots:
    # while True: #https://stackoverflow.com/a/68253392/19324525
    #     cars = gw.getWindowsWithTitle('Chrome')[0] #Any string in the title will do
    #     img = ImageGrab.grab(bbox=(int(cars.left),
    #                                int(cars.top),
    #                                int(cars.left + cars.width),
    #                                int(cars.top + cars.height)))

    titles = gw.getAllTitles()
    print(titles)
    titles_lower = [each_string.lower() for each_string in titles]  # lowercase all titles
    print(titles_lower)

    for check in titleList:  # https://bit.ly/3xojAvH
        title = any(check in string for string in titles_lower)
        # print(title)
        if title:
            title = [string for string in titles_lower if check in string]
            break

    if len(title) != 0:
        # print(title)
        window = gw.getWindowsWithTitle(title[0])[0]  # Any string in the title will do

    active_window = False

    try:
        active_window = window.isActive
    except Exception as e:
        print("Window not found")

    if active_window:
        img = ImageGrab.grab(bbox=(int(window.left),
                                   int(window.top),
                                   int(window.left + window.width),
                                   int(window.top + window.height)))
        dt = datetime.now()
        formated_datetime = dt.strftime('%Y%m%d_%H-%M-%S')
        name = "./process/screenshot-{}.png".format(formated_datetime)
        img.save(name, 'png')
        ocr(name, formated_datetime)

        #Get lines from text file
        txt = "./process/"
        txt += formated_datetime
        ext = '.txt'
        txt += ext
        file = open(txt, "r")
        Lines = file.readlines()
        for line in Lines:
            line2 = line.strip() + " o o o o o o o o"
            # print("with strip: ", line)
            # print("without strip: ", line.strip())
            if get_prediction(line2.strip()):  # Toxic
                # Inside get prediction, do for each line (Done already in one of the files)
                print('Toxic line: ', line.strip())
                print("")
            else:
                print("Safe line: ", line.strip())
                print("")

        print('Done taking screenshot and OCRing')
    else:
        print("No chat app found")


def begin(f):  # Delete the files after 24 hours have passed, then call supreme again.

    shutil.rmtree('process',
                  ignore_errors=True)  # Delete everything inside the folder, ignore errors in cases like it doesn't exist
    supreme(f)

    # # Overwrite the Files if they exist
    # directory = "./process"
    # files_in_directory = os.listdir(directory)
    # filtered_files = [file for file in files_in_directory if file.endswith(".txt") or file.endswith(".jpeg")]
    # try:
    #     for file in filtered_files:
    #         path_to_file = os.path.join(directory, file)
    #         os.remove(path_to_file)
    # except OSError as e:
    #     # Already Empty
    #     pass


def keyword(frequency):  #Idea: Change it monitor other sites. Also, make it right to a file so that it doesn't ask in each run.
    global keywords
    approve = ["Yes", "yes", "Y", "y"]
    deny = ["No", "no", "N", "n"]

    while True:
        ask = input("Do you want to blacklist certain keywords? (Yes or No) ")
        if ask in approve:
            while True:
                word = input("Please enter the word you want to blacklist (Type 'stop' when you're done)").lower()
                if word == "stop":
                    break
                else:
                    keywords.add(word)
            begin(frequency)
            break
        elif ask in deny:
            begin(frequency)
            break
        else:
            print("Please answer with Yes or No.")

        # try:
        #     freq = int(input("How Frequently Should we Take Screenshots? (In Seconds) "))
        # except ValueError:
        #     print("Please enter a valid number.")
        #     continue
        #
        # if freq <= 0:
        #     print("Sorry, your response must not be a zero or a negative.")
        #     continue
        # else:
        #     begin()
        #     break


def freq():
    while True:
        try:
            freq = int(input("How Frequently Should we Take Screenshots? (In Seconds) ")) #No real benifit.. delete it ya 3mie
        except ValueError:
            print("Please enter a valid number.")
            continue

        if freq <= 0:
            print("Sorry, your response must not be a zero or a negative.")
            continue
        else:
            keyword(freq)
            break

freq()
