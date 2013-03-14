from gobject import timeout_add_seconds, source_remove

class WallyTimer():
    def __init__(self, manager):
        self.manager = manager
        self.interval = manager.config.get_selected_interval()
        self.timer = None 
    
    def stop(self):
        #if timer running
        if self.timer:
            source_remove(self.timer)
            self.timer = None
            print "Timer stopped."
            
        print "Timer already stopped."
    
    def set_interval(self, interval):
        #print interval
        self.interval = interval*60
        
        #if running
        if self.timer:
            self.stop()
            self.start()
            print "Timer restarted"
    
    def start(self):
        self.stop()
        self.set_interval(self.manager.config.get_selected_interval())
        self.timer = timeout_add_seconds(self.interval,self.manager.change_wallpaper)
        print "Timer started with interval of",str(self.interval),"seconds"