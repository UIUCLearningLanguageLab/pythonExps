import numpy as np
import pandas as pd
import csv
import os
import tkinter as tk
from datetime import datetime
from PIL import ImageTk, Image


class GUI:
    def __init__(self):
        self.config_dict = self.load_dict('config.csv')
        self.condition_dict = self.load_dict('conditions.csv')

        self.root = tk.Tk()
        self.root.title('Priming.py')
        # root.geometry("750x700")
        # root.resizable(0, 0)

        # reading directory for legal options
        list_options = [os.path.splitext(file)[0] for file
                        in os.listdir('Stimuli/Item_Lists')]
        soa_options = [os.path.splitext(file)[0] for file
                       in os.listdir('Events')]
        task_options = self.load_dict('Stimuli/Tasks/Tasks.csv')
        task_options = list(task_options.keys())

        list_options.sort()
        soa_options.sort()
        task_options.sort()

        # setting up GUI
        self.blocks = tk.StringVar()
        self.blocks.set(self.config_dict["BLOCKS"])
        self.key = tk.StringVar()
        self.key.set(self.config_dict["KEY"])
        self.timeout = tk.StringVar()
        self.timeout.set(self.config_dict["TIMEOUT"])
        self.task = tk.StringVar()
        self.task.set(self.config_dict["TASK"])
        self.rand_within_blocks = tk.StringVar()
        self.rand_within_blocks.set(self.config_dict['RAND_WITHIN_BLOCKS'])
        self.rand_blocks = tk.StringVar()
        self.rand_blocks.set(self.config_dict['RAND_BLOCKS'])
        self.item_list = tk.StringVar()
        self.item_list.set(self.condition_dict['items'])
        self.trial_events = tk.StringVar()
        self.trial_events.set(self.condition_dict['trial_events'])
        self.experimenter = tk.StringVar()
        self.subjectid = tk.StringVar()
        self.saved_changes = tk.BooleanVar()
        self.saved_changes.set(0)

        frame_image = tk.Frame(self.root)
        frame_image.grid(row=0, columnspan=2, pady=(0, 25))
        path = 'Misc/superprime.jpg'
        img = ImageTk.PhotoImage(Image.open(path).resize((350, 250)))
        panel = tk.Label(frame_image, image=img)
        panel.grid(row=0)

        frame_topleft = tk.Frame(self.root)
        frame_topleft.grid(row=1, column=0, sticky='nesw')
        for column in [0, 1]:
            frame_topleft.grid_columnconfigure(column, minsize=175)
        label_configcsv = tk.Label(frame_topleft, text='config.csv', relief='solid')
        label_KEY = tk.Label(frame_topleft, text='KEY')
        label_TIMEOUT = tk.Label(frame_topleft, text='TIMEOUT')
        label_TASK = tk.Label(frame_topleft, text='TASK')
        label_RAND_WITHIN_BLOCK = tk.Label(frame_topleft, text='RAND_WITHIN_BLOCK')
        label_RAND_BLOCKS = tk.Label(frame_topleft, text='RAND_BLOCKS')
        entry_KEY = tk.Entry(frame_topleft, textvariable=self.key)
        entry_TIMEOUT = tk.Entry(frame_topleft, textvariable=self.timeout)
        option_menu_TASK = tk.OptionMenu(frame_topleft, self.task, *task_options)
        option_menu_RAND_WITHIN_BLOCKS = tk.OptionMenu(frame_topleft, self.rand_within_blocks, "TRUE", "FALSE")
        option_menu_RAND_BLOCKS = tk.OptionMenu(frame_topleft, self.rand_blocks, "TRUE", "FALSE")
        label_configcsv.grid(row=0, column=0, columnspan=2, pady=(5, 10))
        label_KEY.grid(row=1, sticky='e')
        label_TIMEOUT.grid(row=2, sticky='e')
        label_TASK.grid(row=3, sticky='e')
        label_RAND_WITHIN_BLOCK.grid(row=4, sticky='e')
        label_RAND_BLOCKS.grid(row=5, sticky='e')
        entry_KEY.grid(row=1, column=1, sticky='we')
        entry_TIMEOUT.grid(row=2, column=1, sticky='we')
        option_menu_TASK.grid(row=3, column=1, sticky='we')
        option_menu_RAND_WITHIN_BLOCKS.grid(row=4, column=1, sticky='we')
        option_menu_RAND_BLOCKS.grid(row=5, column=1, sticky='we')

        frame_topright = tk.Frame(self.root)
        frame_topright.grid(row=1, column=1, sticky='nesw', padx=(30, 0))
        for column in [0, 1]:
            frame_topright.grid_columnconfigure(column, minsize=175)
        label_conditionscsv = tk.Label(frame_topright, text='conditions.csv', relief='solid')
        label_ITEM_LISTS = tk.Label(frame_topright, text='Item List')
        label_SOA = tk.Label(frame_topright, text='SOA')
        option_menu_item_lists = tk.OptionMenu(frame_topright, self.item_list, *list_options)
        option_menu_soa = tk.OptionMenu(frame_topright, self.trial_events, *soa_options)
        label_conditionscsv.grid(row=0, columnspan=2, sticky='N', pady=(5, 10))
        label_ITEM_LISTS.grid(row=1, sticky='e')
        label_SOA.grid(row=2, sticky='e')
        option_menu_item_lists.grid(row=1, column=1, sticky='we')
        option_menu_soa.grid(row=2, column=1, sticky='we')

        frame_bottom = tk.Frame(self.root)
        frame_bottom.grid(row=2, columnspan=2)
        label_Experimenter = tk.Label(frame_bottom, text='Experimenter')
        label_SubjectID = tk.Label(frame_bottom, text='Subject ID')
        label_logcsv = tk.Label(frame_bottom, text='experiment_log.csv', relief='solid')
        button_save = tk.Button(frame_bottom, text='Run!',
                                command=lambda: self.save_changes())
        entry_Experimenter = tk.Entry(frame_bottom, textvariable=self.experimenter, justify='center')
        entry_SubjectID = tk.Entry(frame_bottom, textvariable=self.subjectid, justify='center')
        label_Experimenter.grid(row=1)
        label_SubjectID.grid(row=3)
        label_logcsv.grid(row=0, pady=(25, 10))
        button_save.grid(row=5, pady=(25, 0))
        entry_Experimenter.grid(row=2)
        entry_SubjectID.grid(row=4)

        self.root.mainloop()

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

    def return_block_names(self, filePath):
        data = pd.read_csv(filePath, header=0, skip_blank_lines=True)

        name_set, idx = np.unique(data["Block_Name"], return_index=True)
        name_set = name_set[np.argsort(idx)]
        name_set = list(name_set)
        return name_set

    def popup(self, title, msg, entry=False, textvar=''):
        self.pup = tk.Toplevel()
        self.pup.title(title)

        label_msg = tk.Label(self.pup, text=msg)
        label_msg.pack()

        if entry:
            entry_field = tk.Entry(self.pup, textvariable=textvar)
            entry_field.pack()

        exit_button = tk.Button(self.pup, text='Confirm', command=lambda: [self.save_popup(self.blocks, 'BLOCKS',
                                                                                             self.config_dict),
                                                                             self.pup.destroy()])
        exit_button.pack()
        self.root.wait_window(self.pup)

    def save_changes(self):
        self.config_dict['TASK'] = self.task.get()
        self.experimenter = self.experimenter.get()
        self.subjectid = self.subjectid.get()

        if (len(self.experimenter) > 0) & (len(self.subjectid) > 0):
            if self.task.get() == 'CATEGORY DECISION':
                self.blocks = -1
                self.config_dict['BLOCKS'] = self.blocks
            else:
                self.popup('How many blocks?', 'Number of Blocks', True, self.blocks)

            self.config_dict['KEY'] = self.key.get()
            self.config_dict['TIMEOUT'] = self.timeout.get()
            self.config_dict['RAND_WITHIN_BLOCKS'] = self.rand_within_blocks.get()
            self.config_dict['RAND_BLOCKS'] = self.rand_blocks.get()

            self.condition_dict['items'] = self.item_list.get()
            self.condition_dict['trial_events'] = self.trial_events.get()


            self.condition_dict['subj_id'] = self.subjectid

            self.config_dict['NAME_SET'] = ' '.join(
                self.return_block_names('Stimuli/Item_Lists/' + self.item_list.get() + '.csv'))

            with open('config.csv', 'w') as f:
                for key in self.config_dict.keys():
                    f.write("%s,%s\n" % (key, self.config_dict[key]))
                f.close()

            with open('conditions.csv', 'w') as f:
                for key in self.condition_dict.keys():
                    f.write("%s,%s\n" % (key, self.condition_dict[key]))
                f.close()

            self.write_exp_log()
            self.root.destroy()
            self.saved_changes.set(1)
        else:
            self.popup('FILL EVERYTHING OUT', 'FILL EVERYTHING OUT')
            self.root.destroy()

    def save_popup(self, var, key, dct):
        var = var.get()
        dct[str(key)] = var

    def write_exp_log(self):
        with open('experiment_log.csv', 'a+', newline='') as f:
            f_count = open('experiment_log.csv', 'r')
            length = sum(1 for line in f_count)
            f_count.close()
            if length == 0:
                header = ['Date', 'Time', 'Task', 'SOA', 'RP&List', 'SubjNum', 'Experimenter']
                row = [datetime.now().date(), datetime.now().time(), self.task, self.trial_events.get(),
                       self.item_list.get(), self.subjectid, self.experimenter]
                filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(header)
                filewriter.writerow(row)
            elif length > 0:
                row = [datetime.now().date(), datetime.now().time(), self.task.get(), self.trial_events.get(),
                       self.item_list.get(), self.subjectid, self.experimenter]
                filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(row)
