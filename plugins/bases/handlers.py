import tornado.web
import traceback
from plugins.bases.plugin import PluginBase
import os
import sys

import gdata
import gdata.youtube
import gdata.youtube.service

class HandlersBase(tornado.web.RequestHandler, PluginBase):
    # Every handler must have a web path, override this in this fashion
    WEB_PATH = r"/"
    STORE_ATTRS = True
    STORE_UNREF = True

    # Specifies what JS and CSS files to load from templates/bootstrap/[css|js]
    JS_FILES = []
    CSS_FILES = []

    # Used as a default for every page
    PAGE_TITLE = "Home"
    
    def initialize(self, **kwargs):
        self.sysconf = kwargs.get("sysconf", None)
        
    def get_template_path(self):
        return "%s/templates" % os.path.dirname(os.path.realpath(sys.argv[0]))
    
    # Initialize YouTube reference to perform actions
    def yt_instance(self):
        self.yt_service = gdata.youtube.service.YouTubeService()
        self.yt_service.ssl = True
        self.yt_service.developer_key = self.sysconf.devid
        self.yt_service.client_id = self.sysconf.clientid
        self.yt_service.email = self.sysconf.gmail
        self.yt_service.password = self.sysconf.gpass
        self.yt_service.source = self.sysconf.clientid
        self.yt_service.ProgrammaticLogin()
    
    # Simple class property to return the playlist URI
    @property
    def yt_plist_uri(self):
        return "http://gdata.youtube.com/feeds/api/playlists/%s" % self.sysconf.playlist
    
    # Return the data about the playlist
    def yt_playlist(self):
        return self.yt_service.GetYouTubePlaylistVideoFeed(uri=self.yt_plist_uri)
    
    # Get total number of videos in playlist
    def yt_playlist_count(self):
        plist = self.yt_playlist()
        
        entry = []
        
        for e in plist.entry:
            entry.append(e)
        
        return len(entry)
    
    # Wrapper to get upload token for YouTube video post request
    def yt_uploadtoken(self, mg):
        video_entry = gdata.youtube.YouTubeVideoEntry(media=mg)
        response = self.yt_service.GetFormUploadToken(video_entry)
        
        return (response[0], response[1])
    
    # This defines various aspects of the video
    def yt_mediagroup(self, title, desc):
        return gdata.media.Group(
            title = gdata.media.Title(text=title),
            description = gdata.media.Description(description_type='plain', text=desc),
            keywords=gdata.media.Keywords(text='amber, eric, wedding, 2013, october, 31, halloween'),
            category=[gdata.media.Category(
                text='People',
                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                label='People')],
            player=None
        )
    
    # Adds a video to playlist
    def yt_vid2pl(self, vidid, title, desc):
        video_entry = self.yt_service.AddPlaylistVideoEntryToPlaylist(
                self.yt_plist_uri, vidid, title, desc
            )
            
        if isinstance(video_entry, gdata.youtube.YouTubePlaylistVideoEntry):
            return 1
        
        return 0
        
    """
    show

    Wrapper around RequestHandler's render function to make rendering these templates easier/better.
    This way the class just has to specify what special CSS and/or JavaScript files to load (see handlers/main),
    and it is automatically passed to the template engine to parse and deal with.

    Easier management and use IMO.
    """
    def show(self, templ, **kwargs):
        # What JavaScript files to load?
        js = ["jquery", "bootstrap.min", "common", "jquery.prettyPhoto"]
        js.extend(self.JS_FILES)
        
        # CSS files we want for the particular page
        css = ["common", "prettyPhoto"]
        css.extend(self.CSS_FILES)
        
        # We pass specifics to the page as well as any uniques via kwargs passed from here
        self.render("%s.html" % templ, 
                    js=js, css=css, 
                    page_title=self.PAGE_TITLE, 
                    plistid=self.sysconf.playlist, 
                    **kwargs)

    def write_error(self, status_code, **kwargs):
        path = os.path.dirname(os.path.realpath(sys.argv[0]))

        _,err,_ = kwargs['exc_info']
        
        msg = "Unfortunately an error has occured.  If you believe this is in error, please contact support.<br /><br />"
        msg += "Error: %s" % (err)
        
        self.show("%s/templates/message" % path, path=path, message=msg)
