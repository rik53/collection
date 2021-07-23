from pymongo import MongoClient
MONGO_HOST = "localhost"
MONG0_PORT = 27017
MONGO_DB = "social_network"
MONGO_followers = "followers_insta"
MONGO_subscriptions = "subscriptions_insta"
with MongoClient(MONGO_HOST, MONG0_PORT) as client:
    db = client[MONGO_DB]
    follower = db[MONGO_followers]
    subscription=db[MONGO_subscriptions]

username = input('Введите username: ')
profiles = input('Введите profiles: ')
followers = follower.find({"username": username})
subscriptions = subscription.find({"username": profiles,})
for i in followers :
    print(i)
for j in subscriptions :
    print(j)