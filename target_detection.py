#! /usr/bin/env python
# Time-stamp: <2021-11-16 15:36:47 christophe@pallier.org>
""" This is a simple reaction-time experiment.

At each trial, a cross is presented at the center of the screen and
the participant must press a key as quickly as possible.
"""

## To do : 
##  Restrict the lines to appear only in the circle
##  Condition the stimuli to not appear on top of each other (--> how ?). 
##  Add a condition where the target is not present

import numpy as np
import math
import random
from expyriment import design, control, stimuli


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

N_TRIALS = 20
LINE_LENGTH = 20
LINE_WIDTH = 2
OBLIQUE_ANGLE = 20
WIDTH_SCREEN = 1080
LENGTH_SCREEN = 1920
CIRCLE_RADIUS = 360

exp = design.Experiment(name="Target Detection", text_size=40, background_colour=WHITE)
#control.set_develop_mode(on=True)
control.initialize(exp)

blankscreen = stimuli.BlankScreen(WHITE)

## Define the end points of the line (function of the angle) : 
oblique_relative_end_point = np.array((LINE_LENGTH*math.sin(math.radians(OBLIQUE_ANGLE)), LINE_LENGTH*math.cos(math.radians(OBLIQUE_ANGLE))))
vertical_relative_end_point = np.array((0, LINE_LENGTH))

instructions = stimuli.TextScreen("Instructions",
    f"""You will have a target presented among distractors. Target is either an oblique line or a vertical line, it will be indicated. 

    Your task is to press as quickly as possible the left key if the target is not present or the right key if it is not (We measure your reaction-time).

    There will be {N_TRIALS} trials in total.

    Press the spacebar to start.""", text_colour=BLACK)

exp.add_data_variable_names(['trial', 'key', 'rt', 'nb_distractors'])

def choose_start_point():
    x_coordinate = random.randrange(-CIRCLE_RADIUS+10,CIRCLE_RADIUS-LINE_LENGTH-10)
    angle=math.acos(x_coordinate/CIRCLE_RADIUS)
    y_coordinate = random.randrange(round((-CIRCLE_RADIUS+10)*math.sin(angle)),round((CIRCLE_RADIUS-LINE_LENGTH-10)*math.sin(angle)))

    return((x_coordinate,y_coordinate))


def make_stimulus(target_presence, target_type, nb_distractors, circle): 
    if target_presence == False : 
        if target_type == "oblique target":
            for i in range (nb_distractors+2):
                start_point = np.array(choose_start_point())
                vertical = stimuli.Line(start_point, (start_point+vertical_relative_end_point), line_width=LINE_WIDTH, colour=BLACK)
                vertical.plot(circle)

        elif target_type == "vertical target":
            for i in range (nb_distractors+2):
                start_point_oblique = np.array(choose_start_point())
                oblique = stimuli.Line(start_point_oblique, (start_point_oblique+oblique_relative_end_point), line_width=LINE_WIDTH, colour=BLACK)
                oblique.plot(circle)

    elif target_presence == True:
        if target_type == "oblique target":
            for i in range (nb_distractors+1):
                start_point = np.array(choose_start_point())
                vertical = stimuli.Line(start_point, (start_point+vertical_relative_end_point), line_width=LINE_WIDTH, colour=BLACK)
                vertical.plot(circle)
            start_point_oblique = np.array(choose_start_point())
            oblique = stimuli.Line(start_point_oblique, start_point_oblique+oblique_relative_end_point, line_width=LINE_WIDTH, colour=BLACK)
            oblique.plot(circle)

        elif target_type == "vertical target":
            for i in range (nb_distractors+1):
                start_point_oblique = np.array(choose_start_point())
                oblique = stimuli.Line(start_point_oblique, (start_point_oblique+oblique_relative_end_point), line_width=LINE_WIDTH, colour=BLACK)
                oblique.plot(circle)
            start_point = np.array(choose_start_point())
            vertical = stimuli.Line(start_point, start_point+vertical_relative_end_point, line_width=LINE_WIDTH, colour=BLACK)
            vertical.plot(circle)
    return(circle)


control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()

# Define possible positions :
# circle = stimuli.Circle(360, colour=BLACK, line_width=2)

target_type = ["oblique target", "vertical target"]
target_presences = [True, False] 
list_conditions = []
for target in target_type :
    for presence in target_presences:
        list_conditions.append({"target_type":target,"target_presence": presence})
list_trials=list_conditions*int((N_TRIALS/len(list_conditions)))
random.shuffle(list_trials)

nb_distractors = 20

for trial in list_trials:
    circle = stimuli.Circle(360, colour=BLACK, line_width=2)
    stimulus=make_stimulus(trial["target_presence"], trial["target_type"], nb_distractors, circle)  
    stimulus.present()
    key, rt = exp.keyboard.wait()
    exp.data.add([trial, key, rt, nb_distractors])
    blankscreen.present()
    exp.clock.wait(500)

control.end()


