from psychopy import visual, core, event, monitors, tools, prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound
import collections, pylink, os, numpy
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy 

def display_event(event_text, key_list, tracker, monitor):
    tracker.sendMessage("!V CLEAR 0 0 0 ")	
	
    pos = collections.defaultdict(dict)
    pos[1][1] = (0, 0)
    pos[2][1] = (-0.5, 0)
    pos[2][2] = (0.5, 0)
    pos[4][1] = (-0.5, 0.5)
    pos[4][2] = (0.5, 0.5)
    pos[4][3] = (-0.5, -0.5)
    pos[4][4] = (0.5, -0.5)

    if '.jpg' in event_text or '.jpeg' in event_text:
        
        pictures = event_text.split(' ')
        pic = {}
        for i in range(len(pictures)):
            pic[i] = visual.ImageStim(win, image = 'img/'+ pictures[i], size = [0.8, 0.8], pos = pos[len(pictures)][i+1])
            pic[i].draw()
			
            tracker.sendMessage("!V IMGLOAD CENTER ./img/%s %d %d %d %d" %(pictures[i], (win.size[0]/2) + ((win.size[0]/2)*pos[len(pictures)][i+1][0]), (win.size[1]/2)+((win.size[1]/2)*pos[len(pictures)][i+1][1]), int(win.size[0]/2*0.8), int(win.size[1]/2*0.8) ))
            
            tracker.sendMessage("!V IAREA RECTANGLE %d %d %d %d %d %s" %(int(i), (win.size[0]/2) + ((win.size[0]/2)*pos[len(pictures)][i+1][0])-int((win.size[0]/2*0.8)/2), (win.size[1]/2)+((win.size[1]/2)*pos[len(pictures)][i+1][1])- int((win.size[1]/2*0.8)/2),(win.size[0]/2) + ((win.size[0]/2)*pos[len(pictures)][i+1][0]) + int((win.size[0]/2*0.8)/2), (win.size[1]/2)+((win.size[1]/2)*pos[len(pictures)][i+1][1])+ int((win.size[1]/2*0.8)/2), pictures[i] ))
            tracker.sendMessage("!V TRIAL_VAR Picture%d %s" %(i, str(pictures[i])))
    else:
        texts = event_text.split(' ')
        words = {}
        for i in range(len(texts)):
            words[i] = visual.TextStim(win, text=texts[i],
                                height=0.8,
                                pos=pos[len(texts)][i+1],
                                color='pink',
                                bold=False,
                                italic=False)
            words[i].draw()
            tracker.sendMessage("!V IAREA RECTANGLE 1%d %d %d %d %d %s" %(int(i),(win.size[0]/2) + ((win.size[0]/2)*pos[len(texts)][i+1][0])-int((win.size[0]/2*0.8)/2),(win.size[1]/2) + ((win.size[1]/2)*pos[len(texts)][i+1][1])-int((win.size[1]/2*0.8)/2), (win.size[0]/2) + ((win.size[0]/2)*pos[len(texts)][i+1][0])+int((win.size[0]/2*0.8)/2),(win.size[1]/2) + ((win.size[1]/2)*pos[len(texts)][i+1][1])+int((win.size[1]/2*0.8)/2), str(texts[i])))
            tracker.sendMessage("!V TRIAL_VAR Words %s" %(str(texts[i])))

    win.flip()
    tracker.sendMessage("DisplayOnset_%s" %(event_text))
    
    if len(event_text.split(' ')) > 1:
        currentAudio = 'audio/sound.wav'
        audio = sound.Sound(currentAudio)
        audio.play()
        tracker.sendMessage("AudioOnset")
        core.wait(3)
        audio.stop()
        key_press = event.waitKeys(keyList=key_list)
        tracker.sendMessage("Response")
        tracker.sendMessage("!V TRIAL_VAR Response %s" %( key_press))
        tracker.sendMessage("!V TRIAL_VAR Audio %s" %(currentAudio))
        print(key_press)
    else:
        if event_text == '+':
            core.wait(1)
        else:
            core.wait(0.2)

            
def surfToList(surf):
	w=surf.get_width()
	h=surf.get_height()
	rv = []
	for y in xrange(h):
		line =[]
		for x in xrange(w):
			v = surf.get_at((x,y))
			line.append((v[0],v[1],v[2]))
		rv.append(line)
	return rv
	



