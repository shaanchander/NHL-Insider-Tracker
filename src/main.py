import requests
from functions import *

# insiders' bot ids on mastodon (thanks sportsbots.xyz) - add new ones as desired
insiders = {'eliotteFriedman': '109617175461045229', 'pierreLebrun': '109723560254121614', 'darrenDreger': '109723670700140884', 'chrisJohnston': '109723646153258627', 'frankSeravalli': '109747494700715321'}
# insiders = {'chrisJohnston': '109723646153258627'}

for insider,id in insiders.items():

    posts = getPosts(id, exclude_reblogs=True, exclude_replies=True)

    sendInsiderPost(posts[12])
    # sendMessage('**' + posts[1]['account']['display_name'] + '**:\n' + cleanMessage(posts[1]['content']), images=images, videos=videos)
    # sendMessage(posts[0]['content'] + '\n' + posts[0]['media_attachments'][0]['url'])

    # exit()