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

#---- Settings
STORY_DIR = '../stories/'
STORY_FILENAME = 'story'
STORY_LENGTH = 60
START_FULL_SCREEN = False
VIDEO_HEIGHT = 900
VIDEO_WIDTH = 1400
HIDE_TOGGLE = False

#---- Menu Constants
RPANEL = 101
LPANEL = 102
PPANEL = 103

#---- Classes

class LoopPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('black')
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour('black')
        record = wx.Button(panel, wx.ID_ANY, label="TOUCH HERE TO RECORD YOUR OWN " + str(STORY_LENGTH) + " SECOND STORY!", style=wx.ALIGN_CENTER, name='record_panel')
        record.SetForegroundColour('white')
        record.SetBackgroundColour('black')
        record.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        #record.Bind(wx.EVT_BUTTON, self.SwitchPanel)
        startStop = wx.ToggleButton(panel, wx.ID_ANY, label='Start')
        startStop.SetBackgroundColour('purple')
        startStop.SetForegroundColour('white')
        startStop.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        #startStop.Bind(wx.EVT_TOGGLEBUTTON, self.StoryLoop)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(record, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(startStop, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        panel.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

class RecordPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        #self.SetBackgroundColour('black')
        panel = wx.Panel(self, wx.ID_ANY, size=(600,900))
        panel.SetBackgroundColour('black')
        panel2 = wx.Panel(self, wx.ID_ANY)
        panel2.SetBackgroundColour('black')
        clock = wx.StaticText(panel, wx.ID_ANY, ":" + str(STORY_LENGTH), style=wx.ALIGN_CENTER, size=(400,400))
        clock.SetForegroundColour('#CCAA00')
        clock.SetBackgroundColour('#CCCCCC')
        clock.SetFont(wx.Font(100, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        record = wx.Button(panel2, wx.ID_ANY, label="START RECORDING", style=wx.ALIGN_LEFT, size=(800,100))
        record.SetForegroundColour('white')
        record.SetBackgroundColour('red')
        record.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        #record.Bind(wx.EVT_BUTTON, self.RecordVideo)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(clock, flag=wx.ALIGN_RIGHT)
        vbox.Add(record, flag=wx.ALIGN_CENTER_HORIZONTAL)
        panel.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, flag=wx.EXPAND | wx.ALL)
        sizer.Add(panel2, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

class PreviewPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('black')
        
class SBFrame(wx.Frame):

    def __init__(self, parent, title):

        #setup panels
        wx.Frame.__init__(self, None, wx.ID_ANY, "Storybox")
        self.lpanel = LoopPanel(self)
        self.rpanel = RecordPanel(self)
        self.ppanel = PreviewPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.lpanel, 1, wx.EXPAND)
        self.sizer.Add(self.rpanel, 1, wx.EXPAND)
        self.sizer.Add(self.ppanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        #setup menus
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_to_rpanel = fileMenu.Append(RPANEL, "Switch to &Record Panel")
        switch_to_ppanel = fileMenu.Append(PPANEL, "Switch to &Preview Panel")
        switch_to_lpanel = fileMenu.Append(LPANEL, "Switch to &Loop Panel")
        cleanup = fileMenu.Append(wx.ID_ANY, "Cleanup (kill processes)")
        self.Bind(wx.EVT_MENU, self.SwitchPanel, switch_to_rpanel)
        self.Bind(wx.EVT_MENU, self.SwitchPanel, switch_to_lpanel)
        self.Bind(wx.EVT_MENU, self.SwitchPanel, switch_to_ppanel)
        self.Bind(wx.EVT_MENU, self.CleanUp, cleanup)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
    def SwitchPanel(self, e):
        storybox = wx.GetApp()
        
        #hide panels
        self.lpanel.Hide()
        self.ppanel.Hide()
        self.rpanel.Hide()
        
        #switching from menu
        panel = e.GetId()
        if panel is RPANEL:
            #self.rpanel.Show()
            storybox.RecordPanel()
        elif panel is LPANEL:
            #self.lpanel.Show()
            storybox.LoopPanel()
        elif panel is PPANEL:
            self.ppanel.Show()
        else:
            #switching from button
            btn = e.GetEventObject()
            panel = e.GetName()
            if panel is rpanel:
                self.rpanel.Show()
            if panel is lpanel:
                self.lpanel.Show()
            if panel is ppanel:
                self.ppanel.Show()

        self.Layout()

    def StoryLoop(self, e):
        obj = e.GetEventObject()
        obj.Hide()
        print(obj)
        isPressed = obj.GetValue()
        if(isPressed):
            if(HIDE_TOGGLE):
                obj.Hide()
            print(obj)
            obj.SetLabel('Stop')
            obj.SetBackgroundColour('red')

            files = os.listdir(STORY_DIR)
            for file in files:
                while(isPressed):
                    isPressed = obj.GetValue()
                    if(isPressed):
                        #omx = Popen(['omxplayer','--win','200 0 1700 900', STORY_DIR + file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                        omx = Popen(['omxplayer','--win','0 0 100 100', STORY_DIR + file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                        sleep(10)
                    else:
                        break

    #def Record(self, e):

    def RecordVideo(self, e):
        obj = e.GetEventObject()
        print(obj)
        
    #def CountDown(self):
        #self.timer.Bind(wx.EVT_TIMER, self.update, self.timer)
        #TODO countdown

    #def update(self, event):
        #TODO update

    def CleanUp(self, e):
        pkill = Popen(['pkill', 'omxplayer,picam'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        pkill.wait()

class StoryBox(wx.App):
    def OnInit(self):
        self.frame = SBFrame(None, "Storybox")
        self.SetTopWindow(self.frame)
        self.frame.Maximize()
        if START_FULL_SCREEN:
            self.frame.ShowFullScreen(True)
        else:
            self.frame.Show(True)
            
        return True;

    def RecordPanel(self):
        print('record panel')

    def LoopPanel(self):
        self.frame.lpanel.Show()
        #start video loop
        files = os.listdir(STORY_DIR)
        for file in files:
            #omx = Popen(['omxplayer','--win','200 0 1700 900', STORY_DIR + file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            omx = Popen(['omxplayer','--win','0 0 100 100', STORY_DIR + file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            omx.communicate()
            
    def PreviewPanel(self):
        print('preview panel')
    
#---- Main
if __name__ == '__main__':
    sb = StoryBox()
    sb.MainLoop()
