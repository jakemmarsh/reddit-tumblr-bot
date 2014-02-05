import praw, ConfigParser

config = ConfigParser.RawConfigParser()
config.read('settings.cfg')

class API(object):
    # initialize reddit client
    def __init__(self):
        self.r = praw.Reddit(user_agent=config.get('reddit', 'userAgent'))
        self.alreadyProcessed = []
        
    # get new posts from a subreddit
    def getNewPosts(self, subreddit, limit, after = None):
        returnPosts = []
        if(after):
            posts = self.r.get_subreddit(subreddit).get_new(limit=limit, params={'after': after})
        else:
            posts = self.r.get_subreddit(subreddit).get_new(limit=limit)
        
        # make sure we're only returning posts that haven't already been retrieved before
        for post in posts:
            if(post.id not in self.alreadyProcessed):
                returnPosts.append(post)
                # mark as processed
                self.alreadyProcessed.append(post.id)
                
        return returnPosts
    
    # get hot posts from a subreddit
    def getHotPosts(self, subreddit, limit, after = None):
        returnPosts = []
        if(after):
            posts = self.r.get_subreddit(subreddit).get_hot(limit=limit, params={'after': after})
        else:
            posts = self.r.get_subreddit(subreddit).get_hot(limit=limit)
        
        # make sure we're only returning posts that haven't already been retrieved before
        for post in posts:
            if(post.id not in self.alreadyProcessed):
                returnPosts.append(post)
                # mark as processed
                self.alreadyProcessed.append(post.id)
                
        return returnPosts