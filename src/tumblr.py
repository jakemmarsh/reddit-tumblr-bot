import pytumblr, ConfigParser, re, sys

config = ConfigParser.RawConfigParser()
config.read('settings.cfg')

class API(object):
    # initialize Tumblr client
    def __init__(self):
        self.t = pytumblr.TumblrRestClient(
            config.get('tumblr', 'consumerKey'),
            config.get('tumblr', 'consumerSecret'),
            config.get('tumblr', 'oauthToken'),
            config.get('tumblr', 'oauthSecret')
        )
        self.blogName = config.get('tumblr', 'blogName')
        
    # create a Tumblr post of type audio
    def createAudioPost(self, post):
        # build caption for post with available data
        audioCaption = post['artist'] + ' - ' + post['songTitle']
        if(post['genres'] is not None):
            audioCaption += ' [' + " / ".join(post['genres']) + ']' 
        if(post['songYear'] is not None):
            audioCaption += ' (' + post['songYear'] + ')'
        audioCaption = audioCaption.encode("utf-8")
        
        try:
            print self.t.create_audio(self.blogName, caption=audioCaption, tags=post['genres'], external_url=post['url'])
        except:
            print "failed to create audio post:", sys.exc_info()[0]
        
    # create a Tumblr post for youtube video
    def createYoutubePost(self, post):
        # build caption for post with available data
        videoCaption = post['artist'] + ' - ' + post['songTitle']
        if(post['genres'] is not None):
            videoCaption += ' [' + " / ".join(post['genres']) + ']' 
        if(post['songYear'] is not None):
            videoCaption += ' (' + post['songYear'] + ')'
        videoCaption = videoCaption.encode("utf-8")
        
        # get video ID from URL
        regex = re.compile("v\=([\-\w]+)")
        videoId = regex.search(post['url'])
        try:
            videoId = videoId.groups()[0]
        except:
            return
        
        # create embed code string using video ID
        embedString = '<iframe id="ytplayer" type="text/html" width="640" height="390" src="http://www.youtube.com/embed/' + videoId + '?frameborder="0"/>'
            
        try:
            print self.t.create_video(self.blogName, caption=videoCaption, tags=post['genres'], embed=embedString)
        except:
            print "failed to create youtube post:", sys.exc_info()[0]
        
    # create a Tumblr post for vimeo video
    def createVimeoPost(self, post):
        # build caption for post with available data
        videoCaption = post['artist'] + ' - ' + post['songTitle']
        if(post['genres'] is not None):
            videoCaption += ' [' + " / ".join(post['genres']) + ']' 
        if(post['songYear'] is not None):
            videoCaption += ' (' + post['songYear'] + ')'
        videoCaption = videoCaption.encode("utf-8")
        
        # get video ID from URL
        regex = re.compile("vimeo.com\/([\-\w]+)")
        videoId = regex.search(post['url'])
        try:
            videoId = videoId.groups()[0]
        except:
            return
        
        # create embed code string using video ID
        embedString = '<iframe src="//player.vimeo.com/video/' + videoId + '" width="640" height="390" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
            
        try:
            print self.t.create_video(self.blogName, caption=videoCaption, tags=post['genres'], embed=embedString)
        except:
            print "failed to create vimeo post:", sys.exc_info()[0]
        
    # create a Tumblr post of type link
    def createLinkPost(self, post):
        # build title for post with available data
        linkTitle = post['artist'] + ' - ' + post['songTitle']
        if(post['genres'] is not None):
            linkTitle += ' [' + " / ".join(post['genres']) + ']' 
        if(post['songYear'] is not None):
            linkTitle += ' (' + post['songYear'] + ')'
        linkTitle = linkTitle.encode("utf-8")
        
        try:
            print self.t.create_link(self.blogName, title=linkTitle, tags=post['genres'], url=str(post['url']))
        except:
            print "failed to create link post"