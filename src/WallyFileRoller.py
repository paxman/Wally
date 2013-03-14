import os
from random import choice

class WallyFileRoller():
    
    def __init__(self, root):
        self.root = root
        self.files = None
        self.get_files()
    
    def get_files(self):
        if self.is_valid_path():
            matches = []
            for root, dirnames, filenames in os.walk(self.root):
                for filename in filenames:
                    if filename.endswith(('.jpg', '.jpeg', '.gif', '.png', '.bmp', '.tiff')):
                        matches.append(os.path.join(root, filename))
            self.files = matches
            print "Read "+str(len(self.files))+" files"
        else:
            print "Path not valid, no files loaded - using old files, if present!"
            
    def get_next_file(self):
        filepath = choice(self.files)
        return filepath
    
    def set_path(self, path):
        self.root = path
        self.get_files()
    
    def has_files(self):
        if self.files:
            return True
        
        return False
    
    def is_valid_path(self):
        if self.root == "" or not os.path.isdir(self.root):
            return False
        return True
    