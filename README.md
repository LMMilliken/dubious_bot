# dubious_bot

# PARTS:

## Scraper

The component for retrieving posts from a given user, currently just facebook.

### Currently

Given an html file of a user, can extract all 'post's from the file, and return them as a list. Unfortunately this includes the posts of other users that SUBJECT has liked or quote tweeted or whatever.

### TODO for Scraper:
- Distinguish between user posts and shared posts
- Get correct post count
  - scrolling shenanigans
- twitter? maybe?

### Blocked

chrome driver isnt working, so currently just reading and scraping local files

## Brain

The part that constructs prompts for gpt-3 and gets responses.
Can currently generate a prompt based on a preamble, a list of a user's previous posts, and additional prompts provided by the user.

## Bot

The discord bot that takes commands and forwards them to either scraper or brain, then returns appropriate responses.

The bot can be interacted with using one of two commands, `hey ROBOT` and `hey SUBJECT`, where `SUBJECT` is the name of person the bot is currently 'impersonating'

### `hey SUBJECT`
This is used to interact with ROBOT's persona, anything after `hey SUBJECT` is added to the conversation logs kept by `brain`
and is then sent to gpt-3 as a query.
The response is then sent in the channel the command was posted in.

### `hey ROBOT`:
All commands following `hey ROBOT` are used to interact with the bot itself, not its 'persona'. Possible interactions include:
- `rename to X` to change name of ROBOT
  - This updates both the bot's nickname in the server and the name used to address the `SUBJECT`.
  - TODO: Also update the name used in the 'conversation' created by brain, which will allow ROBOT to recognise its own name in conversation
- `remember that` to force ROBOT to include recent conversation in all future prompts to gpt-3
- `become X` to make ROBOT change its persona
  - can take a dump of a `writer` object as a `.JSON`
  - can take a list of example posts from a subject as a `.txt`
  - TODO: take the url of a facebook page, and scrape posts