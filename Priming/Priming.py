from psychopy import visual, core, event, sound
import numpy as np
import pandas as pd
import csv
import random
import os
import collections

EVENT_TEXT_HEIGHT = 0.5
EVENT_TEXT_FONT = 'Arial'
EVENT_TEXT_COLOR = 'pink'

INSTRUCTION_TEXT_HEIGHT = 0.1
INSTRUCTION_FONT = 'Arial'
INSTRUCTION_TEXT_COLOR = 'white'

TIME_OUT = 1000
FILE_NAME = ''
EXPNAME = ''
SUBJECTID = ''
ITEM_LIST = ''
CONDITION = ''
FEEDBACK = False
RAND_BLOCKS = True
RAND_WITHIN_BLOCKS = True

win = visual.Window(size=(1000, 600), color=(-1, -1, -1), fullscr=False)


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


def display_event_words(event_text, duration, key_list, type):
    """
    When type equals to 'N', all display events will display the time as the input duration
    when movie and music longer than that duration, just cut it
    when movie and music shorter than that time, then wait after they end;
    When type equals to 'W', image and text still display for duration time,
    for movie and music, wait a duration time after they end.
    """
    pos = collections.defaultdict(dict)
    pos[1][1] = (0, 0)
    pos[2][1] = (-0.5, 0)
    pos[2][2] = (0.5, 0)
    pos[4][1] = (-0.5, 0.5)
    pos[4][2] = (0.5, 0.5)
    pos[4][3] = (-0.5, -0.5)
    pos[4][4] = (0.5, -0.5)
    
    timer = core.Clock()
    timer.reset()
    win.flip()
    if '.jpg' in event_text and '.wav' in event_text:
        cur_events = event_text.split(' ')
        pic = {}
        for i in range(len(cur_events)-1):
            pic[i] = visual.ImageStim(win, image = 'Stimuli/Images/'+ cur_events[i], size = [0.8, 0.8], pos = pos[len(cur_events)-1][i+1])
            pic[i].draw()
        win.flip()
        audio = sound.Sound('Stimuli/Audio/' + cur_events[-1])
        audio.play()
        core.wait(duration)
        audio.stop()
    elif '.jpg' in event_text:
        pictures = event_text.split(' ')
        pic = {}
        for i in range(len(pictures)):
            pic[i] = visual.ImageStim(win, image = 'Stimuli/Images/'+ pictures[i], size = [0.8, 0.8], pos = pos[len(pictures)][i+1])
            pic[i].draw()
        win.flip()
        core.wait(duration)
    elif '.avi' in event_text:
        mov = visual.MovieStim3(win, 'Stimuli/Video/' + event_text, noAudio=False)
        if type == 'N':
            while mov.status != visual.FINISHED:
                mov.draw()
                win.flip()
                if timer.getTime() >= duration:
                    mov.status = visual.FINISHED
            used_time = timer.getTime()
            if duration - used_time > 0:
                core.wait(duration - used_time)
        elif type == 'W':
            while mov.status != visual.FINISHED:
                mov.draw()
                win.flip()
            core.wait(duration)
    elif '.wav' in event_text:
        audio = sound.Sound('Stimuli/Audio/' + event_text)
        audio.play()
        if type == 'N':
            core.wait(10)
            audio.stop()
        elif type == 'W':
            # core.wait(audio.getDuration())
            core.wait(10)
            core.wait(duration)
            audio.stop()
    else:
        texts = event_text.split(' ')
        words = {}
        for i in range(len(texts)):
            words[i] = visual.TextStim(win, text=texts[i],
                                height=EVENT_TEXT_HEIGHT,
                                pos=pos[len(texts)][i+1],
                                color=EVENT_TEXT_COLOR,
                                bold=False,
                                italic=False)
            words[i].draw()
        win.flip()
        core.wait(duration)
    """
    When key_list is None, only return the time for display the event
    Else return the time of display, key_press, and the time wait until get a keypress
    """
    if key_list is None:
        timeUse = timer.getTime()
        return round(timeUse * 1000, 4)
    else:
        timeUse_display = timer.getTime()
        timer.reset()
        # wait for the keypress
        key_press = event.waitKeys(keyList=key_list, maxWait=TIME_OUT)
        if key_press == None:
            # get the time uesed for reaction
            timeUse_action = timer.getTime()
            return round(timeUse_display * 1000, 4), 'null', round(timeUse_action * 1000, 4)
        timeUse_action = timer.getTime()
        return round(timeUse_display * 1000, 4), key_press[0], round(timeUse_action * 1000, 4)


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


