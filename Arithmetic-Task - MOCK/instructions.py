from __future__ import absolute_import, division, print_function

import os.path as op
import sys
import time

from psychopy import core, event, gui, visual
from psychopy.constants import STARTED, STOPPED


# Constants
INSTRUCTION_DICT = {
"screen_1": "Each math problem consists of four parts: an equation, a number, a question mark, and feedback.",
"screen_2": """\
You must determine if your answer to the equation is less than, equal to, or greater than the number shown:
    
\u2190 : The equation is greater
\u2193 : Both are equal
\u2192 : The number is greater"
""",
"screen_3": "Let's try practicing.",
"screen_10": """\
        Great job!

Now let's try an equation with words.""",
"screen_17":  """\
Great job!

And now we're done""",
} 

SCREEN_DICT = {
    "screen_1": ("instructions",),
    "screen_2": ("instructions",),
    "screen_3": ("instructions",),
    "screen_4": ("stimuli", "numeric", "initial_dot"),
    "screen_5": ("stimuli", "numeric", "numerical_equation"),
    "screen_6": ("stimuli", "numeric", "red_dot"),
    "screen_7": ("stimuli", "numeric", "numerical_value"),
    "screen_8": ("stimuli", "numeric", "response"),
    "screen_9": ("stimuli", "numeric", "feedback"),
    "screen_10": ("instructions",),
    "screen_11": ("stimuli", "word", "initial_dot"),
    "screen_12": ("stimuli", "word",  "word_equation"),
    "screen_13": ("stimuli", "word",  "red_dot"),
    "screen_14": ("stimuli", "word",  "word_value"),
    "screen_15": ("stimuli", "word",  "response"),
    "screen_16": ("stimuli", "numeric", "feedback"),
    "screen_17": ("instructions",)
}

# Class for user input to adjust screen
class user:
    def __init__(self, position = 1, screen = "screen_1"):
        self.position = position
        self.screen = screen
    #Update screen
    def curr_screen(self, user_input):
        self.position = self.position - 1 if user_input == "backspace" else self.position + 1
        self.position = 1 if self.position == 0 else self.position
        self.screen = "screen_" + str(self.position)

# Initialize class
curr_user = user()

def set_word_size(img):
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
    """
    Closes window if escape is pressed
    """
    if "escape" in event.getKeys():
        win.close()
        core.quit()

def draw_until_keypress(win, stim):
    """Draw stimulus until a continueKey is pressed."""
    continueKeys = ["space", "backspace"]
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
        if keys:
            return keys[-1]
        close_on_esc(win)
        win.flip()


def draw(win, stim, keyList=['left', 'right', 'down', "backspace", "space"]):
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
    window.callOnFlip(response.clock.reset)
    event.clearEvents(eventType='keyboard')
    while True:
        if isinstance(stim, list):
            for s in stim:
                s.draw()
        else:
            stim.draw()
        keys = event.getKeys(keyList=keyList)
        if keys:
            return keys[-1]
            #response.keys.extend(keys)
            #break
        close_on_esc(win)
        win.flip()
    response.status = STOPPED

