#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
from WallyManager import WallyManager
from WallyWrapper import WallyWrapper
from WallyGUI import WallyMessageDialog

if __name__ == "__main__":
    
    if not WallyWrapper.system_has_prerequisites():
        WallyMessageDialog("System hasn't got installed/enabled prerequisites!")
        exit(0)
        
    manager = WallyManager()
    manager.main()
    gtk.main()