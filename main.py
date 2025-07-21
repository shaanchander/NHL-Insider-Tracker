import requests

friedmanUrl = 'https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=did%3Aplc%3Asdobrsxnvwczrjydmnubhibh&filter=posts_and_author_threads&includePins=true&limit=30'

data = requests.get(friedmanUrl).json()

print(data['feed'][0]['post']['record']['text'])