if __name__ == "__main__":

    # Ensure that relative paths start from the same directory as this script
    try:
        script_dir = op.dirname(op.abspath(__file__)).decode(
            sys.getfilesystemencoding()
        )
    except AttributeError:
        script_dir = op.dirname(op.abspath(__file__))

    exp_info = {"English(e)/Spanish(s)":"",}

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
        
     # Make sure language is lower case
    exp_info["English(e)/Spanish(s)"] = exp_info["English(e)/Spanish(s)"].lower()

    # Set base path to stimuli
    base_stimuli_path = op.join(
                    script_dir,
                    "stimuli",
                    "numerals")

    # Get language
    language_stimuli = "spanish" if "s" in exp_info["English(e)/Spanish(s)"] else "english"
    ending_letter = "s" if language_stimuli == "spanish" else "e"

    # Setting up visual stimuli

    window = visual.Window(
        fullscr=True ,
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

    # Screen prompts

    instruction_text_box = visual.TextStim(
        win=window,
        name="instruction_text_box",
        text= INSTRUCTION_DICT["screen_1"],
        font="Arial",
        height=0.1,
        pos=(0, 0),
        wrapWidth=1.85,
        ori=0,
        color="white",
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
    )
    
    feedback_text_box = visual.TextStim(
        win=window,
        name="feedback_text_box",
        text= "After each trial you will receive feedback about your performance.",
        font="Arial",
        height=0.1,
        pos=(0, 0.5),
        wrapWidth=1.85,
        ori=0,
        color="white",
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
    )
    
    
    feedback_key = visual.TextStim(
        win=window,
        name="feedback_text_box",
        text= "Correct            Wrong        No Information",
        font="Arial",
        height=0.1,
        pos=(0.47, -0.40),
        wrapWidth=1.85,
        ori=0,
        color="white",
        colorSpace="rgb",
        opacity=1,
        depth=-1.0,
        alignText = "left",
    )
    
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

    # Functions for screens
    def screen_instructions():
        instruction_text_box.setText(
            INSTRUCTION_DICT[curr_user.screen]
        )
        user_input = draw_until_keypress(win=window, stim=instruction_text_box)
        curr_user.curr_screen(user_input=user_input)
        return
    # Functions for screens
    def screen_stimuli():
        # Not as efficient since variables are recreated each time this function is activated
        if SCREEN_DICT[curr_user.screen][1] == "numeric":
            # Set numeric variables
            # First example- equation with numbers
            term1_image.setImage(op.join(base_stimuli_path, "10_n.png"))
            term2_image.setImage(op.join(base_stimuli_path, "01_n.png"))
            op_image.setImage(op.join(base_stimuli_path, "add_n.png"))
            comparison_image.setImage(op.join(base_stimuli_path, "10_n.png"))
            feedback_image.setImage(op.join(script_dir, "stimuli/feedback/feedback.png"))

            term1_image.setSize(set_word_size(term1_image))
            term2_image.setSize(set_word_size(term2_image))
            op_image.setSize(set_word_size(op_image))
            comparison_image.setSize(set_word_size(comparison_image))
            width, height = feedback_image.size
            new_height = 0.6
            new_shape = (new_height * (width / height), new_height)
            feedback_image.setSize(new_shape)

            term1_pos = (term1_image.size[0] / 2.0) + (op_image.size[0] / 2.0)
            term2_pos = -1 * ((term2_image.size[0] / 2.0) + (op_image.size[0] / 2.0))
            term1_image.pos = (term1_pos, 0.0)
            term2_image.pos = (term2_pos, 0.0)
    
        else:
            # Next example- equation with words
            term1_image.setImage(op.join(base_stimuli_path, f"{language_stimuli}/05_{ending_letter}.png"))
            term2_image.setImage(op.join(base_stimuli_path, f"{language_stimuli}/07_{ending_letter}.png"))
            op_image.setImage(op.join(base_stimuli_path, f"{language_stimuli}/subtract_{ending_letter}.png"))
            comparison_image.setImage(op.join(base_stimuli_path, f"{language_stimuli}/-2_{ending_letter}.png"))
            feedback_image.setImage(op.join(script_dir, "stimuli/feedback/feedback.png"))
            term1_image.setSize(set_word_size(term1_image))
            term2_image.setSize(set_word_size(term2_image))
            op_image.setSize(set_word_size(op_image))
            term1_pos = (term1_image.size[1] / 2.0) + (op_image.size[1] / 2.0)
            term2_pos = -1 * ((term2_image.size[1] / 2.0) + (op_image.size[1] / 2.0))
            term1_image.pos = (0.0, term1_pos)
            term2_image.pos = (0.0, term2_pos)

            comparison_image.setSize(set_word_size(comparison_image))
            width, height = feedback_image.size
            new_height = 0.6
            new_shape = (new_height * (width / height), new_height)
            feedback_image.setSize(new_shape)
        
        # Stimuli screen logic

        if curr_user.screen in ["screen_4", "screen_11"]:
            user_input = draw(win=window, stim=iti_stim, keyList=['space', "backspace"])
            print(user_input)
            curr_user.curr_screen(user_input=user_input)
            
        elif curr_user.screen in ["screen_5", "screen_12"]:
            user_input = draw(win=window, stim=[term1_image, op_image, term2_image], keyList=['space', "backspace"])
            curr_user.curr_screen(user_input=user_input)
            
        elif curr_user.screen in ["screen_6", "screen_13"]:
            user_input = draw(win=window, stim=isi_stim, keyList=['space', "backspace"])
            curr_user.curr_screen(user_input=user_input)
            
        elif curr_user.screen in ["screen_7", "screen_14"]:
            user_input = draw(win=window, stim=comparison_image, keyList=['space', "backspace"])
            curr_user.curr_screen(user_input=user_input)
            
        elif curr_user.screen in ["screen_8", "screen_15"]:
            user_input = draw(win=window, stim=response_stim, keyList=['left', 'right', 'down', "backspace"])
            curr_user.curr_screen(user_input=user_input)
            
        elif curr_user.screen in ["screen_9", "screen_16"]:
            user_input = draw(win=window, stim=[feedback_text_box, feedback_image, feedback_key], keyList=['space', "backspace"])
            curr_user.curr_screen(user_input=user_input)
        
        # Unset stim sizes so they don't pass on to the next trial
        term1_image.size = None
        op_image.size = None
        term2_image.size = None
        eq_image.size = None
        comparison_image.size = None
        
        return
    #Select function based on current user position

    def select_screen(screen):
        if screen != "screen_18":
            if SCREEN_DICT[screen][0] == "instructions": screen_instructions()
            else: screen_stimuli()

    while curr_user.screen  != "screen_18":
        select_screen(screen=curr_user.screen)

     # make sure everything is closed down
    window.close()
    core.quit()