def load_trial_events(trial_event_file):
    trial_event_list = []
    f = open(trial_event_file)
    for line in f:
        data = (line.strip('\n')).split(',')
        trial_event_list.append(data)
    return trial_event_list


def load_data(filePath):
    data = pd.read_csv(filePath, header=0, skip_blank_lines=True)
    return data


def verify_items_and_events(item_data, trial_event_list):
    """
    Check whether all events are include in item list
    """
    item_data_list = item_data.columns.values.tolist()
    for i in range(len(trial_event_list)):
        if trial_event_list[i][0] not in item_data_list:
            if trial_event_list[i][0] != 'ITI':
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
    global FEEDBACK
    if 'Feedback' in item_data.columns.values.tolist():
        FEEDBACK = True
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
        trial_block_list = []
        for i in range(num_blocks):
            block_dataframe = item_data[item_data["Block"] == i + 1]
            if RAND_WITHIN_BLOCKS == True:
                # shuffle within the block
                block_dataframe = block_dataframe.sample(frac=1)
                practice_list = practice_list.sample(frac=1)
            trial_block_list.append(block_dataframe.reset_index())

        practice_list = practice_list.reset_index()

        return item_data, trial_block_list, practice_list
    # for situations with other than TEST
    else:
        for i in range(num_items):
            block_name = item_data.loc[i, "Block_Name"]
            item_data.loc[i, "Block"] = name_set.index(block_name)
        practice_list = item_data[item_data["Block_Name"] == 'PRACTICE']
        practice_list = practice_list.reset_index()

        trial_block_list = []
        # assign pairs to block according to their "Block_Name" value
        for i in range(1, len(name_set)):
            block_dataframe = item_data[item_data["Block"] == i]
            if RAND_WITHIN_BLOCKS == True:
                block_dataframe = block_dataframe.sample(frac=1)
                practice_list = practice_list.sample(frac=1)

            trial_block_list.append(block_dataframe.reset_index())

        practice_list = practice_list.reset_index()

        return item_data, trial_block_list, practice_list


