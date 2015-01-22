#!/usr/bin/env python

#=======================================
# TOHP Storybox
# Version: .1
# by Jessica Oros
#=======================================
import os
import wx
#from pyomxplayer import OMXPlayer
#from time import sleep

#---- Constants
STORY_DIR = '../stories'
STORY_LENGTH = 30000
STORY_FILENAME = 'story'

class Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        self.InitUI()

    def InitUI(self):

        #---- Setup Menu?

        #---- Setup Panels
        panel = wx.Panel(self)
        panel.SetBackgroundColour('black')

        pnl1 = wx.Panel(self, -1, size=(600, 900))
        pnl1.SetBackgroundColour('blue')
        
        pnl2 = wx.Panel(self)
        pnl2.SetBackgroundColour('black')
        text = wx.StaticText(pnl2, 0, "TOUCH HERE TO RECORD YOUR OWN 30 SECOND STORY!", style=wx.ALIGN_CENTER)
        text.SetForegroundColour('red')
        text.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(text, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        pnl2.SetSizer(vbox)
        
        self.StartLoop()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pnl1, flag=wx.EXPAND | wx.ALL)
        sizer.Add(pnl2, proportion=1, flag=wx.EXPAND | wx.ALL)
        
        self.SetSizer(sizer)
        panel.Layout()

    def StartLoop(self):
        #---- Video Loop
        files = os.listdir(STORY_DIR)

        #loop through videos
        #player = OMXPlayer()     

class App(wx.App):
    def OnInit(self):

        #---- Setup Frame
        frame = Frame(None, "Storybox")
        self.SetTopWindow(frame)
        frame.Maximize()
        frame.ShowFullScreen(True)
        return True

storybox = App(redirect=True)
storybox.MainLoop()
