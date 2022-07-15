import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import sleep
from ourFirebase import *

# Fetch the service account key JSON file contents
data = os.path.abspath(os.path.dirname(__file__)) + "/firebase.json"
cred = credentials.Certificate(data)
# Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://xxx.firebaseio.com"
# })

def blacklist(line):
    words = db.reference("parent/Blacklist/").get()
    blacklist = words.get('words').split(",") #Blacklist -> if any in blacklist then ...
    lineList = line.split()
    return any(x in blacklist for x in lineList)
