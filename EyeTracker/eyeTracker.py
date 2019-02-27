from psychopy import visual, core, event, monitors, tools, prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound
import pandas as pd
import collections, pylink, os, numpy, csv, random
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy 

"""
global variables
"""
TIME_OUT = 1000
FILE_NAME = ''
EXPNAME = ''
SUBJECTID = ''
ITEM_LIST = ''
CONDITION = ''
FEEDBACK = False
RAND_BLOCKS = True
RAND_WITHIN_BLOCKS = True

INSTRUCTION = True
INSTRUCTION_TEXT_HEIGHT = 0.1
INSTRUCTION_FONT = 'Arial'
INSTRUCTION_TEXT_COLOR = 'white'


def display_instruction_words(instruction_text):
    """
    Get one line from the instruction text and display
    Wait 'space' to continue
    """
    words = visual.TextStim(win, text=instruction_text.replace(r'\n', '\n'),
                            height=INSTRUCTION_TEXT_HEIGHT,
                            pos=(0.0, 0.0),
                            color=INSTRUCTION_TEXT_COLOR,
                            bold=False,
                            italic=False)
    words.draw()
    win.flip()
    key_press = event.waitKeys(keyList=['space'])


def display_event(event_text, duration, key_list, tracker, monitor):
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
        n = len(pictures)-1
        pic = {}
        for i in range(n):
            pic[i] = visual.ImageStim(win, image = 'Stimuli/Images/'+ pictures[i], size = [0.8, 0.8], pos = pos[n][i+1])
            pic[i].draw()

            tracker.sendMessage("!V IMGLOAD CENTER ./Stimuli/Images/%s %d %d %d %d" %(pictures[i], (win.size[0]/2) + ((win.size[0]/2)*pos[n][i+1][0]), (win.size[1]/2)+((win.size[1]/2)*pos[n][i+1][1]), int(win.size[0]/2*0.8), int(win.size[1]/2*0.8) ))
            
            tracker.sendMessage("!V IAREA RECTANGLE %d %d %d %d %d %s" %(int(i), (win.size[0]/2) + ((win.size[0]/2)*pos[n][i+1][0])-int((win.size[0]/2*0.8)/2), (win.size[1]/2)+((win.size[1]/2)*pos[n][i+1][1])- int((win.size[1]/2*0.8)/2),(win.size[0]/2) + ((win.size[0]/2)*pos[n][i+1][0]) + int((win.size[0]/2*0.8)/2), (win.size[1]/2)+((win.size[1]/2)*pos[n][i+1][1])+ int((win.size[1]/2*0.8)/2), pictures[i] ))
            tracker.sendMessage("!V TRIAL_VAR Picture%d %s" %(i, str(pictures[i])))
    else:
        texts = event_text.split(' ')
        n = len(texts)
        words = {}
        for i in range(n):
            words[i] = visual.TextStim(win, text=texts[i],
                                height=0.8,
                                pos=pos[n][i+1],
                                color='pink',
                                bold=False,
                                italic=False)
            words[i].draw()
            tracker.sendMessage("!V IAREA RECTANGLE 1%d %d %d %d %d %s" %(int(i),(win.size[0]/2) + ((win.size[0]/2)*pos[n][i+1][0])-int((win.size[0]/2*0.8)/2),(win.size[1]/2) + ((win.size[1]/2)*pos[n][i+1][1])-int((win.size[1]/2*0.8)/2), (win.size[0]/2) + ((win.size[0]/2)*pos[n][i+1][0])+int((win.size[0]/2*0.8)/2),(win.size[1]/2) + ((win.size[1]/2)*pos[n][i+1][1])+int((win.size[1]/2*0.8)/2), str(texts[i])))
            tracker.sendMessage("!V TRIAL_VAR Words %s" %(str(texts[i])))

    win.flip()
    tracker.sendMessage("DisplayOnset_%s" %(event_text))
    
    if len(event_text.split(' ')) > 1:
        currentAudio = 'Stimuli/Audio/' + event_text.split(' ')[-1]
        audio = sound.Sound(currentAudio)
        audio.play()
        tracker.sendMessage("AudioOnset")
        core.wait(5)
        #core.wait(audio.getDuration())
        audio.stop()
        if key_press is not None:
            key_press = event.waitKeys(keyList=key_list,maxWait=TIME_OUT)
            tracker.sendMessage("Response")
            tracker.sendMessage("!V TRIAL_VAR Response %s" %( key_press))
            tracker.sendMessage("!V TRIAL_VAR Audio %s" %(currentAudio))
            print(key_press)
    else:
        core.wait(duration)

            
# def surfToList(surf):
# 	w=surf.get_width()
# 	h=surf.get_height()
# 	rv = []
# 	for y in xrange(h):
# 		line =[]
# 		for x in xrange(w):
# 			v = surf.get_at((x,y))
# 			line.append((v[0],v[1],v[2]))
# 		rv.append(line)
# 	return rv


