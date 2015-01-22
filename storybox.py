#!/usr/bin/env python

#=======================================
# StoryBox
# Version: .1
# by Jessica Oros
#=======================================

#---- Includes
import os
import wx
from subprocess import Popen, PIPE
from time import sleep

#---- Constants
STORY_DIR = '../stories/'
STORY_FILENAME = 'story'
STORY_LENGTH = 60
START_FULL_SCREEN = False
VIDEO_HEIGHT = 900
VIDEO_WIDTH = 1400

#---- Classes
class SBFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, wx.ID_ANY)
        self.InitUI()

    def InitUI(self):
        #---- Setup Menu
        #TODO setup menus

        #---- Setup Panels
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour('black')
        timer = wx.Timer(self)
        looping = False

        pnl1 = wx.Panel(self, wx.ID_ANY, size=(600, 900))
        pnl1.SetBackgroundColour('black')
        pnl2 = wx.Panel(self, wx.ID_ANY)
        pnl2.SetBackgroundColour('black')
        text = wx.StaticText(pnl2, wx.ID_ANY, "TOUCH HERE TO RECORD YOUR OWN " + str(STORY_LENGTH) + " SECOND STORY!", style=wx.ALIGN_CENTER)
        text.SetForegroundColour('white')
        text.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        startStop = wx.Button(pnl2, -1, label='Start')
        startStop.SetBackgroundColour('purple')
        startStop.SetForegroundColour('white')
        startStop.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        startStop.Bind(wx.EVT_BUTTON, self.StoryLoop)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(text, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(startStop, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        pnl2.SetSizer(vbox)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pnl1, flag=wx.EXPAND | wx.ALL)
        sizer.Add(pnl2, proportion=1, flag=wx.EXPAND | wx.ALL)
        
        self.SetSizer(sizer)
        panel.Layout()

    def StoryLoop(self, e):
        files = os.listdir(STORY_DIR)
        looping = True
        while(looping):
            for file in files:
                omx = Popen(['omxplayer','--win','200 0 1700 900', STORY_DIR + file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                omx.communicate()
                #self.CountDown()
            #return false here until we can stop it
            looping = False
        
    def CountDown(self):
        self.timer.Bind(wx.EVT_TIMER, self.update, self.timer)

    #def update(self, event):
        #TODO update

class StoryBox(wx.App):
    def OnInit(self):
        frame = SBFrame(None, "Storybox")
        self.SetTopWindow(frame)
        frame.Maximize()
        if(START_FULL_SCREEN):
            frame.ShowFullScreen(True)
        else:
            frame.Show(True)
            
        return True;
    
#---- Main
if __name__ == '__main__':
    sb = StoryBox()
    sb.MainLoop()
