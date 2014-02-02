Reddit to Tumblr Bot
=====================

This is a bot written in Python using the following libraries:

- [PRAW](https://github.com/praw-dev/praw) for accessing the Reddit API
- [Pytumblr](https://github.com/tumblr/pytumblr) for accessing the Tumblr API

The purpose of this bot is to periodically query a specified subreddit via the Reddit API for newest posts. If a previous query has been executed, it will only query for posts after the latest ID. From there, it parses the post titles for the information desired for Tumblr. The Tumblr API is then utilized in order to create new posts for each retrieved Reddit post.