Reddit to Tumblr Bot
=====================
This is a bot written in Python using the following libraries:

- [PRAW](https://github.com/praw-dev/praw) for accessing the Reddit API
- [Pytumblr](https://github.com/tumblr/pytumblr) for accessing the Tumblr API

The purpose of this bot is to periodically query a specified subreddit via the Reddit API for newest posts. If a previous query has been executed, it will only query for posts after the latest ID. From there, it parses the post titles for the information desired for Tumblr. The Tumblr API is then utilized in order to create new posts for each retrieved Reddit post.

Bot Parameters
---------------
When initializing the Reddit-to-Tumblr bot, it accepts four parameters (not including all your API keys). They are:

- `subreddit` (str): the name of the subreddit from which to retrieve posts. Has no default.
- `queryType` (str): the type of posts to retrieve from the specified subreddit. Options are `hot` (default) and `new`.
- `timer` (int): the number of seconds to wait in between retrieving and posting. Defaults to `3600`, or 1 hour.
- `limit` (int): the maximum number of posts to retrieve from Reddit per query. Defaults to `20`.

As the project is currently configured, all of these parameters are pulled from a global configuration file. The structure and use of this configuration file is described below.

Sample Configuration File
--------------------------
The bot is currently set up to draw all API keys and parameters from a configuration file. Although this isn't required and can be changed pretty easily, it is a quick way to input all your information and get up and running. Below is how your configuration file should look if you choose to go this route:

```
[tumblr]
blogName : YOUR BLOG NAME HERE
consumerKey : YOUR TUMBLR CONSUMER KEY HERE
consumerSecret : YOUR TUMBLR CONSUMER SECRET HERE
oauthToken : YOUR TUMBLR OAUTH TOKEN HERE
oauthSecret : YOUR TUMBLR OAUTH SECRET HERE

[reddit]
userAgent : A SHORT DESCRIPTION OF YOUR BOT HERE
subreddit : THE NAME OF THE SUBREDDIT TO GET POSTS FROM HERE
queryType : EITHER hot OR new
limit : NUMBER OF POSTS TO RETRIEVE AT A TIME FROM REDDIT

[timer]
seconds : THE NUMBER OF SECONDS TO WAIT IN BETWEEN RETRIEVING/CREATING POSTS
```

**A few notes:**
- The configuration file should be titled 'settings.cfg' and should be placed in the same directory as the source `.py` files
- All parameters drawn from the config file are automatically strings. Quotes are not necessary, and for things like the number of seconds they must be cast as `int` when used (this is already done for you).