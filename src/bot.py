import tumblr, reddit, time

class Bot():
    def __init__(self, subreddit, queryType = 'hot', limit = 20, timer = 3600):
        self.redditAPI = reddit.API()
        self.tumblrAPI = tumblr.API()
        self.subreddit = subreddit
        self.timer = timer
        # build function name to make correct API call
        self.queryType = 'get' + queryType.lower().title() + 'Posts'
        self.limit = limit
        self.latest = None
        
    # get latest posts from specified subreddit via reddit API
    def getLatestRedditPosts(self):
        # check to see if query should be paginated
        if(self.latest is not None):
            # use getattr in order to use variable as function call name
            posts = getattr(self.redditAPI, self.queryType)(subreddit=self.subreddit, limit = self.limit, after=self.latest)
        else:
            # use getattr in order to use variable as function call name
            posts = getattr(self.redditAPI, self.queryType)(subreddit=self.subreddit, limit = self.limit)
        
        # update self.latest for later paginated queries
        self.latest = posts[0].id
        
        return posts
        
    # get song artist from reddit post title
    def getSongArtist(self, postTitle):
        # TODO: use regex
        for i in range(0, len(postTitle)):
            if(postTitle[i] == '-'):
                # return song artist and remaining section of title
                # TODO: use real unescaping
                return postTitle[0:i-1], postTitle[i+2:].replace('&amp;', '&')
        
    # get song title from remaining unprocessed portion of reddit post title
    def getSongTitle(self, remainingPostTitle):
        # TODO: use regex
        for i in range(0, len(remainingPostTitle)):
            if(remainingPostTitle[i] == '['):
                # return song title and remaining section of title
                return remainingPostTitle[0:i-1], remainingPostTitle[i:]
            
    # get song genres from remaining unprocessed portion of reddit post title
    def getSongGenres(self, remainingPostTitle):
        # TODO: use regex
        allGenres = ''
        for i in range(0, len(remainingPostTitle)):
            if(remainingPostTitle[i] == '['):
                while(remainingPostTitle[i+1] != ']'):
                    allGenres += str(remainingPostTitle[i+1])
                    i += 1
                else:
                    if '/' in allGenres:
                        genres = [x.strip(' ').title() for x in allGenres.split('/')]
                    elif ',' in allGenres:
                        genres = [x.strip(' ').title() for x in allGenres.split(',')]
                    else:
                        genres = [allGenres.strip(' ').title()]
                    
                    return genres, remainingPostTitle[i:]
        
    # get song year from remaining unprocessed portion of reddit post title
    def getSongYear(self, remainingPostTitle):
    # TODO: use regex
        year = ''
        for i in range(0, len(remainingPostTitle)):
            if(remainingPostTitle[i] == '('):
                while(remainingPostTitle[i+1] != ')' and remainingPostTitle[i+1].isdigit()):
                    year += str(remainingPostTitle[i+1])
                    i += 1
                else:
                    # only return year if a valid one was found
                    if(len(year) > 0):
                        return year
                    else:
                        return None
    
    # pull necessary information from reddit posts
    def getFormattedRedditPosts(self):
        redditPosts = self.getLatestRedditPosts()
        
        formattedPosts = []
        
        for post in redditPosts:
            #print "\n", post.title
            formattedPost = {}
            
            # only parse and save post if it isn't a self post
            # TODO: use regex?
            if('www.reddit.com' not in post.url.lower()):
                # get URL
                formattedPost['url'] = post.url
                # get artist
                formattedPost['artist'], remainingTitle = self.getSongArtist(post.title)
                # get song title
                formattedPost['songTitle'], remainingTitle = self.getSongTitle(remainingTitle)
                # get genres
                formattedPost['genres'], remainingTitle = self.getSongGenres(remainingTitle)
                # get year
                formattedPost['songYear'] = self.getSongYear(remainingTitle)
                    
                formattedPosts.append(formattedPost)
        
        return formattedPosts
    
    # create Tumblr posts for all retrieved reddit posts
    def createTumblrPosts(self, redditPosts):  
        for post in redditPosts:
            # do something with youtube links
            # TODO: use regex?
            if('youtube.com' in post['url'].lower()):
                self.tumblrAPI.createYoutubePost(post)
                
            # do something with vimeo links
            # TODO: use regex?
            if('vimeo.com' in post['url'].lower()):
                self.tumblrAPI.createVimeoPost(post)
            
            # do something with audio links
            # TODO: use regex?
            elif('soundcloud.com' in post['url'].lower() or 'bandcamp.com' in post['url'].lower()):
                self.tumblrAPI.createAudioPost(post)
        
    # query for reddit posts and subsequently create Tumblr posts
    def process(self):
        self.createTumblrPosts(self.getFormattedRedditPosts())
        
    def run(self):
        while True:
            self.process()
            time.sleep(self.timer)