import requests, re

def getPosts(id: str, exclude_reblogs:bool=False, exclude_replies:bool=False):
    """Gets posts made by a given user

    Args:
        id (str): user id (in mastodon)
        exclude_reblogs (bool, optional): whether or not to include reblogs (reposts/retweets)
        exclude_replies (bool, optional): whether or not to include replies

    Returns:
        (nothing)

    """
    
    url = f'https://mastodon.social/api/v1/accounts/{id}/statuses?exclude_reblogs={str(exclude_reblogs).lower()}&exclude_replies={str(exclude_replies).lower()}'
    data = requests.get(url).json()

    return data

# def getProfile(id):
#     url = f'https://mastodon.social/api/v1/accounts/{id}'
#     data = requests.get(url).json()

#     return data


def sendMessage(msg:str, webhookUrl:str, username:str='', avatar_url:str='', images:list=[], videos:list=[]):
    """Sends a message to the discord webhook

    Args:
        msg (str): message contents
        username (str, optional): display username to use as message sender (optional)
        avatar_url (str): url of avatar to display in discord (optional)
        images (list): list of image urls to embed in message (optional)
        videos (list): list of video urls to embed in message (optional)

    Returns:
        (nothing)

    """

    data = {
        'content' : msg,
        'embeds': []
    }

    if username:
        data['username'] = username

    if avatar_url:
        data['avatar_url'] = avatar_url

    # add images to webhook data as embeds
    for img in images:
        data['embeds'].append({
            'image': {
                'url': img
            }
        })

    # add videos to webhook data as embeds
    for vid in videos:
        data['embeds'].append({
            'video': {
                'url': img
            }
        })

    print(data)

    result = requests.post(webhookUrl, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f'Payload delivered successfully (code {result.status_code})')

def cleanMessage(post:dict) -> str:
    """Cleans and interprets message contents (including html tags)

    Args:
        msg (str): message contents

    Returns:
        (str) cleaned message

    """

    # thanks to acarters on GitHub for most of this regex cleaning stuff
    regexReplacements = [('</p><p>', '\n\n'), ('<br>', '\n'), ('\\"', '"'), ('&amp', '&'), ('&gt', '>'), ('<(:?[^>]+)>', ''), ('@x.com', ''), ('&nbsp', ''), ('@twitter.com', ''), ('@sportsbots.xyz', '')]

    cleaned = post['content']

    for reg in regexReplacements:
        cleaned = re.sub(reg[0], reg[1], cleaned)

    # fix url if applicable to be complete
    if post['card'] and 'url' in post['card']:
        cleaned = re.sub('\\S*(\\.com|\\.ca|\\.org|\\.net)\\S*(…|\\.\\.\\.)', post['card']['url'], cleaned)

    return cleaned

def sendInsiderPost(post: dict, webhookUrl: str):
    """Sends a formatted mastodon post (json) to the discord webhook

    Args:
        post (arr): insider post to send

    Returns:

    """

    username = ''
    avatarUrl = ''

    workingPost = {}

    # handle boosted (reposted) posts
    if post['reblog'] != None:
        workingPost = post['reblog']
        username = workingPost['account']['display_name'] + f' (via {post['account']['display_name']})'
        avatarUrl = workingPost['account']['avatar']
    else:
        workingPost = post
        username = post['account']['display_name']
        avatarUrl = post['account']['avatar']

    images = []
    videos = []

    for attachment in workingPost['media_attachments']:
        if attachment['type'] == 'image':
            images.append(attachment['url'])

        if attachment['type'] == 'video':
            videos.append(attachment['url'])

    sendMessage(cleanMessage(workingPost), webhookUrl, username=username, avatar_url=avatarUrl, images=images, videos=videos)