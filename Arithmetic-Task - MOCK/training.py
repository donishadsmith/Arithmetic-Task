#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.2),
    on June 26, 2019, at 17:43
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
from __future__ import absolute_import, division, print_function

import os.path as op
import sys
import time
from glob import glob
from os import makedirs

import numpy as np
import pandas as pd
from psychopy import core, data, event, gui, logging, visual
from psychopy.constants import STARTED, STOPPED

# Constants
OPERATOR_DICT = {"+": "add", "-": "subtract", "/": "divide", "*": "multiply"} 
RUN_DURATION = 450
LEAD_IN_DURATION = 6
END_SCREEN_DURATION = 2
INSTRUCTION_DICT = {
        "instructions": """\
Instructions:

\u2190 : The equation is greater
\u2193 : Both are equal
\u2192 : The number is greater

To continue, press the "spacebar"
"""
    }

def set_word_size(img):
    """Set size of word image."""
    # det from orig height 2row / orig height 1row
    const = 1.764505119453925

    # desired 1row height
    height_1row = 0.225
    height_2rows = height_1row * const
    width, height = img.size
    if height > 1:  # det by stim gen procedure
        new_height = height_2rows
    else:
        new_height = height_1row
    new_shape = (new_height * (width / height), new_height)
    return new_shape


def close_on_esc(win):
    """Close window if escape is pressed."""
    if "escape" in event.getKeys():
        win.close()
        core.quit()


def draw_until_keypress(win, stim):
    """Draw stimulus until a continueKey is pressed."""
    continueKeys = ["space"]
    response = event.BuilderKeyResponse()
    win.callOnFlip(response.clock.reset)
    event.clearEvents(eventType="keyboard")
    while True:
        if isinstance(stim, list):
            for s in stim:
                s.draw()
        else:
            stim.draw()
        keys = event.getKeys(keyList=continueKeys)
        if any([ck in keys for ck in continueKeys]):
                return
        close_on_esc(win)
        win.flip()
        
def draw(win, stim, duration, clock):
    """
    Draw stimulus for a given duration.

    Parameters
    ----------
    win : (visual.Window)
    stim : object with `.draw()` method or list of such objects
    duration : (numeric)
        duration in seconds to display the stimulus
    """
    # Use a busy loop instead of sleeping so we can exit early if need be.
    start_time = time.time()
    response = event.BuilderKeyResponse()
    response.tStart = start_time
    response.frameNStart = 0
    response.status = STARTED
    win.callOnFlip(response.clock.reset)
    event.clearEvents(eventType="keyboard")
    while time.time() - start_time < duration:
        if isinstance(stim, list):
            for s in stim:
                s.draw()
        else:
            stim.draw()
        keys = event.getKeys(keyList=["right", "down", "left"], timeStamped=clock)
        if keys:
            response.keys.extend(keys)
            response.rt.append(response.clock.getTime())
        close_on_esc(win)
        win.flip()
    response.status = STOPPED
    return response.keys, response.rt


