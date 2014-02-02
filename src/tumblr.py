import pytumblr, ConfigParser

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
        
        print self.t.create_audio(self.blogName, caption=audioCaption, tags=post['genres'], external_url=post['url'])
        
    # create a Tumblr post of type video
    def createVideoPost(self, post):
        return
        # build caption for post with available data
        videoCaption = post['artist'] + ' - ' + post['songTitle']
        if(post['genres'] is not None):
            videoCaption += ' [' + " / ".join(post['genres']) + ']' 
        if(post['songYear'] is not None):
            videoCaption += ' (' + post['songYear'] + ')'
        videoCaption = videoCaption.encode("utf-8")
            
        self.t.create_video(self.blogName, caption=videoCaption, tags=post['genres'], embed=str(post['url']))
        
    # create a Tumblr post of type link
    def createLinkPost(self, post):
        # build title for post with available data
        linkTitle = post['artist'] + ' - ' + post['songTitle']
        if(post['genres'] is not None):
            linkTitle += ' [' + " / ".join(post['genres']) + ']' 
        if(post['songYear'] is not None):
            linkTitle += ' (' + post['songYear'] + ')'
        linkTitle = linkTitle.encode("utf-8")
            
        self.t.create_link(self.blogName, title=linkTitle, tags=post['genres'], url=str(post['url']))