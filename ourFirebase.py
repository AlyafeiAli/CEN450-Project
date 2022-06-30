import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from imgur import *

# Fetch the service account key JSON file contents
cred = credentials.Certificate("firebase/firebase.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://xxx.firebaseio.com"
})


# print(ref.get())

def send(child, sentence, imgname):
    txt = db.reference('parent/child/'+child+"/reports/")
    txt.push({"text":sentence, "image":imagelink(imgname)})
    print("Sent to DB")
    # print(ref.get())

# ref = db.reference('/line')
# print(ref.get())

# send("Nive!")
# print(ref.get())



# for key, value in ref.get().items():
#     print(value)