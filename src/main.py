import yaml
from functions import *

confData= {}

with open('../conf.yaml', 'r') as file:
    confData = yaml.safe_load(file)

if 'insiders' not in confData or 'discordWebhookUrl' not in confData:
    print("YAML doesn't include 'insiders' field and 'discordWebhookUrl'")
    exit()
    
insiders = confData['insiders']
discordWebhookUrl = confData['discordWebhookUrl']

for insider in insiders:

    posts = getPosts(insider, exclude_reblogs=True, exclude_replies=True)

    sendInsiderPost(posts[13], discordWebhookUrl)