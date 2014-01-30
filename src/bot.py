import tumblr, reddit

class Bot():
    def __init__(self, subreddit = 'listentothis'):
        self.redditAPI = reddit.API()
        self.tumblrAPI = tumblr.API()
        self.subreddit = subreddit
        self.latest = None
        
    # get posts from /r/listentothis via reddit API
    def getRedditPosts(self):
        # check to see if query should be paginated
        if(self.latest is not None):
            posts = self.redditAPI.getNewPosts(subreddit=self.subreddit, after=self.latest)
        else:
            posts = self.redditAPI.getNewPosts(subreddit=self.subreddit)
        
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
                while(remainingPostTitle[i+1] != ')'):
                    year += str(remainingPostTitle[i+1])
                    i += 1
                else:
                    return year
    
    # pull necessary information from reddit posts
    def getFormattedRedditPosts(self):
        redditPosts = self.getRedditPosts()
        
        formattedPosts = []
        
        for post in redditPosts:
            print "\n", post.title
            formattedPost = {}
            
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
            # do something with video links
            if('youtube' in post['url'].lower() or 'vimeo' in post['url'].lower()):
                self.tumblrAPI.createVideoPost(post)
            
            # do something with audio links
            elif('soundcloud' in post['url'].lower() or 'bandcamp' in post['url'].lower()):
                self.tumblrAPI.createAudioPost(post)
        
    # query for reddit posts and subsequently create Tumblr posts
    def process(self):
        self.createTumblrPosts(self.getFormattedRedditPosts())