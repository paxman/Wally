# -*- coding: utf-8 -*-

import gtk
from WallyUtil import Plural
from functools import partial

class WallyTray(gtk.StatusIcon):
    def __init__(self, manager):
        gtk.StatusIcon.__init__(self)
        self.manager = manager
        self.set_from_file("tango_desktop_preferences.png")
        self.connect('popup-menu', self.menu_popup)
        self.connect('button-press-event', self.manager.user_change_wallpaper)#self.on_double_click,test=1)
        
        self.set_tooltip('Wally')
        self.menu = None
        
        self.make_menu()
        
    def make_menu(self):
        self.menu = gtk.Menu()
        
        self.create_quit_item()
        self.create_about_item()
        
        #separator
        sep = gtk.SeparatorMenuItem()
        sep.show()
        self.menu.append(sep)
       
        self.create_path_items()
        self.create_mode_items()
        self.create_interval_items()
        
        #separator
        sep = gtk.SeparatorMenuItem()
        sep.show()
        self.menu.append(sep)
       
        self.create_stop_item()
        self.create_start_item()

    
    def create_quit_item(self):
        # add quit item
        self.quit = gtk.MenuItem("Quit")
        self.quit.show()
        self.quit.connect('button-press-event', self.manager.do_quit)
    
        self.menu.append(self.quit)
        
    def create_about_item(self):
        about = gtk.MenuItem("About")
        about.show()
        about.connect('button-press-event', self.manager.show_about_dialog)

        self.menu.append(about)
    
    def create_path_items(self):
        path = gtk.MenuItem("Path")
        path.show()
        self.menu.append(path)

        #path submenu
        self.path_submenu = gtk.Menu()
        
        if not self.manager.fileroller.has_files() or not self.manager.fileroller.is_valid_path():
            set_path = "Invalid path, select new"
        else:
            set_path = self.manager.config.get_path()
            
        self.path_real = gtk.MenuItem(set_path)
        self.path_real.show()
        path_sep = gtk.SeparatorMenuItem()
        path_sep.show()
        path_open = gtk.MenuItem("Select...")
        path_open.show()
        path_open.connect('button-press-event', self.manager.show_select_folder)
          
        self.path_submenu.append(self.path_real)
        self.path_submenu.append(path_sep)
        self.path_submenu.append(path_open)
        
        path.set_submenu(self.path_submenu)
    
    def create_mode_items(self):
        #modes
        modes = gtk.MenuItem("Mode")
        modes.show()
        self.menu.append(modes)
        
        #modes submenu
        self.interval_modes = gtk.Menu()
        set_mode = self.manager.config.get_mode()
        
        self.mode_buttons = []
        for mode in self.manager.wrapper.supported_modes():# ("Stretch","Fit","Center","Tile"):
            if mode == "stretch":
                group = None
            else:
                group = self.mode_buttons[0]
                 
            button = gtk.RadioMenuItem(group,mode.title())
            button.connect('button-press-event', partial( self.manager.changed_mode,mode=mode))
            button.show()
            if set_mode == mode:
                button.set_active(True)
                
            self.mode_buttons.append(button)
            self.interval_modes.append(button)
    
    
        modes.set_submenu(self.interval_modes)

    def create_interval_items(self):
        interval = gtk.MenuItem("Interval")
        interval.show()
        
        #interval values submenu
        self.interval_submenu = gtk.Menu()
        
        set_interval = self.manager.config.get_selected_interval()
        set_interval_type = self.manager.config.get_interval_type()
        
        self.buttons = []
        
        #custom interval
        self.custom = gtk.RadioMenuItem(None,"Custom: "+str(self.manager.config.get_custom_interval()))
        self.custom.show()
        self.custom.connect('button-press-event', partial(self.manager.changed_interval,time=self.manager.config.get_custom_interval(),interval_type=1))
        self.custom.connect('button-release-event',self.disable_propagation)
        
        self.interval_submenu.append(self.custom)
        self.buttons.append(self.custom)
        
        self.custom_interval = gtk.MenuItem("Change")
        self.custom_interval.show()
        self.custom_interval.connect('button-press-event', self.manager.show_select_interval)
        
        if set_interval_type == 1:
            self.custom.set_active(True)
        else:
            self.custom_interval.set_sensitive(False)
        
        self.interval_submenu.append(self.custom_interval)
        
        #preselected intervals
              
        self.custom_interval_sep = gtk.SeparatorMenuItem()
        self.custom_interval_sep.show()
        self.interval_submenu.append(self.custom_interval_sep)
         
        group = self.buttons[0]
        for time in self.manager.default_intervals:
            button = gtk.RadioMenuItem(group,Plural(time,"minute"))
            #button.connect('button-press-event',self.radio_button_activated,time*60)
            button.connect('button-press-event',partial(self.manager.changed_interval,time=time,interval_type=0))

            button.show()
            if set_interval == time and set_interval_type == 0:
                button.set_active(True)
                
            self.buttons.append(button)
            self.interval_submenu.append(button)
    
    
        interval.set_submenu(self.interval_submenu)

        self.menu.append(interval)
    
    def create_stop_item(self):
        self.stop = gtk.MenuItem("Stop")
        self.stop.show()
        self.menu.append(self.stop)
        self.stop.connect('button-press-event', self.manager.stop)
       
    def create_start_item(self):
        self.start = gtk.MenuItem("Start")
        self.start.show()
        self.menu.append(self.start)
        self.start.connect('button-press-event', self.manager.start)
            
    def disable_propagation(self, widget, event, **kwargs):
        #to prevent menu from closing on menu item click        
        return True
    
    def menu_popup(self, icon, event_button, event_time):
        self.menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self)
        self.menu.show()
    
    def deselect_custom_interval_button(self):
        self.custom.set_active(False)
        self.custom_interval.set_sensitive(False)
    
    def select_custom_interval_button(self):
        self.custom.set_active(True)
        self.custom_interval.set_sensitive(True)
        
    def set_custom_label(self, label):
        self.custom.set_label(label)
    
    def set_path_label(self, label):
        self.path_real.set_label(label)
            
class WallyFolderSelector(gtk.FileChooserDialog):
    def __init__(self, message,folder):
        gtk.FileChooserDialog.__init__(self,message,None,gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        self.set_current_folder(folder)
        self.set_default_response(gtk.RESPONSE_CANCEL)
        
class WallyIntervalInput(gtk.MessageDialog):
    def __init__(self, message):
        gtk.MessageDialog.__init__(self,parent=None,flags=0,type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_OK_CANCEL, message_format=message)
        
        action_area = self.get_content_area()
        adj = gtk.Adjustment(1, 0, 600, 1, 1)
        self.entry = gtk.SpinButton(adj)
        action_area.pack_start(self.entry)

        self.show_all()
        
    def get_input(self):
        time = self.entry.get_value_as_int()
        return time
        
class WallyAboutDialog(gtk.AboutDialog):
    def __init__(self, *args, **kwargs):
        gtk.AboutDialog.__init__(self, *args, **kwargs)
        self.set_destroy_with_parent (True)
        self.set_icon_name ("Wally")
        self.set_name('Wally')
        self.set_version('0.1 alpha')
        self.set_copyright("(C) 2013 paxman")
        self.set_comments(("Desktop background changer for PCManFM file browser"))
        
class WallyMessageDialog(gtk.MessageDialog):
    def __init__(self, message):
        gtk.MessageDialog.__init__(self,parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format=message)
        self.run()
        self.destroy()
          
        