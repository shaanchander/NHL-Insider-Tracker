import yaml
from functions import *
from datetime import datetime
import os

requiredOptions = [('insiders', 'list'), ('discordWebhookUrl', 'string'), ('excludeBoostedPosts', 'boolean')]

confData= {}

with open('../conf.yaml', 'r') as file:
    confData = yaml.safe_load(file)

for opt in requiredOptions:
    if opt[0] not in confData:
        print("YAML doesn't include all config options. They should include the below options:\n")

        for option in requiredOptions:
            print(f'{option[0]} ({option[1]})')

        exit()

lastSend = ""
if os.path.exists('../lastSend.txt'):
    with open('../lastSend.txt', 'r') as file:
        lastSend = file.readline()
else:
    lastSend = str(datetime.now())
    print('lastSend.txt not found - initializing new one with current time')

    with open('../lastSend.txt', 'w') as file:
        file.write(str(datetime.now()))

    exit()
    
insiders = confData['insiders']
discordWebhookUrl = confData['discordWebhookUrl']

postsToSend = []

for insider in insiders:

    posts = getPosts(insider, exclude_reblogs=confData['excludeBoostedPosts'], exclude_replies=True)

    for post in posts:
        if post['created_at'] > lastSend:
            postsToSend.append(post)

    # sendInsiderPost(posts[0], discordWebhookUrl)

postsToSend = sorted(postsToSend, key = lambda x:datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'))

for post in postsToSend:
    # print(post['account']['username'])
    sendInsiderPost(post, discordWebhookUrl)

with open('../lastSend.txt', 'w') as file:
    file.write(str(datetime.now()))