"""
Preparation Part
"""


def load_dict(dict_file):
    res_dict = {}
    f = open(dict_file)
    for line in f:
        data = (line.strip('\n')).split(',')
        try:
            res_dict[data[0]] = data[1]
        except:
            print('ERROR in' + dict_file + 'in Row {}'.format(data))
            sys.exit(2)
    return res_dict


def show_instructions(filePathName, name=None):
    """
    Display the main instructions and block instructions
    For block instructions, display the text according to the block name
    """
    if name == None:
        with open(filePathName) as fp:
            introduction = fp.readlines()
        for i in range(len(introduction)):
            display_instruction_words(introduction[i])
    else:
        res_dict = {}
        file = open(filePathName)
        for line in file:
            data = (line.strip('\n')).split('#')
            res_dict[data[0]] = data[1]
        display_instruction_words(res_dict[name])


def load_trail_events(trail_event_file):
    trail_event_list = []
    f = open(trail_event_file)
    for line in f:
        data = (line.strip('\n')).split(',')
        trail_event_list.append(data)
    return trail_event_list


def load_data(filePath):
    data = pd.read_csv(filePath, header=0, skip_blank_lines=True)
    return data


def verify_items_and_events(item_data, trail_event_list):
    """
    Check whether all events are include in item list
    """
    item_data_list = item_data.columns.values.tolist()
    for i in range(len(trail_event_list)):
        if trail_event_list[i][0] not in item_data_list:
            if trail_event_list[i][0] != 'ITI':
                return False
    return True


def prepare_pairs(item_data, config_dict):
    """
    This function randomize the order of item_data and return the list of item data for practice
    and each block
    A list of things done:
    1. check whether it has a feedback column, if there is, show image or display sound when the 
    answer is wrong
    2. when num_blocks is positive, there are only PRACTICE and TEST, 
    and all PRACTICE are list before TEST in csv file, and here random assign TEST to blocks;
    when num_blocks is negative, there are other Block_Name than PRACTICE and TEST, assign data to block
    according to the block_name, and shuffle the data in each block. The display order of block is same as
    the NAME_SET in config file, and always put PRACTICE first.
    """

    num_blocks = int(config_dict['BLOCKS'])
    name_set = config_dict['NAME_SET'].split(' ')
    num_items = len(item_data)
    
    # for situation with only PRACTICE and TEST
    if num_blocks > 0:
        block_list = []
        current_block = 1
        count = 0; # count the number of practice pairs
        # Assign the block number
        for i in range(num_items):
            if item_data.loc[i, "Block_Name"] == 'PRACTICE':
                count += 1
                block_list.append(0)
                continue
            block_list.append(current_block)
            if current_block < num_blocks:
                current_block += 1
            else:
                current_block = 1
        if RAND_BLOCKS == True:
            block_list_copy = block_list[count:]
            # shuffle the list of block numbers
            random.shuffle(block_list_copy)
            block_list[count:] = block_list_copy

        # assign the block number to "Block" column
        for i in range(len(item_data)):
            item_data.loc[i, "Block"] = block_list[i]

        # get the practice list
        practice_list = item_data[item_data["Block"] == 0]
        practice_list = practice_list.reset_index()

        # assign the pairs into each block according to the "Block" value
        trail_block_list = []
        for i in range(num_blocks):
            block_dataframe = item_data[item_data["Block"] == i + 1]
            if RAND_WITHIN_BLOCKS == True:
                # shuffle within the block
                block_dataframe = block_dataframe.sample(frac=1)
            trail_block_list.append(block_dataframe.reset_index())

        return item_data, trail_block_list, practice_list
    # for situations with other than TEST
    else:
        for i in range(num_items):
            block_name = item_data.loc[i, "Block_Name"]
            item_data.loc[i, "Block"] = name_set.index(block_name)

        practice_list = item_data[item_data["Block_Name"] == 'PRACTICE']
        practice_list = practice_list.reset_index()

        trail_block_list = []
        # assign pairs to block according to their "Block_Name" value
        for i in range(1, len(name_set)):
            block_dataframe = item_data[item_data["Block"] == i]
            if RAND_WITHIN_BLOCKS == True:
                block_dataframe = block_dataframe.sample(frac=1)
            trail_block_list.append(block_dataframe.reset_index())
        return item_data, trail_block_list, practice_list


