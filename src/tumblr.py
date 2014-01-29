import pytumblr

class API(object):
    # initialize Tumblr client
    def __init__(self):
        self.t = pytumblr.TumblrRestClient(
            '<consumer_key>',
            '<consumer_secret>',
            '<oauth_token>',
            '<oauth_secret>',
        )
        self.blogName = "thenewmusicmachine"
        
    # create a Tumblr post of type audio
    def createAudioPost(self, post):
        audioCaption = post['artist'] + ' - ' + post['songTitle'] + ' [' + post['genres'].join(' / ') + '] (' + post['songYear'] + ')'
        self.t.create_audio(self.blogName, caption=audioCaption, data=post['url'])
        
    # create a Tumblr post of type video
    def createVideoPost(self, post):
        videoCaption = post['artist'] + ' - ' + post['songTitle'] + ' [' + post['genres'].join(' / ') + '] (' + post['songYear'] + ')'
        self.t.create_video(self.blogName, caption=videoCaption, data=post['url'])
        
    # create a Tumblr post of type link
    def createLinkPost(self, post):
        linkTitle = post['artist'] + ' - ' + post['songTitle'] + ' [' + post['genres'].join(' / ') + '] (' + post['songYear'] + ')'
        self.t.create_link(self.blogName, title=linkTitle, url=post['url'])
        