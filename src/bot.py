import tumblr, reddit, time, re

class Bot():
    def __init__(self, subreddit, queryType = 'hot', limit = 20, timer = 3600):
        self.redditAPI = reddit.API()
        self.tumblrAPI = tumblr.API()
        self.subreddit = subreddit
        self.timer = timer
        self.queryType = queryType.lower()
        self.limit = limit
        self.latest = None

    # get latest posts from specified subreddit via reddit API
    def getLatestRedditPosts(self):
        posts = self.redditAPI.getPosts(subreddit=self.subreddit,limit = self.limit, queryType = self.queryType, after=self.latest)

        # update self.latest for later paginated queries
        if(len(posts) > 0):
            self.latest = "t3_" + str(posts[-1].id)

        return posts

    # get song artist from reddit post title
    def getSongArtist(self, postTitle):
        try:
            return re.search('-{1,2} (.+) \[|\(', postTitle).groups()[0].replace('&amp;', '&')
        except:
            return None

    # get song title from reddit post title
    def getSongTitle(self, postTitle):
        try:
            return re.search('(.+) -{1,2}', postTitle).groups()[0]
        except:
            return None

    # get song genres from reddit post title
    def getSongGenres(self, postTitle):
        try:
            allGenres = re.search('\[(.+)\]', postTitle).groups()[0];
        except:
            return None

        if '/' in allGenres:
            genres = [x.strip(' ').title() for x in allGenres.split('/')]
        elif ',' in allGenres:
            genres = [x.strip(' ').title() for x in allGenres.split(',')]
        else:
            genres = [allGenres.strip(' ').title()]

        return genres

    # get song year from reddit post title
    def getSongYear(self, postTitle):
        try:
            return re.search('\((\d+)\)', postTitle).groups()[0];
        except:
            return None

    # pull necessary information from reddit posts
    def getFormattedRedditPosts(self):
        redditPosts = self.getLatestRedditPosts()
        formattedPosts = []

        for post in (x for x in redditPosts if x is not None):
            formattedPost = {}

            # only parse and save post if it isn't a self post
            if(not re.search('!reddit.com', post.url.lower(), re.IGNORECASE)):
                formattedPost['url'] = post.url
                formattedPost['artist'] = self.getSongArtist(post.title)
                formattedPost['songTitle'] = self.getSongTitle(post.title)
                formattedPost['genres'] = self.getSongGenres(post.title)
                formattedPost['songYear'] = self.getSongYear(post.title)

                # only process songs newer than 2012
                if(formattedPost['songYear'] is not None and int(formattedPost['songYear']) > 2012):
                    formattedPosts.append(formattedPost)

        return formattedPosts

    # create Tumblr posts for all retrieved reddit posts
    def createTumblrPosts(self, redditPosts):
        for post in redditPosts:
            # do something with youtube links
            if(re.search('youtube.com', post['url'], re.IGNORECASE)):
                self.tumblrAPI.createYoutubePost(post)

            # do something with vimeo links
            if(re.search('vimeo.com', post['url'], re.IGNORECASE)):
                self.tumblrAPI.createVimeoPost(post)

            # do something with audio links
            elif(re.search('soundcloud.com|bandcamp.com', post['url'], re.IGNORECASE)):
                self.tumblrAPI.createAudioPost(post)

    # query for reddit posts and subsequently create Tumblr posts
    def process(self):
        redditPosts = self.getFormattedRedditPosts()
        if(len(redditPosts) > 0):
            self.createTumblrPosts(redditPosts)

    def run(self):
        cycleCount = 0
        while True:
            # start from beginning every 12 hours if we're retrieving 'hot' posts
            if(self.queryType.lower() == 'hot'):
                if(cycleCount == 12):
                    self.latest = None
                    cycleCount = 0
                cycleCount += 1

            self.process()
            time.sleep(self.timer)