from plugins.bases.handlers import HandlersBase

class upload(HandlersBase):
    WEB_PATH = r"/upload/?"
    STORE_ATTRS = True
    STORE_UNREF = True
    OPTS = {}
    PAGE_TITLE = "Upload Your Memories"
    
    def get(self):
        """
        Browser-based uploads will pass along a HTTP status code of the upload 
        along with the video ID on success.  It is passed via URI so we just 
        get the argument.
        """
        status = self.get_argument("status", None)
        vidid = self.get_argument("id", None)
        
        # By default we haven't tried to add a video
        added = -1
        
        # Load up the YouTube reference and get the new ID/video episode
        self.yt_instance()
        index = self.yt_playlist_count() + 1
        
        # Store the new video title and description (needed to get YouTube upload token)
        video_title = "Wedding Video #%d" % index
        video_desc = video_title
        
        # Pre-dispose media group data (see plugins/bases/handlers.py)
        mg = self.yt_mediagroup(video_title, video_desc)
        
        # We need the YouTube URL to post to as well as the token
        post_url, youtube_token = self.yt_uploadtoken(mg)
        
        # If we submitted a video successfully try to add it to the playlist
        if vidid != None:
            added = self.yt_vid2pl(vidid, video_title, video_desc)
                
        self.show("upload", token=[post_url,youtube_token], status=status, vidid=vidid, added_to_list=added)
