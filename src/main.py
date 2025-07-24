import yaml
from functions import *

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
    
insiders = confData['insiders']
discordWebhookUrl = confData['discordWebhookUrl']

for insider in insiders:

    posts = getPosts(insider, exclude_reblogs=confData['excludeBoostedPosts'], exclude_replies=True)

    sendInsiderPost(posts[0], discordWebhookUrl)