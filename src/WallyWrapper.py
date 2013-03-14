from subprocess import call, check_output, STDOUT, CalledProcessError
import string, os

class WallyWrapper():
    def __init__(self):
        pass
    
    @staticmethod
    def system_has_prerequisites(): 
        if not WallyWrapper.is_installed() or not WallyWrapper.is_managing_desktop() or not WallyWrapper.supports_wallpaper():
            return False
        return True
    
    @staticmethod
    def is_installed():
        try:
            check_output(["which pcmanfm"],stderr=STDOUT,shell=True)
        except CalledProcessError:
            print "PCManFM is NOT installed!"
            return False
        print "PCManFM IS installed!"
        return True
    
    @staticmethod
    def supports_wallpaper():
        output = check_output(["pcmanfm --help | grep wallpaper"],shell=True)
        splitted = string.split(output.strip(), "\n")
        if len(splitted) == 2:
            print "PCManFM SUPPORTS setting wallpaper!"
            return True
        print "PCManFM does NOT support setting wallpaper!"
        return False

    @staticmethod
    def is_managing_desktop():
        output = check_output(["ps ax | grep 'pcmanfm --desktop'"],shell=True)
        splitted = string.split(output.strip(), "\n")
        #print splitted
        if len(splitted) == 3:
            print "PCManFM IS managing desktop!"
            return True
        print "PCManFM is NOT managing desktop!"
        return False
    
    def supported_modes(self):
        output = check_output(["pcmanfm --help | grep wallpaper"],shell=True)
        all_modes = ("stretch","fit","tile","center")
        supported_modes = []
        for mode in all_modes:
            if mode in output:
                supported_modes.append(mode) 
        print "Supports:",supported_modes," modes."
        return supported_modes 
    
    def change_wallpaper(self, file_path, mode):
        #print "pcmanfm --set-wallpaper='"+file_path+"' --wallpaper-mode="+mode
        call(["pcmanfm --set-wallpaper='"+file_path+"' --wallpaper-mode="+mode],shell=True)
    
    @staticmethod
    def user_pictures_folder():
        output = ""
        xdg_installed = True
        
        #for ubuntu and similar
        try:
            output = check_output(["which xdg-user-dir"],stderr=STDOUT,shell=True)
        except CalledProcessError:
            print "xdg-user-dir is NOT installed!"
            xdg_installed = False
        
        if xdg_installed:
            output = check_output(["xdg-user-dir PICTURES"],shell=True)
            output = output.strip()
        #fallback to user home folder
        else:
            output = os.path.expanduser("~")
        
        print "Using",output,"as pictures folder"
        return output