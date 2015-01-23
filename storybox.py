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
START_FULL_SCREEN = True
VIDEO_HEIGHT = 900
VIDEO_WIDTH = 1400
HIDE_TOGGLE = True

#---- Classes
class SBFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, wx.ID_ANY)
        self.InitUI()

    def InitUI(self):
        #---- Setup Menu
        #TODO setup menus

        timer = wx.Timer(self)
        looping = False

        #---- Setup Panels
        lpanel = wx.Panel(self, wx.ID_ANY)
        lpanel.SetBackgroundColour('black')
        pnl1 = wx.Panel(self, wx.ID_ANY, size=(600, 900))
        pnl1.SetBackgroundColour('black')
        pnl2 = wx.Panel(self, wx.ID_ANY)
        pnl2.SetBackgroundColour('black')
        record = wx.Button(pnl2, wx.ID_ANY, label="TOUCH HERE TO RECORD YOUR OWN " + str(STORY_LENGTH) + " SECOND STORY!", style=wx.ALIGN_CENTER)
        record.SetForegroundColour('white')
        record.SetBackgroundColour('black')
        record.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        #record.Bind(wx.EVT_BUTTON, self.SwitchPanel)
        startStop = wx.ToggleButton(pnl2, -1, label='Start')
        startStop.SetBackgroundColour('purple')
        startStop.SetForegroundColour('white')
        startStop.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        startStop.Bind(wx.EVT_TOGGLEBUTTON, self.StoryLoop)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(record, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(startStop, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        pnl2.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pnl1, flag=wx.EXPAND | wx.ALL)
        sizer.Add(pnl2, proportion=1, flag=wx.EXPAND | wx.ALL)
        #init lpanel
        #self.SetSizer(sizer)
        #lpanel.Layout()

        rpanel = wx.Panel(self, wx.ID_ANY)
        rpanel.SetBackgroundColour('black')
        pnl3 = wx.Panel(self, wx.ID_ANY, size=(600,900))
        pnl3.SetBackgroundColour('black')
        pnl4 = wx.Panel(self, wx.ID_ANY)
        pnl4.SetBackgroundColour('black')
        clock = wx.StaticText(pnl3, wx.ID_ANY, ":" + str(STORY_LENGTH), style=wx.ALIGN_CENTER, size=(400,400))
        clock.SetForegroundColour('#CCAA00')
        clock.SetBackgroundColour('#CCCCCC')
        clock.SetFont(wx.Font(100, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        record2 = wx.Button(pnl4, wx.ID_ANY, label="START RECORDING", style=wx.ALIGN_LEFT, size=(800,100))
        record2.SetForegroundColour('white')
        record2.SetBackgroundColour('red')
        record2.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        #record2.Bind(wx.EVT_BUTTON, self.RecordVideo)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(clock, flag=wx.ALIGN_RIGHT)
        vbox2.Add(record2, flag=wx.ALIGN_CENTER_HORIZONTAL)
        pnl3.SetSizer(vbox2)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(pnl3, flag=wx.EXPAND | wx.ALL)
        sizer2.Add(pnl4, flag=wx.EXPAND | wx.ALL)
        #init rpanel
        self.SetSizer(sizer2)
        rpanel.Layout()

    #def SwitchPanel(self, e):
        #TODO switchpanel

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
        
            
    #def CountDown(self):
        #self.timer.Bind(wx.EVT_TIMER, self.update, self.timer)
        #TODO countdown

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
