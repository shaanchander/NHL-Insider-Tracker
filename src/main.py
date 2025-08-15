import yaml
from functions import *
from datetime import datetime, timezone
import os

def main():

    projDir = os.path.dirname(__file__)
    requiredOptions = [('insiders', 'list'), ('discordWebhookUrl', 'string'), ('excludeBoostedPosts', 'boolean')]
    dateTimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'

    confData= {}

    with open(projDir + '/../conf.yaml', 'r') as file:
        confData = yaml.safe_load(file)

    for opt in requiredOptions:
        if opt[0] not in confData:
            print("YAML doesn't include all config options. They should include the below options:\n")

            for option in requiredOptions:
                print(f'{option[0]} ({option[1]})')

            exit()

    lastSend = ""
    if os.path.exists(projDir + '/../lastSend.txt'):
        with open(projDir + '/../lastSend.txt', 'r') as file:
            lastSend = datetime.strptime(file.readline(), dateTimeFormat)
    else:
        lastSend = datetime.now(timezone.utc)
        print('lastSend.txt not found - initializing new one with current time')

        with open(projDir + '/../lastSend.txt', 'w') as file:
            file.write(datetime.now(timezone.utc).strftime(dateTimeFormat))

        exit()
        
    insiders = confData['insiders']
    discordWebhookUrl = confData['discordWebhookUrl']

    postsToSend = []

    for insider in insiders:

        posts = getPosts(insider, exclude_reblogs=confData['excludeBoostedPosts'], exclude_replies=True)

        for post in posts:
            if datetime.strptime(post['created_at'], dateTimeFormat) > lastSend:
                print(f"{post['created_at']} > {lastSend}")
                postsToSend.append(post)

    postsToSend = sorted(postsToSend, key = lambda x:datetime.strptime(x['created_at'], dateTimeFormat))

    for post in postsToSend:
        sendInsiderPost(post, discordWebhookUrl)

    with open(projDir + '/../lastSend.txt', 'w') as file:
        file.write(datetime.now(timezone.utc).strftime(dateTimeFormat))

if __name__ == "__main__":
    main()