def prepare_output_header(assigned_item_data, trial_block_list, trial_event_list, config_dict):
    """
    prepare the header for the output file
    """
    header_row = []
    header_row.extend(('ExpName', 'SubjectID', 'Item_List', 'Condition'))
    header_row.extend(('BlockID', 'TrialID'))
    header_row.extend(assigned_item_data.columns.values.tolist()[0:-1])

    for i in range(len(trial_event_list)):
        if trial_event_list[i][0] == 'ITI':
            continue
        event_time = trial_event_list[i][0] + '_Time'
        header_row.append(event_time)

    header_row.extend(('Key_response', 'RT'))
    header_row.append('ITI_Time')

    with open('Data/' + FILE_NAME + '.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(header_row)


def experiment(assigned_item_data, trial_block_list, trial_event_list, config_dict, practice_list):
    """
    This is the experiment function
    """
    # get the number of block
    num_blocks = int(config_dict['BLOCKS'])
    show_instructions('Stimuli/Instructions/main_instructions.txt')
    prepare_output_header(assigned_item_data, trial_block_list, trial_event_list, config_dict)
    name_flag = False
    # When there are PRACTICE pairs
    if len(practice_list) > 0:
        show_instructions('Stimuli/Instructions/practice_instructions.txt')
        block(practice_list, trial_event_list, 0, config_dict)
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
        show_instructions('Stimuli/Instructions/block_instructions2.txt', block_name)
        block(trial_block_list[i - 1], trial_event_list, i, config_dict)
        if i < num_blocks:
            show_instructions('Stimuli/Instructions/block_break.txt')


def block(item_data_frame, trial_event_list, block_num, config_dict):
    """
    This function executes each trial with all events in order.
    """
    num_trials = len(item_data_frame)
    num_events = len(trial_event_list)
    key = config_dict['KEY']
    interval = 0

    for i in range(num_trials):
        interval = 0
        row = []
        row.extend((EXPNAME, SUBJECTID, ITEM_LIST, CONDITION))
        row.extend((block_num, i + 1))
        row.extend(item_data_frame.iloc[i, 1:-1])

        for j in range(num_events):
            valid_key_list = ''
            event_name = trial_event_list[j][0]
            type = 'N'
            # if this step need a key press
            if trial_event_list[j][1] == "KEY":
                type = 'W'
                duration = 0
                valid_key_list = key.split()
            else:
                str = trial_event_list[j][1][0]
                if str == 'W':
                    # type 'W' means wait after sound or video fully displayed
                    type = 'W'
                    duration = float(int(trial_event_list[j][1][1:]) / 1000)
                else:
                    duration = float(int(trial_event_list[j][1]) / 1000)
            # break between pairs
            if event_name == 'ITI':
                timer = core.Clock()
                timer.reset()
                win.flip()
                core.wait(duration)
                timeUse = timer.getTime()
                row.append(round(timeUse * 1000, 4))
            else:
                # need display the pairs
                event_text = item_data_frame.loc[i, event_name]
                if valid_key_list != '':
                    res = display_event_words(event_text, duration, valid_key_list, type)
                    corr_response = item_data_frame.loc[i, 'Corr_response'].astype('str')
                    # if feedback is need, display the sound and text
                    if FEEDBACK == True:
                        if res[1] != corr_response:
                            audio = sound.Sound('Stimuli/Audio/' + item_data_frame.loc[i, 'Feedback'])
                            audio.play()
                            words = visual.TextStim(win, text='Wrong',
                                                    height=EVENT_TEXT_HEIGHT,
                                                    pos=(0.0, 0.0),
                                                    color='Red',
                                                    bold=False,
                                                    italic=False)
                            words.draw()
                            win.flip()
                            core.wait(2)
                            audio.stop()
                    row.extend(res)
                else:
                    timer = core.Clock()
                    timer.reset()
                    res = display_event_words(event_text, duration, None, type)
                    row.append(res)
        with open('Data/' + FILE_NAME + '.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(row)


def prepare(config_dict, condition_dict):
    """
    This function prepare the global variables from information in config.csv and conditions.csv
    """
    global EXPNAME, TIME_OUT, ITEM_LIST, CONDITION, SUBJECTID, FILE_NAME, RAND_BLOCKS, RAND_WITHIN_BLOCKS
    file = os.path.basename(__file__)
    # get the expriment name
    EXPNAME = os.path.splitext(file)[0]
    TIME_OUT = float(config_dict['TIMEOUT']) / 1000
    items = condition_dict['items'].split(' ')
    # get the item list in random
    ITEM_LIST = str(items[random.randint(0, len(items) - 1)])
    conditions = condition_dict['trial_events'].split(' ')
    # get the condition in random
    CONDITION = str(conditions[random.randint(0, len(conditions) - 1)])
    # randomly generate a subject id
    SUBJECTID = random.randint(10 ** 5, 10 ** 6)
    # generate the file name for output
    task_rp_list = ITEM_LIST.split('_')
    task = task_rp_list[0]
    rp = task_rp_list[1]
    lst = task_rp_list[2]
    FILE_NAME = EXPNAME + '_' + task + '_' + CONDITION + '_' + rp + '_' + lst + '_' + str(SUBJECTID)
    RAND_BLOCKS = (config_dict['RAND_BLOCKS'] == 'TRUE')
    RAND_WITHIN_BLOCKS = (config_dict['RAND_WITHIN_BLOCKS'] == 'TRUE')


def main():
    config_dict = load_dict('config.csv')
    condition_dict = load_dict('conditions.csv')
    prepare(config_dict, condition_dict)
    item_data = load_data('Stimuli/Item_Lists/' + ITEM_LIST + '.csv')
    trial_event_list = load_trial_events('Events/' + CONDITION + '.csv')
    if verify_items_and_events(item_data, trial_event_list):
        assigned_item_data, trial_block_list, practice_list = prepare_pairs(item_data, config_dict)
        experiment(assigned_item_data, trial_block_list, trial_event_list, config_dict, practice_list)
        show_instructions('Stimuli/Instructions/end.txt')
    else:
        print('Data Error!')


main()