from psychopy import visual, core, event, sound
import collections

def display_event(event_text, key_list):
    
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
    win.flip()
    if len(event_text.split(' ')) > 1:
        audio = sound.Sound('audio/sound.wav')
        audio.play()
        core.wait(3)
        audio.stop()
        key_press = event.waitKeys(keyList=key_list)
        print(key_press)
    else:
        if event_text == '+':
            core.wait(1)
        else:
            core.wait(0.2)
 

def experiment(trails):
    for trail in trails:
        events = trail.split(';')
        for event in events:
            display_event(event, ['1','2'])
        win.flip()
        
def eyelink_prepare():
    pass

if __name__=="__main__":
    trails = ['+;&;dog.jpg cat.jpeg','+;&;dog.jpg shoes.jpg','+;&;cat.jpeg monkey.jpg','+;&;cat.jpeg mouse.jpeg']
    eyelink_prepare()
    win = visual.Window(size = (1000,600), color = (-1,-1,-1), fullscr = False )
    experiment(trails)