if __name__ == "__main__":
    # Ensure that relative paths start from the same directory as this script
    try:
        script_dir = op.dirname(op.abspath(__file__)).decode(
            sys.getfilesystemencoding()
        )
    except AttributeError:
        script_dir = op.dirname(op.abspath(__file__))

    # Collect user input
    # ------------------
    exp_info = {
        "English(e)/Spanish(s)":"",
    }
    
    while exp_info["English(e)/Spanish(s)"].lower() not in ["e","s"]:
        dlg = gui.DlgFromDict(
            exp_info,
            title="Arithmetic Task",
            order=[
                "English(e)/Spanish(s)",
            ],
        )
        # Quit is ok isn't selected
        if not dlg.OK:
            core.quit()

    exp_info["Subject"] = 0
    exp_info["Session"] = 0
    exp_info["Number of Training Runs"] = 1

    window = visual.Window(
        fullscr=True,  # Remember to turn fullscr to True for the real deal.
        size=(800, 600),
        monitor="testMonitor",
        units="norm",
        allowStencil=False,
        allowGUI=False,
        color="black",
        colorSpace="rgb",
        blendMode="avg",
        useFBO=True,
    )
    # Make sure language is lower case
    exp_info["English(e)/Spanish(s)"] = exp_info["English(e)/Spanish(s)"].lower()

    """if not dlg.OK or not exp_info["English(e)/Spanish(s)"] in ["e","s"]:
        core.quit()  # user pressed cancel"""
    
    # Number of Training Runs will always be 1
    exp_info["Number of Training Runs"] = 1
    # Make output dir
    makedirs(op.join(script_dir, "data"), exist_ok=True)

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    base_name = "sub-{0}_ses-{1}_task-arithmetic".format(
        exp_info["Subject"],
        exp_info["Session"],
    )

    n_runs = exp_info["Number of Training Runs"]

    # Point to correct stimuli folder
    language_stimuli = "spanish" if "s" in exp_info["English(e)/Spanish(s)"] else "english"
    # Check for existence of output files
    config_files = glob(op.join(script_dir, "config", language_stimuli, "config_*.tsv"))[0]
    
    
    for i_run in range(1, n_runs + 1):
        outfile = op.join(
            script_dir, "data", "{0}_run-{1}_events.tsv".format(base_name, i_run)
        )
        """if op.exists(outfile) and "Pilot" not in outfile:
            raise ValueError("Output file already exists.")"""

    # save a log file for detail verbose info
    filename = op.join(script_dir, "data", "{0}_events".format(base_name))
    logfile = logging.LogFile(filename + ".log", level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    # Initialize stimuli
    # ------------------
    term1_image = visual.ImageStim(
        win=window,
        name="equation_first_term",
        image=None,
        ori=0,
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
        interpolate=True,
    )
    op_image = visual.ImageStim(
        win=window,
        name="equation_operator",
        image=None,
        ori=0,
        pos=(0, 0),
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
        interpolate=True,
    )
    term2_image = visual.ImageStim(
        win=window,
        name="equation_second_term",
        image=None,
        ori=0,
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
        interpolate=True,
    )
    eq_image = visual.ImageStim(
        win=window,
        name="equation",
        image=None,
        ori=0,
        pos=(0, 0),
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
        interpolate=True,
    )
    comparison_image = visual.ImageStim(
        win=window,
        name="comparison",
        image=None,
        ori=0,
        pos=(0, 0),
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
        interpolate=True,
    )
    feedback_image = visual.ImageStim(
        win=window,
        name="feedback",
        image=None,
        size=None,
        ori=0,
        pos=(0, 0),
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
        interpolate=True,
    )
    
    done_image = visual.ImageStim(
        win=window,
        name="feedback",
        image=None,
        size=None,
        ori=0,
        pos=(0, 0),
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
        interpolate=True,
    )
    iti_stim = visual.TextStim(
        win=window,
        name="fixation",
        text="\u2022",
        font="Arial",
        pos=(0, 0),
        height=0.14,
        wrapWidth=None,
        ori=0,
        color="white",
        colorSpace="rgb",
        opacity=1,
        depth=0.0,
    )

    isi_stim = visual.TextStim(
        win=window,
        name="fixation",
        text="\u2022",
        font="Arial",
        pos=(0, 0),
        height=0.14,
        wrapWidth=None,
        ori=0,
        color="red",
        colorSpace="rgb",
        opacity=1,
        depth=0.0,
    )
    response_stim = visual.TextStim(
        win=window,
        name="fixation",
        text="\u003F",
        font="Arial",
        pos=(0, 0),
        height=0.14,
        wrapWidth=None,
        ori=0,
        color="white",
        colorSpace="rgb",
        opacity=1,
        depth=0.0,
    )
    end_screen = visual.TextStim(
        win=window,
        name="end_screen",
        text="The task is now complete.",
        font="Arial",
        pos=(0, 0),
        height=0.14,
        wrapWidth=None,
        ori=0,
        color="white",
        colorSpace="rgb",
        opacity=1,
        depth=0.0,
    )

    # Scanner runtime
    # ---------------
    # NOTE: unused
    # global_clock = core.Clock()  # to track the time since experiment started
    run_clock = core.Clock()  # to track time since each run starts (post scanner pulse)
    stage_clock = core.Clock()  # to track duration of each stage in each trial

    # set up handler to look after randomisation of conditions etc
    run_loop = data.TrialHandler(
        nReps=n_runs,
        method="random",
        extraInfo=exp_info,
        originPath=-1,
        trialList=[None],
        seed=None,
        name="run_loop",
    )

    for curr_run in run_loop:
        
        COLUMNS = [
            "onset",
            "duration",
            "trial_type",
            "run_type",
            "comparison_onset",
            "comparison_duration",
            "feedback_onset",
            "feedback_duration",
            "feedback_type",
            "first_term",
            "operation",
            "second_term",
            "comparison",
            "solution",
            "rounded_difference",
            "response",
            "response_time",
            "accuracy",
            "stim_file_first_term",
            "stim_file_operator",
            "stim_file_second_term",
            "stim_file_comparison",
            "stim_file_feedback",
            "equation_representation",
            "comparison_representation",
        ]
        run_data = {c: [] for c in COLUMNS}
        # NOTE: appears unused
        # currentLoop = run_loop
        run_label = run_loop.thisN + 1

        run_type = "Training"

        config_df = pd.read_table(config_files)
        
        outfile = op.join(
            script_dir,
            "data",
            "{0}_run-{1}_events.tsv".format(base_name, run_label),
        )

        # set up handler to look after randomisation of conditions etc
        trial_loop = data.TrialHandler(
            nReps=config_df.shape[0],
            method="random",
            extraInfo=exp_info,
            originPath=-1,
            trialList=[None],
            seed=None,
            name="trial_loop",
        )

        # Scanner runtime
        # ---------------
        # Wait for trigger from scanner.
        # Get language specific instruction
        instruction_text_box = visual.TextStim(
        win=window,
        name='instruction_text_box',
        text= INSTRUCTION_DICT["instructions"],
        font=u'Arial',
        height=0.1,
        pos=(0, 0),
        wrapWidth=1.3,
        ori=0,
        color='white',
        colorSpace='rgb',
        opacity=1,
        depth=-1.0,
        alignText = "center")
       
       
        draw_until_keypress(win=window, stim=instruction_text_box)
        
        # Create path to stimuli

        base_stimuli_path = op.join(
                    script_dir,
                    "stimuli",
                    "numerals")
        
        run_clock.reset()

        # Beginning fixation
        stage_clock.reset()
        draw(win=window, stim=iti_stim, duration=LEAD_IN_DURATION, clock=stage_clock)

        for curr_trial in trial_loop:
            # This section (before the "prepare" portion) takes ~0.4s with 300dpi images
            # Within reasonable range for 72dpi images
            trial_num = trial_loop.thisN
            
            trial_type = config_df.loc[trial_num, "trial_type"]
            equation = config_df.loc[trial_num, "equation"]
            num_type_eq = config_df.loc[trial_num, "equation_representation"]
            num_type_comp = config_df.loc[trial_num, "comparison_representation"]
            comparison = int(config_df.loc[trial_num, "comparison"])
            rounded_difference = int(config_df.loc[trial_num, "rounded_difference"])
            solution = config_df.loc[trial_num, "solution"]
            feedback_type = config_df.loc[trial_num, "feedback"]

            #term_stimuli_path = base_stimuli_path if num_type_eq[0] == "n" else op.join(base_stimuli_path,f"{language_stimuli}")
            
            if num_type_eq[0] == "n":term_stimuli_path = base_stimuli_path
            elif num_type_eq[0] == "e": term_stimuli_path =  op.join(base_stimuli_path,"english")
            else: term_stimuli_path =  op.join(base_stimuli_path,"spanish")

            operator = [x for x in equation if not x.isdigit()][0]
            term1, term2 = equation.split(operator)
            term1_image.setImage(
                op.join(term_stimuli_path,
                    "{0:02d}_{1}.png".format(int(term1), num_type_eq[0]),
                )
            )
            term2_image.setImage(
                op.join(term_stimuli_path,
                    "{0:02d}_{1}.png".format(int(term2), num_type_eq[0]),
                )
            )
            op_image.setImage(
                op.join(term_stimuli_path,
                    "{0}_{1}.png".format(OPERATOR_DICT[operator], num_type_eq[0]),
                )
            )
            op_image.setSize(set_word_size(op_image))
            if num_type_eq == "numeric":
                term1_image.setSize(set_word_size(term1_image))
                term2_image.setSize(set_word_size(term2_image))
                term1_pos = -1 * (
                    (term1_image.size[0] / 2.0) + (op_image.size[0] / 2.0)
                )
                term2_pos = (term2_image.size[0] / 2.0) + (op_image.size[0] / 2.0)
                term1_image.pos = (term1_pos, 0.0)
                term2_image.pos = (term2_pos, 0.0)
            elif num_type_eq in ["english_word", "spanish_word"]:
                term1_image.setSize(set_word_size(term1_image))
                term2_image.setSize(set_word_size(term2_image))
                term1_pos = (term1_image.size[1] / 2.0) + (op_image.size[1] / 2.0)
                term2_pos = -1 * (
                    (term2_image.size[1] / 2.0) + (op_image.size[1] / 2.0)
                )
                term1_image.pos = (0.0, term1_pos)
                term2_image.pos = (0.0, term2_pos)
            elif num_type_eq == "analog":  # unused
                term1_image.size = (0.45, 0.675)
                term2_image.size = (0.45, 0.675)
                term1_image.pos = (-0.45, 0.0)
                term2_image.pos = (0.45, 0.0)
            else:
                raise Exception(
                    'num_type_eq must be "analog", "numeric", '
                    ',"english_word", or "spanish_word,  not {}'.format(num_type_eq)
                )

            run_data["first_term"].append(int(term1))
            run_data["operation"].append(OPERATOR_DICT[operator])
            run_data["second_term"].append(int(term2))
            run_data["stim_file_first_term"].append(
                term1_image.image.split(op.sep + "stimuli" + op.sep)[1]
            )
            run_data["stim_file_second_term"].append(
                term2_image.image.split(op.sep + "stimuli" + op.sep)[1]
            )
            run_data["stim_file_operator"].append(
                op_image.image.split(op.sep + "stimuli" + op.sep)[1]
            )

            #comparison_stimuli_path = base_stimuli_path if num_type_comp[0] == "n" else op.join(base_stimuli_path,f"{language_stimuli}")
            
            if num_type_comp[0] == "n":comparison_stimuli_path = base_stimuli_path
            elif num_type_comp[0] == "e": comparison_stimuli_path =  op.join(base_stimuli_path,"english")
            else: comparison_stimuli_path =  op.join(base_stimuli_path,"spanish")
            
            comparison_image.setImage(
                op.join(comparison_stimuli_path ,
                    "{0:02d}_{1}.png".format(comparison, num_type_comp[0]),
                )
            )
            comparison_image.setSize(set_word_size(comparison_image))

            # Equation
            stage_clock.reset()
            equation_onset_time = run_clock.getTime()
            draw(
                win=window,
                stim=[term1_image, op_image, term2_image],
                duration=config_df.loc[trial_num, "equation_duration"],
                clock=stage_clock,
            )
            equation_duration = stage_clock.getTime()

            # ISI1
            stage_clock.reset()
            isi1_keys, _ = draw(
                win=window,
                stim=isi_stim,
                duration=config_df.loc[trial_num, "isi1"],
                clock=stage_clock,
            )

            # Comparison
            stage_clock.reset()
            comparison_onset_time = run_clock.getTime()
            task_keys, _ = draw(
                win=window,
                stim=comparison_image,
                duration=config_df.loc[trial_num, "comparison_duration"],
                clock=stage_clock,
            )
            comparison_duration = stage_clock.getTime()

            # ISI2
            stage_clock.reset()
            isi2_keys, _ = draw(
                win=window,
                stim=[response_stim],
                duration=config_df.loc[trial_num, "isi2"],
                clock=stage_clock,
            )

            # determine response, using the *last* key pressed within the response window
            # (comparison window + ISI2)
            if task_keys and isi2_keys:
                response_value = isi2_keys[-1][0]
                run_data["response_time"].append(task_keys[0][1])
            elif task_keys and not isi2_keys:
                response_value = task_keys[-1][0]
                run_data["response_time"].append(task_keys[0][1])
            elif isi2_keys and not task_keys:
                response_value = isi2_keys[-1][0]
                run_data["response_time"].append(isi2_keys[0][1])
            else:
                response_value = "n/a"
                run_data["response_time"].append(np.nan)

            run_data["response"].append(response_value)

            # determine correct response
            if solution > comparison:
                corr_resp = "left"
            elif solution == comparison:
                corr_resp = "down"
            elif solution < comparison:
                corr_resp = "right"

            # determine accuracy
            if response_value == "n/a":
                trial_status = "no_response"
            elif response_value == corr_resp:
                trial_status = "correct"
            else:
                trial_status = "incorrect"

            # determine feedback
            if feedback_type == "noninformative": 
                feedback_image.image = op.join(
                        script_dir, "stimuli", "feedback", "noninformative.png"
                    )
            else:
                if trial_status == "correct":
                    feedback_image.image = op.join(
                        script_dir, "stimuli", "feedback", "positive.png"
                    )
                elif trial_status == "incorrect":
                    feedback_image.image = op.join(
                        script_dir, "stimuli", "feedback", "negative.png"
                    )
                else:  # no response
                    feedback_image.image = op.join(
                        script_dir, "stimuli", "feedback", "negative.png"
                    )

            # feedback presentation
            stage_clock.reset()
            feedback_onset_time = run_clock.getTime()
            width, height = feedback_image.size
            new_height = 0.6
            new_shape = (new_height * (width / height), new_height)
            feedback_image.setSize(new_shape)
            draw(
                win=window,
                stim=feedback_image,
                duration=config_df.loc[trial_num, "feedback_duration"],
                clock=stage_clock,
            )
            feedback_duration = stage_clock.getTime()

            # Compile new row of output file
            run_data["onset"].append(equation_onset_time)
            run_data["duration"].append(equation_duration)
            run_data["trial_type"].append(trial_type)
            run_data["comparison_onset"].append(comparison_onset_time)
            run_data["comparison_duration"].append(comparison_duration)
            run_data["feedback_onset"].append(feedback_onset_time)
            run_data["feedback_duration"].append(feedback_duration)
            run_data["feedback_type"].append(feedback_type)
            run_data["equation_representation"].append(num_type_eq)
            run_data["comparison_representation"].append(num_type_comp)
            run_data["comparison"].append(comparison)
            run_data["accuracy"].append(trial_status)
            run_data["solution"].append(solution)
            run_data["rounded_difference"].append(rounded_difference)
            run_data["run_type"].append(run_type)
            run_data["stim_file_comparison"].append(
                comparison_image.image.split(op.sep + "stimuli" + op.sep)[1]
            )
            run_data["stim_file_feedback"].append(
                feedback_image.image.split(op.sep + "stimuli" + op.sep)[1]
            )

            # ITI
            stage_clock.reset()
            if trial_num == config_df.index.values[-1]:
                # For last trial, update fixation duration
                iti_duration = RUN_DURATION - run_clock.getTime()
            else:
                iti_duration = config_df.loc[trial_num, "iti"]
            
            # Unset stim sizes so they don't pass on to the next trial
            term1_image.size = None
            op_image.size = None
            term2_image.size = None
            eq_image.size = None
            comparison_image.size = None
            # end trial_loop

        run_frame = pd.DataFrame(run_data)
        run_frame.to_csv(
            outfile,
            sep="\t",
            line_terminator="\n",
            na_rep="n/a",
            index=False,
            float_format="%.2f",
        )

        print("Total duration of run: {}".format(run_clock.getTime()))
        # end run_loop

    # Scanner is off for this
    stage_clock.reset()
    draw(win=window, stim=end_screen, duration=END_SCREEN_DURATION, clock=stage_clock)
    window.flip()

    logging.flush()

    # make sure everything is closed down
    window.close()
    core.quit()
