import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./pteracup-firebase-adminsdk-5r6k8-ed8304a9d2.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pteracup-default-rtdb.firebaseio.com',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

##databaseに初期データを追加する
users_ref = db.reference('/users')

users_ref.set({
    'user001': {
        'user_id': '1',
        'name': 'unkonow'
        },
    'user002': {
        'user_id': '2',
        'name': 'tosabaka'
        }
    })

# databaseにデータを追加する
users_ref.child('user003').set({
      'user_id': '3',
      'name': 'ute'
    })

##データを取得する
print(users_ref.get())