import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate("firebase/firebase.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://cen450-test-default-rtdb.firebaseio.com"
})

ref = db.reference('line')
# print(ref.get())

def send(sentence):
    ref.push(sentence)
    print("Sent to DB")
    # print(ref.get())

# ref = db.reference('/line')
# print(ref.get())

# send("Nive!")
# print(ref.get())



# for key, value in ref.get().items():
#     print(value)