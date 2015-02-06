#!/usr/bin/env python

#=======================================
# StoryBox
# Version: .1
# by Jessica Oros
#=======================================

import os, wx, threading
from subprocess import call, check_output

#-Settings-#
STORY_DIR = '../stories/'
STORY_FILENAME = 'story'
STORY_LENGTH = 60
PLAYER_WINDOW = '0 100 1280 720'
CAMERA_WINDOW = '0,0,1280,720'
CAMERA_VFLIP = True
CAMERA_HFLIP = False
ALSA_DEVICE = '1,0'
DEBUG = False

RPANEL = 101
LPANEL = 102
PPANEL = 103

class LoopPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('black')
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour('black')
        panel2 = wx.Panel(self, wx.ID_ANY)
        panel2.SetBackgroundColour('black')
        record = wx.Button(panel2, wx.ID_ANY, label="Touch here to add your own story!", name='rpanel')
        record.SetForegroundColour('white')
        record.SetBackgroundColour('#28024f')
        record.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        record.Bind(wx.EVT_BUTTON, parent.SwitchPanel)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddStretchSpacer(3)
        vbox.Add(record, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        panel.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, flag=wx.EXPAND)
        sizer.Add(panel2, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)

class RecordPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('black')
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour('black')
        panel2 = wx.Panel(self, wx.ID_ANY)
        panel2.SetBackgroundColour('black')
        record = wx.Button(panel2, wx.ID_ANY, label="Start Recording", name="lpanel")
        record.SetForegroundColour('white')
        record.SetBackgroundColour('#0072bb')
        record.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        record.Bind(wx.EVT_BUTTON, self.ToggleRecord)
        cancel = wx.Button(panel2, wx.ID_ANY, label="Cancel", name="lpanel")
        cancel.SetForegroundColour('white')
        cancel.SetBackgroundColour('#c5383e')
        cancel.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        cancel.Bind(wx.EVT_BUTTON, parent.SwitchPanel)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(record, 1, wx.EXPAND)
        hbox.Add(cancel, 1, wx.EXPAND)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddStretchSpacer(3)
        vbox.Add(hbox, 1, wx.EXPAND)
        panel.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        sizer.Add(panel2, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def ToggleRecord(self, e):
        global recording
        btn = e.GetEventObject()
        if not recording:
            wx.GetApp().StartRecording()
            btn.SetBackgroundColour('#932e72')
            btn.SetLabel('Stop Recording')
        else:
            wx.GetApp().StopRecording()
            btn.SetBackgroundColour('#0072bb')
            btn.SetLabel('Start Recording')
            self.GetParent().SwitchPanel(None, 'ppanel')

class PreviewPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('black')
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour('black')
        panel2 = wx.Panel(self, wx.ID_ANY)
        panel2.SetBackgroundColour('black')
        save = wx.Button(panel2, wx.ID_ANY, label="Save", name="lpanel")
        redo = wx.Button(panel2, wx.ID_ANY, label="Redo", name="rpanel")
        cancel = wx.Button(panel2, wx.ID_ANY, label="Cancel", name="lpanel")
        cancel.SetForegroundColour('white')
        cancel.SetBackgroundColour('#c5383e')
        cancel.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        cancel.Bind(wx.EVT_BUTTON, parent.SwitchPanel)
        save.SetForegroundColour('white')
        save.SetBackgroundColour('green')
        save.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        save.Bind(wx.EVT_BUTTON, wx.GetApp().SaveVideo)
        redo.SetForegroundColour('white')
        redo.SetBackgroundColour('#0072bb')
        redo.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        redo.Bind(wx.EVT_BUTTON, parent.SwitchPanel)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(save, 1, wx.EXPAND)
        hbox.Add(redo, 1, wx.EXPAND)
        hbox.Add(cancel, 1, wx.EXPAND)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddStretchSpacer(3)
        vbox.Add(hbox, 1, wx.EXPAND)

        panel.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        sizer.Add(panel2, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
class SBFrame(wx.Frame):

    def __init__(self, parent, title):

        global storybox;
        storybox = wx.GetApp()

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
        self.Bind(wx.EVT_MENU, storybox.CleanUp, cleanup)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    def HidePanels(self):
        self.lpanel.Hide()
        self.ppanel.Hide()
        self.rpanel.Hide()
        
    def SwitchPanel(self, e=None, panel=""):
        self.HidePanels()

        if not panel:
            #switching from menu
            panel = e.GetId()
            if panel is RPANEL:
                panel = 'rpanel'
            elif panel is LPANEL:
                panel = 'lpanel'
            elif panel is PPANEL:
                panel = 'ppanel'
            else:
                #switching from button
                btn = e.GetEventObject()
                panel = btn.GetName()

        if panel == 'rpanel':
            wx.GetApp().RecordPanel()
        if panel == 'lpanel':
            wx.GetApp().LoopPanel()
        if panel == 'ppanel':
            wx.GetApp().PreviewPanel()

        self.Layout()

class StoryBox(wx.App):
    def OnInit(self):
        self.frame = SBFrame(None, "Storybox")
        self.SetTopWindow(self.frame)
        self.frame.Maximize()
        if not DEBUG:
            self.frame.ShowFullScreen(True)
        else:
            self.frame.Show(True)

        #init LoopPanel
        self.frame.HidePanels()
        self.LoopPanel()

        global encoding
        encoding = 0

        return True;

    def LoopVideos(self):
        global looping
        looping = True
        while looping:
            files = os.listdir(STORY_DIR)
            for file in files:
                call('omxplayer --win "' + PLAYER_WINDOW + '" ' + str(STORY_DIR) + str(file), shell=True)
                if not looping:
                    break

    def PreviewCamera(self):
        picam = 'picam --alsadev hw:' + ALSA_DEVICE + ' --previewrect ' + CAMERA_WINDOW
        if CAMERA_HFLIP:
            picam += ' --hflip'
        if CAMERA_VFLIP:
            picam += ' --vflip'
        call(picam, shell=True)

    def StartRecording(self):
        global recording
        open('hooks/start_record', 'w')
        recording = True

    def StopRecording(self):
        global recording
        open('hooks/stop_record', 'w')
        recording = False
        self.frame.SwitchPanel(None, 'ppanel')

    def PreviewVideo(self):
        global previewing
        previewing = True
        while previewing:
            call('omxplayer --win "' + PLAYER_WINDOW + '" rec/archive/*.ts', shell=True)
            if not previewing:
                break

    def SaveVideo(self, e):
        global encoding
        ffmpeg = threading.Thread(target=self.EncodeVideo)
        ffmpeg.start()
        ffmpeg.join()
        self.frame.SwitchPanel(e)

    def EncodeVideo(self):
        global encoding
        encoding += 1
        files = os.listdir(STORY_DIR)
        new_story = STORY_DIR + STORY_FILENAME + str(len(files)+1) + '.mp4'
        call('ffmpeg -i rec/archive/*.ts -c:v copy -c:a copy -bsf:a aac_adtstoasc ' + new_story, shell=True)
        encoding -= 1
        
    def LoopPanel(self):
        self.CleanUp()
        self.DeleteTempFiles()
        self.frame.lpanel.Show()
        #start video loop
        loop = threading.Thread(target=self.LoopVideos)
        loop.start()

    def RecordPanel(self):
        self.CleanUp()
        self.DeleteTempFiles()
        self.frame.rpanel.Show()
        #start camera
        camera = threading.Thread(target=self.PreviewCamera)
        camera.start()
            
    def PreviewPanel(self):
        self.CleanUp()
        self.frame.ppanel.Show()
        #preview video
        preview = threading.Thread(target=self.PreviewVideo)
        preview.start()

    def CleanUp(self, e=None):
        global looping, recording, previewing
        previewing = False
        looping = False
        recording = False
        pkill = call('pkill omxplayer', shell=True)
        pkill = call('pkill picam', shell=True)

    def DeleteTempFiles(self):
        call('rm -rf hooks state rec', shell=True)
    
if __name__ == '__main__':
    sb = StoryBox()
    sb.MainLoop()
