# -*- coding=utf-8 -*-
# Alan Exaile plugin v0.1
# Copyright © 2013 Semplice Team. All rights reserved.
# Written by Luca B. <sidtux _AT_ gmail _DOT_ com>, released under GPLv3 license.

import alan.core.structure as struct
import alan.core.objects.core as core
import alan.core.actions.glob as ga
import t9n.library as trans

import alan.core.extension

import os, sys, dbus

_ = trans.translation_init("alan")

executable = " ".join(sys.argv)

# Information about this extension ;)
coders = { "Luca B.":"http://semplice-linux.sourceforge.net" }
infos = {_("Coders"):coders}

# Initialize the session bus
bus = dbus.SessionBus()

class Exaile:
    def playpause(self, iface):
        iface.PlayPause()

    def stop(self, iface):
        iface.Stop()

    def prev(self, iface):
        iface.Prev()

    def next(self, iface):
        iface.Next()

class Extension(alan.core.extension.Extension):
    def run(self):

        # Initiate pipemenu
        self.menu = struct.PipeMenu()
        self.menu.start() # add initial tag
        
        i = self.menu.insert
        
        i(core.header("Exaile"))
            
        try:
            self.remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
            self.iface = dbus.Interface(self.remote_object, "org.exaile.Exaile")

            if self.iface.GetState() == "playing":
                i(core.item(_("Pause"), ga.execute("alan-show-extension %s playpause" % sys.argv[1]), icon="media-playback-pause"))
            else:
                i(core.item(_("Play"), ga.execute("alan-show-extension %s playpause" % sys.argv[1]), icon="media-playback-start"))
                
            i(core.item(_("Stop"), ga.execute("alan-show-extension %s stop" % sys.argv[1]), icon="media-playback-stop"))
    
            i(core.separator)
    
            i(core.item(_("Previous"), ga.execute("alan-show-extension %s prev" % sys.argv[1]), icon="media-skip-backward"))
            i(core.item(_("Next"), ga.execute("alan-show-extension %s next" % sys.argv[1]), icon="media-skip-forward"))
            
            i(core.separator)
            # Displays infos about the current song
            if(self.iface.IsPlaying()):
                i(core.item(self.iface.GetTrackAttr("title"), ga.execute("echo"), icon="audio-x-generic"))
                i(core.item(self.iface.GetTrackAttr("album"), ga.execute("echo"), icon="media-optical"))
                i(core.item(self.iface.GetTrackAttr("artist"), ga.execute("echo"), icon="audio-input-microphone"))
            else:
                #i(core.item(_("Open Exaile"), ga.execute("exaile"), icon="/usr/share/pixmaps/exaile.png"))
                i(core.item(_("Exaile is not playing."), ga.execute("echo"), icon=""))
        except dbus.exceptions.DBusException:
            i(core.item(_("Open Exaile"), ga.execute("exaile"), icon="exaile"))
            #print("Exaile is not running.")

        self.menu.end()

if len(sys.argv) > 2:
    try:
        remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
        iface = dbus.Interface(remote_object, "org.exaile.Exaile")
        if sys.argv[2] == "playpause":
            Exaile().playpause(iface)
        elif sys.argv[2] == "stop":
            Exaile().stop(iface)
        elif sys.argv[2] == "prev":
            Exaile().prev(iface)
        elif sys.argv[2] == "next":
            Exaile().next(iface)
    except:
        pass
