from psychopy import visual, core, event, sound
import pandas as pd
import csv
import random
import os
import collections


class SuperPrime:

    def __init__(self):
        self.EVENT_TEXT_HEIGHT = 0.1
        self.EVENT_TEXT_FONT = 'Arial'
        self.EVENT_TEXT_COLOR = 'pink'

        self.INSTRUCTION_TEXT_HEIGHT = 0.06
        self.INSTRUCTION_FONT = 'Arial'
        self.INSTRUCTION_TEXT_COLOR = 'white'

        self.TIME_OUT = 1000
        self.FILE_NAME = ''
        self.EXPNAME = ''
        self.SUBJECTID = ''
        self.ITEM_LIST = ''
        self.CONDITION = ''
        self.RAND_BLOCKS = ''
        self.RAND_WITHIN_BLOCKS = ''
        self.FEEDBACK = False

        self.item_data = ''
        self.trial_block_list = ''
        self.practice_list = ''
        self.name_set = ''
        self.item_data_list = ''

        self.config_dict = self.load_dict('config.csv')
        self.condition_dict = self.load_dict('conditions.csv')

        self.win = visual.Window(size=(1000, 600), color=(-1, -1, -1), fullscr=True)

        self.prepare()
        self.item_data = self.load_data('Stimuli/Item_Lists/' + self.ITEM_LIST + '.csv')
        self.trial_event_list = self.load_trial_events('Events/' + self.CONDITION + '.csv')
        if self.verify_items_and_events():
            self.prepare_pairs()
            self.experiment()
            self.show_instructions('Stimuli/Instructions/end.txt')
        else:
            print('Data Error!')

    def display_instruction_words(self, instruction_text):
        """
        Get one line from the instruction text and display
        Wait 'space' to continue
        """
        words = visual.TextStim(self.win, text=instruction_text.replace(r'\n', '\n'),
                                height=self.INSTRUCTION_TEXT_HEIGHT,
                                pos=(0.0, 0.0),
                                color=self.INSTRUCTION_TEXT_COLOR,
                                bold=False,
                                italic=False)
        words.draw()
        self.win.flip()
        key_press = event.waitKeys(keyList=['space', 'escape'])

        if 'escape' in key_press:
            core.quit()

    def display_event_words(self, event_text, duration, key_list, type):
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
        self.win.flip()
        if '.jpg' in event_text and '.wav' in event_text:
            cur_events = event_text.split(' ')
            pic = {}
            for i in range(len(cur_events) - 1):
                pic[i] = visual.ImageStim(self.win, image='Stimuli/Images/' + cur_events[i], size=[0.8, 0.8],
                                          pos=pos[len(cur_events) - 1][i + 1])
                pic[i].draw()
            self.win.flip()
            audio = sound.Sound('Stimuli/Audio/' + cur_events[-1])
            audio.play()
            core.wait(duration)
            audio.stop()
        elif '.jpg' in event_text:
            pictures = event_text.split(' ')
            pic = {}
            for i in range(len(pictures)):
                pic[i] = visual.ImageStim(self.win, image='Stimuli/Images/' + pictures[i], size=[0.8, 0.8],
                                          pos=pos[len(pictures)][i + 1])
                pic[i].draw()
            self.win.flip()
            core.wait(duration)
        elif '.avi' in event_text:
            mov = visual.MovieStim3(self.win, 'Stimuli/Video/' + event_text, noAudio=False)
            if type == 'N':
                while mov.status != visual.FINISHED:
                    mov.draw()
                    self.win.flip()
                    if timer.getTime() >= duration:
                        mov.status = visual.FINISHED
                used_time = timer.getTime()
                if duration - used_time > 0:
                    core.wait(duration - used_time)
            elif type == 'W':
                while mov.status != visual.FINISHED:
                    mov.draw()
                    self.win.flip()
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
                words[i] = visual.TextStim(self.win, text=texts[i],
                                           height=self.EVENT_TEXT_HEIGHT,
                                           pos=pos[len(texts)][i + 1],
                                           color=self.EVENT_TEXT_COLOR,
                                           bold=False,
                                           italic=False)
                words[i].draw()
            self.win.flip()
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
            key_press = event.waitKeys(keyList=key_list, maxWait=self.TIME_OUT)
            if key_press == None:
                # get the time uesed for reaction
                timeUse_action = timer.getTime()
                return round(timeUse_display * 1000, 4), 'null', round(timeUse_action * 1000, 4)
            timeUse_action = timer.getTime()
            if key_press[0] in ['num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9',
                                'num_0']:
                key_press[0] = key_press[0][-1]

            if key_press[0] == 'num_end':
                key_press[0] = '1'
            elif key_press[0] == 'num_down':
                key_press[0] = '2'

            if 'escape' in key_press:
                core.quit()
            return round(timeUse_display * 1000, 4), key_press[0], round(timeUse_action * 1000, 4)

    def show_instructions(self, filePathName, name=None):
        """
        Display the main instructions and block instructions
        For block instructions, display the text according to the block name
        """
        if name == None:
            with open(filePathName) as fp:
                introduction = fp.readlines()
            for i in range(len(introduction)):
                self.display_instruction_words(introduction[i])
        else:
            res_dict = {}
            file = open(filePathName)
            for line in file:
                data = (line.strip('\n')).split('#')
                res_dict[data[0]] = data[1]
            self.display_instruction_words(res_dict[name])

    def load_dict(self, dict_file):
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

    def load_trial_events(self, trial_event_file):
        trial_event_list = []
        f = open(trial_event_file)
        for line in f:
            data = (line.strip('\n')).split(',')
            trial_event_list.append(data)
        return trial_event_list

    def load_data(self, filePath):
        data = pd.read_csv(filePath, header=0, skip_blank_lines=True)
        return data

    def verify_items_and_events(self):
        """
        Check whether all events are include in item list
        """
        self.item_data_list = self.item_data.columns.values.tolist()
        for i in range(len(self.trial_event_list)):
            if self.trial_event_list[i][0] not in self.item_data_list:
                if self.trial_event_list[i][0] != 'ITI':
                    return False
        return True

    def prepare_pairs(self):
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

        if 'Feedback' in self.item_data.columns.values.tolist():
            self.FEEDBACK = True

        num_blocks = int(self.config_dict['BLOCKS'])
        self.name_set = self.config_dict['NAME_SET'].split()
        num_items = len(self.item_data)

        if self.RAND_BLOCKS:
            copy = self.name_set[1:]
            random.shuffle(copy)
            self.name_set[1:] = copy

        # for situation with only PRACTICE and TEST
        if num_blocks > 0:
            block_list = []
            current_block = 1
            count = 0;  # count the number of practice pairs
            # Assign the block number
            for i in range(num_items):
                if self.item_data.loc[i, "Block_Name"] == 'PRACTICE':
                    count += 1
                    block_list.append(0)
                    continue
                block_list.append(current_block)
                if current_block < num_blocks:
                    current_block += 1
                else:
                    current_block = 1

            # assign the block number to "Block" column
            for i in range(len(self.item_data)):
                self.item_data.loc[i, "Block"] = block_list[i]

            # get the practice list
            practice_list = self.item_data[self.item_data["Block"] == 0]
            practice_list = practice_list.reset_index()

            # assign the pairs into each block according to the "Block" value
            self.trial_block_list = []
            for i in range(num_blocks):
                block_dataframe = self.item_data[self.item_data["Block"] == i + 1]
                if self.RAND_WITHIN_BLOCKS:
                    # shuffle within the block
                    block_dataframe = block_dataframe.sample(frac=1)
                    practice_list = practice_list.sample(frac=1)
                self.trial_block_list.append(block_dataframe.reset_index())

            self.practice_list = practice_list.reset_index(drop=True)

        # for situations with other than TEST
        else:
            for i in range(num_items):
                block_name = self.item_data.loc[i, "Block_Name"]
                self.item_data.loc[i, "Block"] = self.name_set.index(block_name)
            practice_list = self.item_data[self.item_data["Block_Name"] == 'PRACTICE']
            practice_list = practice_list.reset_index()

            self.trial_block_list = []
            # assign pairs to block according to their "Block_Name" value
            for i in range(1, len(self.name_set)):
                block_dataframe = self.item_data[self.item_data["Block"] == i]
                if self.RAND_WITHIN_BLOCKS:
                    block_dataframe = block_dataframe.sample(frac=1)
                    self.practice_list = practice_list.sample(frac=1)

                self.trial_block_list.append(block_dataframe.reset_index())

            self.practice_list = practice_list.reset_index(drop=True)

    def prepare_output_header(self):
        """
        prepare the header for the output file
        """
        header_row = []
        header_row.extend(('ExpName', 'SubjectID', 'Item_List', 'Condition'))
        header_row.extend(('BlockID', 'TrialID'))
        header_row.extend(self.item_data.columns.values.tolist()[0:-1])

        for i in range(len(self.trial_event_list)):
            if self.trial_event_list[i][0] == 'ITI':
                continue
            event_time = self.trial_event_list[i][0] + '_Time'
            header_row.append(event_time)

        header_row.extend(('Key_response', 'RT'))
        header_row.append('ITI_Time')

        with open('Data/' + self.FILE_NAME + '.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(header_row)

    def experiment(self):
        """
        This is the experiment function
        """
        # get the number of block
        num_blocks = int(self.config_dict['BLOCKS'])
        self.show_instructions('Stimuli/Instructions/main_instructions.txt')

        # determine task of the experiment and show corresponding task instructions
        task = self.condition_dict['items'].split('_')[0]
        try:
            self.show_instructions('Stimuli/Instructions/task_instructions1.txt', task)
            self.show_instructions('Stimuli/Instructions/task_instructions2.txt', task)
            self.show_instructions('Stimuli/Instructions/task_instructions3.txt', task)
        except KeyError:
            print('no corresponding instructions in file')
            pass

        self.prepare_output_header()
        name_flag = False
        # When there are PRACTICE pairs
        if len(self.practice_list) > 0:
            self.show_instructions('Stimuli/Instructions/practice_instructions.txt')
            self.block(self.practice_list, 0)
            self.show_instructions('Stimuli/Instructions/start_test.txt')
        # When there are other "Block_Name" than TEST, get the number of block according to
        # the NAME_SET
        if num_blocks < 0:
            num_blocks = len(self.config_dict['NAME_SET'].split(' ')) - 1
            name_flag = True
        for i in range(1, num_blocks + 1):
            if name_flag:
                block_name = self.name_set[i]
            else:
                block_name = 'TEST'
            self.show_instructions('Stimuli/Instructions/block_instructions.txt', block_name)
            self.block(self.trial_block_list[i - 1], i)
            if i < num_blocks:
                self.show_instructions('Stimuli/Instructions/block_break.txt')

    def block(self, item_data_frame, block_num):
        """
        This function executes each trial with all events in order.
        """
        num_trials = len(item_data_frame)
        num_events = len(self.trial_event_list)
        key = self.config_dict['KEY']
        interval = 0

        for i in range(num_trials):
            interval = 0
            row = []
            row.extend((self.EXPNAME, self.SUBJECTID, self.ITEM_LIST, self.CONDITION))
            row.extend((block_num, i + 1))
            row.extend(item_data_frame.iloc[i, 1:-1])

            for j in range(num_events):
                valid_key_list = ['escape']
                # esc key is default escape from program
                event_name = self.trial_event_list[j][0]
                type = 'N'
                # if this step need a key press
                if self.trial_event_list[j][1] == "KEY":
                    type = 'W'
                    duration = 0
                    valid_key_list.extend(key.split())
                else:
                    str = self.trial_event_list[j][1][0]
                    if str == 'W':
                        # type 'W' means wait after sound or video fully displayed
                        type = 'W'
                        duration = float(int(self.trial_event_list[j][1][1:]) / 1000)
                    else:
                        duration = float(int(self.trial_event_list[j][1]) / 1000)
                # break between pairs
                if event_name == 'ITI':
                    timer = core.Clock()
                    timer.reset()
                    self.win.flip()
                    core.wait(duration)
                    timeUse = timer.getTime()
                    row.append(round(timeUse * 1000, 4))
                else:
                    # need display the pairs
                    event_text = item_data_frame.loc[i, event_name]
                    if valid_key_list != ['escape']:
                        res = self.display_event_words(event_text, duration, valid_key_list, type)
                        corr_response = item_data_frame.loc[i, 'Corr_response'].astype('str')
                        # if feedback is need, display the sound and text
                        if self.FEEDBACK == True:
                            if res[1] != corr_response:
                                audio = sound.Sound('Stimuli/Audio/' + item_data_frame.loc[i, 'Feedback'])
                                audio.play()
                                words = visual.TextStim(self.win, text='Wrong',
                                                        height=self.EVENT_TEXT_HEIGHT,
                                                        pos=(0.0, 0.0),
                                                        color='Red',
                                                        bold=False,
                                                        italic=False)
                                words.draw()
                                self.win.flip()
                                core.wait(2)
                                audio.stop()
                        row.extend(res)
                    else:
                        timer = core.Clock()
                        timer.reset()
                        res = self.display_event_words(event_text, duration, None, type)
                        row.append(res)
            with open('Data/' + self.FILE_NAME + '.csv', 'a', newline='') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(row)

    def prepare(self):
        """
        This function prepare the global variables from information in config.csv and conditions.csv
        """
        file = os.path.basename(__file__)
        # get the expriment name
        self.EXPNAME = os.path.splitext(file)[0]
        self.TIME_OUT = float(self.config_dict['TIMEOUT']) / 1000
        items = self.condition_dict['items'].split(' ')
        # get the item list in random
        self.ITEM_LIST = str(items[random.randint(0, len(items) - 1)])
        conditions = self.condition_dict['trial_events'].split(' ')
        # get the condition in random
        self.CONDITION = str(conditions[random.randint(0, len(conditions) - 1)])
        # generate the file name for output
        task_rp_list = self.ITEM_LIST.split('_')
        task = task_rp_list[0]
        rp = task_rp_list[1]
        lst = task_rp_list[2]
        self.FILE_NAME = self.EXPNAME + '_' + task + '_' + self.CONDITION + '_' + rp + '_' + lst + '_' + \
                         str(self.SUBJECTID)
        self.RAND_BLOCKS = self.config_dict['RAND_BLOCKS']
        self.RAND_WITHIN_BLOCKS = self.config_dict['RAND_WITHIN_BLOCKS']

