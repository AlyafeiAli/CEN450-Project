import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import sleep
from firebaseUpdate import *

# Fetch the service account key JSON file contents
cred = credentials.Certificate("firebase/firebase.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://cen450-test-default-rtdb.firebaseio.com"
})

def blacklist(line):
    word = db.reference("parent/blacklist/").get()
    blacklist = word.get('word').split(",") #Blacklist -> if any in blacklist then ...
    lineList = line.split()
    return any(x in blacklist for x in lineList)


# blacklist()

