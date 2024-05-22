#! /usr/bin/env python
# Time-stamp: <2021-11-16 15:36:47 christophe@pallier.org>
""" This is a simple target-detection experiment.

At each trial, lines are presented at the center of the screen and
the participant must answer as quickly as possible if a target is present or not.
"""

##  Condition the stimuli to not appear on top of each other (--> can do a list of possible positions, choose randomly from it and remove the elements already chosen).

import numpy as np
import math
import random
from expyriment import design, control, stimuli


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

N_TRIALS = 20
LINE_LENGTH = 20
LINE_WIDTH = 2
OBLIQUE_ANGLE = 20
CIRCLE_RADIUS = 360

# Define the keys to answer ("y" and "n")
y = 121
n = 110
answers = {y : "Yes", n : "No"}

## Define the conditions of the experiment and make it a list for each trial :
nbs_distractors = [5,10,15]
target_types = ["oblique", "vertical"]
target_presences = [True, False]
list_conditions = []
for target in target_types:
    for presence in target_presences:
        for nb_distractors in nbs_distractors:
            list_conditions.append({
                "target_type": target,
                "target_presence": presence,
                "nb_distractors": nb_distractors
            })
list_trials=list_conditions*(round(N_TRIALS/len(list_conditions)))
random.shuffle(list_trials)


exp = design.Experiment(name="Target Detection", text_size=40, background_colour=WHITE)
# control.set_develop_mode(on=True)
control.initialize(exp)

blankscreen = stimuli.BlankScreen(WHITE)

instructions = stimuli.TextScreen("Instructions",
    f"""You will have a target presented among distractors. Target is either an oblique line among vertical lines or a vertical line among oblique lines. 
    You will have to tell if the target is present (if there is a line that is different from the rest) or not .
    The target will be present 50% of the time and absent 50% of the time. 
    
    Your task is to press as quickly as possible y if the target is present or n if it is not (measure of reaction time).

    There will be {len(list_trials)} trials in total.

    Press the spacebar to start.""", position = (0,-175), text_colour=BLACK, text_size=20)

exp.add_data_variable_names(['target_type','target_presence', 'answer', 'accuracy', 'rt', 'nb_distractors'])

# Distance of the line from the border of the circle :
distance = 20 

# Function to randomly chose a starting point (with a distance from the border of the circle)
def choose_start_point():
    x_coordinate = random.randrange(-CIRCLE_RADIUS + distance,
        round(CIRCLE_RADIUS - distance - LINE_LENGTH))
    angle = math.acos(x_coordinate / (CIRCLE_RADIUS - distance))
    if angle == 0 or angle == math.pi:
        y_coordinate = 0
    else:
        y_coordinate = random.randrange(
            round((distance - CIRCLE_RADIUS) * math.sin(angle)),
            round((CIRCLE_RADIUS - LINE_LENGTH - distance) * math.sin(angle)))
    start_point = np.array((x_coordinate, y_coordinate))
    return (start_point)

## Define the relative end points of the line (as a function of the angle) :
oblique_relative_end_point = np.array(
    (LINE_LENGTH * math.sin(math.radians(OBLIQUE_ANGLE)),
     LINE_LENGTH * math.cos(math.radians(OBLIQUE_ANGLE))))
vertical_relative_end_point = np.array((0, LINE_LENGTH))

#Function to make a line (vertical or oblique)
def make_line(type):
    start_point = choose_start_point()
    if type == "vertical":
        relative_end_point = vertical_relative_end_point
    elif type == "oblique":
        relative_end_point = oblique_relative_end_point
    line = stimuli.Line(start_point, (start_point + relative_end_point),
                        line_width=LINE_WIDTH,
                        colour=BLACK,
                        anti_aliasing=10)
    return (line)

# Function to create the whole stimulus (lines in the circle)
def make_stimulus(target_presence, target_type, nb_distractors):
    if target_presence == True:
        target = make_line(target_type)
        target.plot(circle)
    else :
        nb_distractors = nb_distractors+1

    distractor_type = "oblique" if target_type == "vertical" else "vertical"
    for i in range (nb_distractors):
        distractor = make_line(distractor_type)
        distractor.plot(circle)

    return(circle)

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()

for trial in list_trials:
    circle = stimuli.Circle(CIRCLE_RADIUS, colour=BLACK, line_width=2)
    stimulus = make_stimulus(trial["target_presence"], trial["target_type"],
                             trial["nb_distractors"])
    stimulus.present()
    key, rt = exp.keyboard.wait(keys=list(answers.keys()))

    correct = (trial["target_presence"] == True
               and answers[key] == "Yes") or (trial["target_presence"] == False
                                              and answers[key] == "No")

    exp.data.add([
        trial["target_type"], trial["target_presence"], answers[key], correct,
        rt, trial["nb_distractors"]
    ])

    blankscreen.present()
    exp.clock.wait(500)

control.end()
