import ConfigParser
import os
from WallyWrapper import WallyWrapper

class WallyConfig():
    
    def __init__(self):
        self.load()
        
    def load(self):
        user_path = os.path.expanduser("~")
        
        #use defaults 
        if not os.path.isfile(user_path+"/.config/wally/config.cfg"):
            self.set_default()
        else:
            try:
                config = ConfigParser.RawConfigParser(allow_no_value=True)
                config.read(user_path+"/.config/wally/config.cfg")
                self.interval = config.getint("wally", "interval")
                self.custom_interval = config.getint("wally", "custom_interval")
                self.interval_type = config.getint("wally", "interval_type")
                self.mode = config.get("wally", "mode")
                self.path = config.get("wally", "path")
            #if any errors
            except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
                self.set_default()
    
    def get_mode(self):
        return self.mode
    
    def get_interval(self):
        return self.interval
 
    def get_custom_interval(self):
        return self.custom_interval
    
    def get_selected_interval(self):
        if self.get_interval_type() == 0:
            return self.get_interval()
        else:
            return self.get_custom_interval()
    
    def get_interval_type(self):
        return self.interval_type
     
    def get_path(self):
        return self.path
    
    def set_mode(self, mode):
        self.mode = mode
    
    def set_interval(self, interval):
        self.interval = interval
        
    def set_custom_interval(self, custom_interval):
        self.custom_interval = custom_interval
    
    def set_interval_type(self, interval_type):
        self.interval_type = interval_type
            
    def set_path(self, path):
        self.path = path
    
    def set_default(self):
        print "Loading defaults.."
        self.interval = 5
        self.custom_interval = 6
        self.interval_type = 0
        self.mode = "fit"
        self.path = WallyWrapper.user_pictures_folder()
    
    def save_config(self):
        print "Saving..."
        #TODO: allow no value for excluded files 
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.add_section("wally")
        config.set("wally",'interval', self.get_interval())
        config.set("wally",'custom_interval', self.get_custom_interval())
        config.set("wally",'interval_type', self.get_interval_type())
        config.set("wally",'mode', self.get_mode())
        config.set("wally",'path', self.get_path())
        user_path = os.path.expanduser("~")
        
        #create folder if it does not exist
        if not os.path.isdir(user_path+"/.config/wally/"):
            os.makedirs(user_path+"/.config/wally/")
            
        with open(user_path + "/.config/wally/config.cfg", 'wb') as configfile:
            config.write(configfile)
        print "...done"