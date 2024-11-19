# About

I wanted to include this to explain the code.

**Originally**, I thought it would be a good idea to use webpack to bundle the code so that I could have separate scripts for Firefox and Google Chrome.

The main reason was so that we could use the sidepanel API in both extensions.
Although I realized later it was more complicated than I thought,
so I decided to leave webpack.

## Content Scripts

The main purpose of the content script is to grab the necessary information from Canvas,
and then use messages to send to the background script.

## Background Scripts

This creates and sets a JWT as a cookie for our main site (which is also an iFrame in the sidepanel)
for user login in. Additionally, this script has the environment variables to send information to
the backend `api.aitutor.live`
