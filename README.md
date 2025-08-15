# NHL-Insider-Tracker
Python program to relay specified NHL insiders' tweets to a Discord server using a webhook allowing for instant notifications and chronological scrolling of past posts.

## Background

As an avid hockey fan who wants to keep up with all the news while also not wanting to use X/Twitter, there aren't many great options. With most insiders posting exclsuively to X/Twitter, it's harder to keep up to date while not being on the platform. 

One great option previously was Icebreaker/Tradebreaker, it essentially mirrored NHL insiders from Twitter to a mobile app and sent push notifications as well. Unfortunately, due to Twitter's new API limitations, [it was forced to be shut down](https://mattjennings.io/blog/tradebreaker-is-shutting-down).

This program aims to achieve similar functionality, though instead relying on the mirror of the accounts from Twitter to Mastodon by sportsbots.xyz (huge thanks to them) and using Discord webhooks as a free way to send push notifications, and offer a chronological view of tweets to scroll through. 

## Usage

### Initial Setup
1. Create a new Discord server and channel to be where notifications are sent
2. Generate a webhook url for the server and connect it to that channel you just created
3. Replace the discordWebhookUrl at the top of conf.yaml.sample with the one you just generated
4. Rename file from conf.yaml.sample to conf.yaml (remove the .sample extension)

### Configuring periodic checks
The program keeps track internally of when it last ran to prevent repeat notifications, so it can be run on whatever interval you'd like with something like a cronjob running the script. 

For example, adding the following to your crontab file will run the program every 10 minutes:

```
*/10 * * * * python3 /path/to/project/folder/src/main.py
```

As usual, [Crontab Guru](https://crontab.guru) is your friend for helping you make a cron expression that does what you'd like.

**Note: the first run is used for initialization of last sent time so nothing will be sent on the first run**

### Adding new insiders

The project was created to be used for NHL insiders and includes a few prominent ones, but any account should work

1. Go to their profile on Mastodon (sports insiders mirrored by sportsbots.xyz)
2. Open the network inspector and refesh the page
3. Look for a url similar to https://mastodon.world/api/v1/accounts/[ACCOUNT_ID] or https://mastodon.social/redirect/accounts/[ACCOUNT_ID]
4. Add that account id to config.yaml (optionally comment their name next to it for reference later)

## TODO / Current limitations
- Assumes boosts are never of boosted posts (assumes a regular post is boosted or just a regular post)
- Make insiders be added by url instead of id for simplicity
- Error trap conf.yaml properly

## Thanks to
- [acarters](https://github.com/acarters) - for the regex cleanup stuff to parse the stylized bodies from Mastodon
- [sportsbots.xyz](https://www.sportsbots.xyz/) - for mirroring the accounts from X/Twitter to Mastodon (please support them [here](https://www.buymeacoffee.com/sportsbots) if you can)