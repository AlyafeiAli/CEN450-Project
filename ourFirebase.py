import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from imgur import *
import os

# Fetch the service account key JSON file contents
data = os.path.abspath(os.path.dirname(__file__)) + "/firebase.json"
cred = credentials.Certificate(data)
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://xxx.firebaseio.com/"
})


# print(ref.get())
childpath = os.path.abspath(os.path.dirname(__file__)) + "/childname.txt"
child = open(childpath, "r").readline()

def send(sentence, imgname, keyboard=False):
    # txt = db.reference('parent/child/' + child + "/reports/")
    # txt.push({"text": sentence, "image": imgname})
    db.reference('parent/child/' + child).update({"name": child, "hasKeyboard": keyboard})
    db.reference('parent/child/' + child + '/reports/').push({"text": sentence, "imageURL":imagelink(imgname)})
    print("Sent to DB")
    # print(ref.get())

# ref = db.reference('/line')
# print(ref.get())

# send("Nive!")
# print(ref.get())



# for key, value in ref.get().items():
#     print(value)
