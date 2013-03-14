from WallyConfig import WallyConfig
from WallyTimer import WallyTimer
from WallyFileRoller import WallyFileRoller
from WallyWrapper import WallyWrapper
from WallyGUI import WallyTray
from WallyGUI import WallyAboutDialog, WallyFolderSelector, WallyIntervalInput
import gtk,os

class WallyManager():
    
    default_intervals = (60,30,15,10,5,3,2,1)
    default_max_interval = 600
    
    def __init__(self):
        self.config = WallyConfig()
        self.wrapper = WallyWrapper()
        self.timer = WallyTimer(self)
        self.fileroller = WallyFileRoller(self.config.get_path())
        self.tray = WallyTray(self)
         
    def user_change_wallpaper(self, widget, event,**kwarg):
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            self.stop()
            self.change_wallpaper()
            self.start()
        
    def change_wallpaper(self):
        selected_file = self.fileroller.get_next_file()
        self.wrapper.change_wallpaper(selected_file,self.config.get_mode())
        self.tray.set_tooltip(os.path.basename(selected_file))
        print "Wallpaper changed to:",selected_file
        return True
       
    def changed_interval(self, *args, **kwargs):
        #print kwargs
        interval = kwargs['time']
        interval_type = kwargs['interval_type']
        #let's be reasonable, m'kay? ;)
        #max 10 hours
        if interval > 0 and interval < self.default_max_interval:
            #if change to preselected
            if interval_type == 0:
                self.config.set_interval(interval)
                #change from custom to preselected 
                if self.config.get_interval_type() == 1:
                    self.tray.deselect_custom_interval_button()
            else:
                self.config.set_custom_interval(interval)
                self.tray.select_custom_interval_button()
                self.tray.set_custom_label("Custom: "+str(self.config.get_custom_interval()))

            self.changed_interval_type(interval_type=interval_type)    
            
    def changed_interval_type(self, interval_type):
        self.config.set_interval_type(interval_type)
        self.stop()
        self.start()
            
    def changed_mode(self,*args,**kwargs):
        mode = kwargs['mode']
        print mode
        if mode in self.wrapper.supported_modes():
            print "Mode changed to",mode
            self.config.set_mode(mode)
            self.change_wallpaper()
             
    def set_folder(self, path):
        self.stop()
        self.fileroller.set_path(path) 
        self.config.set_path(path)
        self.start()

    def start(self,*args,**kwargs):
        #don't start if bogus
        if self.fileroller.has_files() and self.fileroller.is_valid_path():
            self.timer.start()
        else:
            print "Path not valid or no matching files, no files loaded!"
            self.show_select_folder(None,None)
            
    def stop(self,*args,**kwargs):
        self.timer.stop()
        self.tray.set_tooltip("Wally")
    
    def show_about_dialog(self, widget,event):
        about_dialog = WallyAboutDialog()
        about_dialog.run()
        about_dialog.destroy()
    
    def show_select_folder(self, widget,event):
        select_dialog = WallyFolderSelector("Select folder:", self.config.get_path())
        response = select_dialog.run()
        
        if response == gtk.RESPONSE_OK:
            folder = select_dialog.get_filename()
            self.set_folder(folder)
            self.tray.set_path_label(folder)
            
        select_dialog.destroy()    

    def show_select_interval(self, widget,event):
        messagedialog = WallyIntervalInput("Set custom interval (in minutes)")
        response = messagedialog.run() 
        time = messagedialog.get_input()
        messagedialog.destroy()
        
        if response == gtk.RESPONSE_OK:
            self.changed_interval(time=int(time),interval_type=1)
    
                
    def do_quit(self, *args):
        self.stop()
        self.config.save_config()
        gtk.main_quit()
    
    def main(self):
        self.start()