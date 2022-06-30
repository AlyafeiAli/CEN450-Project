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

child = input("What's the child's name? ")
txt = db.reference('parent/child/'+child+"/reports/")
# print(ref.get())

def send(sentence):
    txt.push({"text":sentence, "image":imagelink('test')})
    print("Sent to DB")

while True:
    send(input("What to write? "))
    # upload()
    sleep(1)