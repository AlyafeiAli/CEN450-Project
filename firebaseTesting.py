import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import sleep
import imgbbpy
from imgur import *

# Fetch the service account key JSON file contents
cred = credentials.Certificate("firebase/firebase.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://xxx.firebaseio.com"
})

def send(child, sentence, imgname, keyboard=False):
    # txt = db.reference('parent/child/' + child + "/reports/")
    # txt.push({"text": sentence, "image": imgname})
    db.reference('parent/child/' + child).update({"name": child, "hasKeyboard": keyboard})
    db.reference('parent/child/' + child + '/reports/').push({"text": sentence, "image": imgname})
    print("Sent to DB")

while True:
    child = input("What's the child's name? ")
    txt = input("What to write? ")
    image = input("Image link? ")
    keyboard = input("has keyboard? (n/y) ")
    if keyboard == "n":
        send(child, txt, image)
    elif keyboard == "y":
        send(child, txt, image, True)
    # upload()
    sleep(1)
