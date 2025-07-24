thanks to @acarters for the regex cleanup stuff

## Adding new insiders
1. Go to their profile on mastodon (mirrored by sportsbots.xyz)
2. Open the network inspector and refesh the page
3. Look for a url similar to "https://mastodon.world/api/v1/accounts/[ACCOUNT_ID]"
4. Add that account id to config.yaml (optionally comment their name next to it for reference later)

## TODO / Current limitations
- Assumes boosts are never of boosted posts (assumes a regular post is boosted or just a regular post)