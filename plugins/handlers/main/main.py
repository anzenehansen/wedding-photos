from plugins.bases.handlers import HandlersBase
import os
import sys

class MainHandler(HandlersBase):
    WEB_PATH = r"/"
    STORE_ATTRS = True
    STORE_UNREF = True
    OPTS = {}
    JS_FILES = ['main']

    def get(self):
        data = []
        
        # Get the system stats of "/" (mount point of where we store the pictures)
        stat = os.statvfs('/')
        
        """
        By default statvfs returns long-ints (L), but we want to be able to work from 
        decimals as well.  So we convert each ending result to a float, then round to 
        2 decimal spots.
        
        We have to multiply by f_frsize because the data is returned as "# of blocks", 
        instead of bytes.  This way we can convert the information to bytes (blocks * type = bytes_type / blocks).
        """
        space_avail = round( (float(stat.f_bavail * stat.f_frsize) / float(stat.f_blocks * stat.f_frsize)) * 100, 2)
        
        # Load up YouTube instance in our class
        self.yt_instance()
        
        # Get the playlist so far
        playlist_video_feed = self.yt_playlist()
        
        entry = []
        
        for e in playlist_video_feed.entry:
            entry.append(e)
        
        # The path to our pictures
        path = "%s/templates/bootstrap/img/wedding/" % os.getcwd()
        
        # Load up each listing into a list
        photos = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        self.show("main", avail=space_avail, videos=entry, pics=photos)
