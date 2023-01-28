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

The part that constructs prompts for gpt-3 and gets responses. Not implemented yet

### TODO for brain:
- Finalize preamble
- choose what posts to pass
- write endpoint for bot to use <- THE MAIN PART
- test endpoint with custom personas
- test endpoint with subject1

### Features for Brain

#### Must haves

- Make preamble given posts
- send prompt/return response
  - keep a log of conversation
  - return just the response

#### Should haves
- Shorten the conversation logs to reduce tokens per query
  - see thoughts
- Function to adjust the preamble/heat

## Bot

The discord bot that takes commands and forwards them to either scraper or brain, then returns appropriate responses. Not implemented yet

## Thoughts

Number of tokens per request increases as conversation goes on, meaning more expensive too.
This makes longer dialogues with SUBJECT too expensive, what do we make him forget?
- If X many minutes pass without SUBJECT being addressed, reset to originial prompt?
- Let users 'save' chunks of conversation via command?
  - If they particularly like a conversation, and want the model to continue acting like that
    - "hey ROBOT, remember that"
- Maybe this isnt even the case?
  - Actually it probably is if ur using the API, how couldnt it be

For given persona/iteration, keep track of the whole conversation as a json of
```json
[
    {
        question: "hey SUBJECT, whats up?",
        answer: "oh you know, cant complain",
        time: xx-xx-xx-xxxx,
        must_include: False,
    }

]
```
This makes it much easier to choose what to include/remove in the next prompt  

  

Have a different trigger word for conversation and for commands
- 'hey SUBJECT'
  - trigger for conversation
- 'hey ROBOT'
  - trigger for commands
- What if SUBJECT == ROBOT?
  - I dont know
    - probably fine

Different preambles for different situations?
- The responses could change depending on how the examples are framed in the preamble, maybe a couple of different candidate preambles that can be switched between wouldnt be too bad
- "This is a conversation between SUBJECT and THECORD"
- "This is an argument between SUBJECT and THECORD"
- and more!