def experiment(assigned_item_data, trail_block_list, trail_event_list, config_dict, practice_list, tracker, monitor):
    
    num_blocks = int(config_dict['BLOCKS'])
    if INSTRUCTION:
        show_instructions('Stimuli/Instructions/main_instructions.txt')
    name_flag = False
    # When there are PRACTICE pairs
    if len(practice_list) > 0:
        if INSTRUCTION:
            show_instructions('Stimuli/Instructions/practice_instructions.txt')
        block(practice_list, trail_event_list, 0, config_dict, tracker, monitor)
    # When there are other "Block_Name" than TEST, get the number of block according to 
    # the NAME_SET
    if num_blocks < 0:
        num_blocks = len(config_dict['NAME_SET'].split(' ')) - 1
        name_flag = True
    for i in range(1, num_blocks + 1):
        if name_flag:
            block_name = config_dict['NAME_SET'].split(' ')[i]
        else:
            block_name = 'TEST'
        if INSTRUCTION:
            show_instructions('Stimuli/Instructions/block_instructions2.txt', block_name)
        block(trail_block_list[i - 1], trail_event_list, i, config_dict, tracker, monitor)
        if i < num_blocks:
            if INSTRUCTION:
                show_instructions('Stimuli/Instructions/block_break.txt')


def block(item_data_frame, trial_event_list, block_num, config_dict, tracker, monitor):

    num_trails = len(item_data_frame)
    num_events = len(trail_event_list)
    key = config_dict['KEY']

    for i in range(num_trails):
        # log trial onset message
        tracker.sendMessage("TRIALID 0 %d" % i)


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
            
    
        for j in range(num_events):
            valid_key_list = ''
            event_name = trial_event_list[j][0]
            # if this step need a key press
            if trial_event_list[j][1] == "KEY":
                duration = 0
                valid_key_list = key.split()
            else:
                duration = float(int(trial_event_list[j][1]) / 1000)
            # break between pairs
            if event_name == 'ITI':
                core.wait(duration)
            else:
                # need display the pairs
                event_text = item_data_frame.loc[i, event_name]
                if valid_key_list != '':
                    display_event(event_text, duration, valid_key_list,tracker,monitor)
                else:
                    display_event(event_text, duration, None,tracker,monitor)

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
	tracker.sendCommand("add_file_preamble_text = EyeTracker")

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

def prepare(config_dict, condition_dict):
    """
    This fuction prepare the globle varibles from information in cofig.csv and conditions.csv
    """
    global EXPNAME, TIME_OUT, ITEM_LIST, CONDITION, SUBJECTID, FILE_NAME, RAND_BLOCKS, RAND_WITHIN_BLOCKS, INSTRUCTION
    file = os.path.basename(__file__)
    # get the expriment name
    EXPNAME = os.path.splitext(file)[0]
    TIME_OUT = float(config_dict['TIMEOUT']) / 1000
    items = condition_dict['items'].split(' ')
    # get the item list in random
    ITEM_LIST = str(items[random.randint(0, len(items) - 1)])
    conditions = condition_dict['trail_events'].split(' ')
    # get the condition in random
    CONDITION = str(conditions[random.randint(0, len(conditions) - 1)])
    # randomly generate a subject id
    SUBJECTID = random.randint(10 ** 5, 10 ** 6)
    # generate the file name for output
    FILE_NAME = str(SUBJECTID)+ '.edf'
    RAND_BLOCKS = (config_dict['RAND_BLOCKS'] == 'TRUE')
    RAND_WITHIN_BLOCKS = (config_dict['RAND_WITHIN_BLOCKS'] == 'TRUE')
    INSTRUCTION = (config_dict['INSTRUCTION'] == 'TRUE')

if __name__=="__main__":
    # load the data files
    config_dict = load_dict('config.csv')
    condition_dict = load_dict('conditions.csv')
    prepare(config_dict, condition_dict)
    item_data = load_data('Stimuli/Item_Lists/' + ITEM_LIST + '.csv')
    trail_event_list = load_trail_events('Events/' + CONDITION + '.csv')

    #Open a connection to the tracker
    DummyMode = False
    
    if DummyMode == True:
        tk = pylink.EyeLink(None)
    else:
        tk = pylink.EyeLink('100.1.1.1')
    # Enter subject name
    edfFileName = FILE_NAME
    print(edfFileName)
    # set monitor
    mon = monitors.Monitor('myMon', width=33.7, distance=60.0)
    # define window
    win = visual.Window(size = (1000,600), color = (-1,-1,-1), monitor=mon, fullscr = True )

    #set monitor pixel dimensions
    mon.setSizePix((win.size[0], win.size[1]))
    # set up tracker
    eyelink_prepare(tk, win, mon, edfFileName)
	
    """
    Experiment Part
    """

    if verify_items_and_events(item_data, trail_event_list):
        assigned_item_data, trail_block_list, practice_list = prepare_pairs(item_data, config_dict)
        experiment(assigned_item_data, trail_block_list, trail_event_list, config_dict, practice_list, tk, mon)
    else:
        print('Data Error!')
	
    # Close down the tracker
    EyeLinkClose(tk,edfFileName)
    win.close()