def experiment(trails, tracker, monitor):
    for trail in trails:
        # log trial onset message
        tracker.sendMessage("TRIALID")

        #agc = surfToList(bgbm)
	#bitmapSave(bgbm.get_width(),bgbm.get_height(),agc,0,0,bgbm.get_width(),bgbm.get_height(),"trial"+str(trial)+".bmp", "trialimages",SV_NOREPLACE,)
	# Save a local copy of background image then transfer to host to use as gaze cursor backdrop
	#getEYELINK().bitmapSaveAndBackdrop(bgbm.get_width(),bgbm.get_height(),agc,0,0,bgbm.get_width(),bgbm.get_height(),"trial" + str(trial)+".png","trialimages",SV_NOREPLACE, 0, 0, BX_MAXCONTRAST)
	# or use bitmapBackdrop for faster transfer
	#getEYELINK().bitmapBackdrop(bgbm.get_width(),bgbm.get_height(),agc,0,0,bgbm.get_width(),bgbm.get_height(),0,0,BX_MAXCONTRAST)
        
        # record_status_message : show some info on the host PC
        #tracker.sendCommand("record_status_message '%s'"% )
        
        #Optional - start realtime mode
        pylink.beginRealTimeMode(100)
        
        # # do driftcheck
        # try:
            # error = tracker.doDriftCorrect(win.size()[0]/2,win.size()[1],1,1)
            # if error == 27: 
                # tracker.doTrackerSetup()
        # except:
            # tracker.doTrackerSetup()
            
        # start recording
        tracker.startRecording(1, 1, 1, 1)
        pylink.msecDelay(50)
            
    
        events = trail.split(';')
        for event in events:
            display_event(event, ['1','2'],tracker,monitor)
        win.flip()
    
        # disable realtime mode
        pylink.endRealTimeMode()
        pylink.msecDelay(100)		

        # stop recording on the Eyetracker	  	
        tracker.stopRecording()

        # end trial parsing	
        pylink.msecDelay(50)
        tracker.setOfflineMode()
        tracker.sendMessage('TRIAL_RESULTS 0')
	
def eyelink_prepare(tracker, win, monitor, edfFileName):
	# open an EDF (eyelink) data file; This needs to be done early, so as to record all user interactions with the tracker
	tracker.openDataFile(edfFileName)
	
	# Note here that getEYELINK() is equivalent to tk, i.e., the currently initiated EyeLink tracker instance
	tracker.sendCommand("add_file_preamble_text = PictureTest")

        # get window size
	[scnWidth, scnHeight] = win.size
	
	# open the external graphics
	genv = EyeLinkCoreGraphicsPsychoPy(tracker, win)
	pylink.openGraphicsEx(genv)

	#### STEP V: Set up the tracker ################################################################
	# set a few other frequently used tracker parameters, if needed
	# Note that getEYELINK() is equivalent to the tracker instance you created, i.e., "tk", see below
	# all eyelink control commands are included in the .INI configuration files on the host PC, in "/elcl/exe"
	# we need to put the tracker in offline mode before we change its configrations
	tracker.setOfflineMode()
	# sampling rate, 250, 500, 1000, or 2000, won't work for EyeLInk II
	tracker.sendCommand('sample_rate 500')

	# inform the tracker the resolution of the subject display
	# [see Eyelink Installation Guide, Section 8.4: Customizing Your PHYSICAL.INI Settings ]
	tracker.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

	# stamp display resolution in EDF data file for Data Viewer integration
	# [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
	tracker.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

	# specify the calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical), 
	tracker.sendCommand("calibration_type = HV5") # tk.setCalibrationType('HV9') also works, see the Pylink manual

	# data stored in data file and passed over the link (online)
	# [see Eyelink User Manual, Section 4.6: Settting File Contents]

	# Set the tracker to parse Events using "GAZE" (or "HREF") data
	tracker.sendCommand("recording_parse_type = GAZE")

	# Online parser configuration: 0-> standard/coginitve, 1-> sensitive/psychophysiological
	# the Parser for EyeLink I is more conservative, see below
	# [see Eyelink User Manual, Section 4.3: EyeLink Parser Configuration]
	tracker.sendCommand('select_parser_configuration 0')

	# specify the EVENT and SAMPLE data that are stored in EDF or retrievable from the Link
	# See Section 4 Data Files of the EyeLink user manual
	tracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
	tracker.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
	tracker.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
	tracker.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
	
	# Perform camera setup
	tracker.doTrackerSetup()
	
def EyeLinkClose(tracker,edfFileName):
	#close EDF data File
	tracker.closeDataFile()
	
	#EyeLink - copy EDF file to Display PC and put it in the 'edfData' folder
	edfTransfer = visual.TextStim(win, text='Gaze data is transfering from EyeLink Host PC, please wait...', color='white')
	edfTransfer.draw()
	win.flip()
	tracker.receiveDataFile(edfFileName, edfFileName)

	#EyeLink - Close connection to tracker
	tracker.close()

if __name__=="__main__":
    trails = ['+;&;dog.jpg cat.jpeg','+;&;dog.jpg shoes.jpg','+;&;cat.jpeg monkey.jpg','+;&;cat.jpeg mouse.jpeg']
    #Open a connection to the tracker
    DummyMode = False
    
    if DummyMode == True:
        tk = pylink.EyeLink(None)
    else:
        tk = pylink.EyeLink('100.1.1.1')
    # Enter subject name
    edfFileName = 'test.edf'
    # set monitor
    mon = monitors.Monitor('myMon', width=33.7, distance=60.0)
    # define window
    win = visual.Window(size = (1000,600), color = (-1,-1,-1), monitor=mon, fullscr = True )
    print win.size
    #set monitor pixel dimensions
    mon.setSizePix((win.size[0], win.size[1]))
    # set up tracker
    eyelink_prepare(tk, win, mon, edfFileName)
	
    # Run Experiment
    experiment(trails,tk,mon)
	
    # Close down the tracker
    EyeLinkClose(tk,edfFileName)
    win.close()
