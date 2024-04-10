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

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()

# Define possible positions :
# circle = stimuli.Circle(360, colour=BLACK, line_width=2)

conditions = ["oblique target", "vertical target"]
trials=conditions*int((N_TRIALS/len(conditions)))
random.shuffle(trials)

nb_distractors = 20

for trial in trials:
    circle = stimuli.Circle(360, colour=BLACK, line_width=2)
    if trial == "oblique target":
        for j in range (nb_distractors+1):
            start_point = np.array((random.randrange(-360,360),random.randrange(-360,360)))
            vertical = stimuli.Line(start_point, (start_point+vertical_relative_end_point), line_width=LINE_WIDTH, colour=BLACK)
            vertical.plot(circle)
        start_point_oblique = np.array((random.randrange(-360,360),random.randrange(-360,360)))
        oblique = stimuli.Line(start_point_oblique, start_point_oblique+oblique_relative_end_point, line_width=LINE_WIDTH, colour=BLACK)
        oblique.plot(circle)

    if trial == "vertical target":
        for j in range (nb_distractors+1):
            start_point_oblique = np.array((random.randrange(-360,360),random.randrange(-360,360)))
            oblique = stimuli.Line(start_point_oblique, (start_point_oblique+oblique_relative_end_point), line_width=LINE_WIDTH, colour=BLACK)
            oblique.plot(circle)
        start_point = np.array((random.randrange(-360,360),random.randrange(-360,360)))
        vertical = stimuli.Line(start_point, start_point+vertical_relative_end_point, line_width=LINE_WIDTH, colour=BLACK)
        vertical.plot(circle)
    circle.present()
    key, rt = exp.keyboard.wait()
    exp.data.add([trial, key, rt, nb_distractors])
    blankscreen.present()
    exp.clock.wait(500)

control.end()


