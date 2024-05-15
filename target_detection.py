#! /usr/bin/env python
# Time-stamp: <2021-11-16 15:36:47 christophe@pallier.org>
""" This is a simple target-detection experiment.

At each trial, lines are presented at the center of the screen and
the participant must answer as quickly as possible if a target is present or not.
"""

## To do : 
##  Condition the stimuli to not appear on top of each other (--> can do a list of possible positions, choose randomly from it and remove the elements already chosen). 
## Separate the target types in 2 experiments or in one experiment (add an something for what to look for ?)

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
# HEIGHT_SCREEN = 1080
# WIDTH_SCREEN = 1920
CIRCLE_RADIUS = 360

## Define the conditions of the experiment : 
nbs_distractors = [5,10,15]
target_types = ["oblique target", "vertical target"]
target_presences = [True, False] 
list_conditions = []
for target in target_types :
    for presence in target_presences:
        for nb_distractors in nbs_distractors:
            list_conditions.append({"target_type":target,"target_presence": presence, "nb_distractors":nb_distractors})
list_trials=list_conditions*(round(N_TRIALS/len(list_conditions)))
random.shuffle(list_trials)


exp = design.Experiment(name="Target Detection", text_size=40, background_colour=WHITE)
# control.set_develop_mode(on=True)
control.initialize(exp)

blankscreen = stimuli.BlankScreen(WHITE)

instructions = stimuli.TextScreen("Instructions",
    f"""You will have a target presented among distractors. Target is either an oblique line among vertical lines or a vertical line among oblique lines. 
    You will have to decide which target you are looking for according to what the distractors are.
    The target will be present 50% of the time and absent 50% of the time. 
    
    Your task is to press as quickly as possible y if the target is present or n if it is not (measure of reaction time).

    There will be {len(list_trials)} trials in total.

    Press the spacebar to start.""", position = (0,-175), text_colour=BLACK, text_size=20)

exp.add_data_variable_names(['target_type','target_presence', 'answer', 'accuracy', 'rt', 'nb_distractors'])

## Define the relative end points of the line (function of the angle) : 
oblique_relative_end_point = np.array((LINE_LENGTH*math.sin(math.radians(OBLIQUE_ANGLE)), LINE_LENGTH*math.cos(math.radians(OBLIQUE_ANGLE))))
vertical_relative_end_point = np.array((0, LINE_LENGTH))

distance = 20

def choose_start_point():
    x_coordinate = random.randrange(-CIRCLE_RADIUS+distance,round(CIRCLE_RADIUS-distance-LINE_LENGTH)) #math.cos(math.radians(OBLIQUE_ANGLE))
    angle = math.acos(x_coordinate/(CIRCLE_RADIUS-distance))
    if angle == 0 or angle == math.pi:
        y_coordinate = 0
    else : 
        y_coordinate = random.randrange(round((distance-CIRCLE_RADIUS)*math.sin(angle)),round((CIRCLE_RADIUS-LINE_LENGTH-distance)*math.sin(angle)))

    return((x_coordinate,y_coordinate))


def make_stimulus(target_presence, target_type, nb_distractors): 
    distractor_type = "distractor oblique" if target_type == "vertical target" else "distractor vertical"
    if distractor_type == "distractor vertical":
        for i in range (nb_distractors+1):
            start_point = np.array(choose_start_point())
            vertical = stimuli.Line(start_point, (start_point+vertical_relative_end_point), line_width=LINE_WIDTH, colour=BLACK)
            vertical.plot(circle)

    elif distractor_type == "distractor oblique":
        for i in range (nb_distractors+1):
            start_point_oblique = np.array(choose_start_point())
            oblique = stimuli.Line(start_point_oblique, (start_point_oblique+oblique_relative_end_point), line_width=LINE_WIDTH, colour=BLACK, anti_aliasing=10)
            oblique.plot(circle)

    if target_presence == True:
        if target_type == "oblique target":
            start_point_oblique = np.array(choose_start_point())
            oblique = stimuli.Line(start_point_oblique, (start_point_oblique+oblique_relative_end_point), line_width=LINE_WIDTH, colour=BLACK, anti_aliasing=10)
            oblique.plot(circle)

        elif target_type == "vertical target":
            start_point = np.array(choose_start_point())
            vertical = stimuli.Line(start_point, (start_point+vertical_relative_end_point), line_width=LINE_WIDTH, colour=BLACK)
            vertical.plot(circle)
    return(circle)


control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()


# for trial in list_trials:
index_trial = 0
while index_trial < len(list_trials):
    trial=list_trials[index_trial]
    circle = stimuli.Circle(CIRCLE_RADIUS, colour=BLACK, line_width=2)
    stimulus = make_stimulus(trial["target_presence"], trial["target_type"], trial["nb_distractors"])
    stimulus.present()
    key, rt = exp.keyboard.wait()
    if key == 121 : 
        answer = "Yes"
    elif key == 110 :
        answer = "No"
    else : 
        continue
    if (trial["target_presence"] == True and answer == "No") or (trial["target_presence"] == False and answer == "Yes"):
        accuracy = "incorrect"
    elif (trial["target_presence"] == True and answer == "Yes") or (trial["target_presence"] == False and answer == "No"):
        accuracy = "correct"
    exp.data.add([trial["target_type"],trial["target_presence"], answer, accuracy, rt, trial["nb_distractors"]])
    index_trial += 1
    blankscreen.present()
    exp.clock.wait(500)

control.end()


