%matplotlib inline
import os.path as op, glob, os
import matplotlib.pyplot as plt
from num2words import num2words

# Base directory with system separator
base_dir = f'..{op.sep}stimuli{op.sep}numerals'

# Create Directory
if not op.exists(base_dir):
        os.makedirs(base_dir)

# Check if english stimuli is already in folder
png_files = [(file, op.basename(file)) for file in glob.glob(op.join(base_dir,"*.png"))]
# Move english stimuli to folder
if len(png_files) > 0:
    if not op.exists(op.join(base_dir,"english")) and glob.glob(op.join(base_dir,"*_w.png")):
        os.makedirs(op.join(base_dir,"english"))
        renamed_files = [os.rename(original_file, op.join(base_dir,'english', basename.replace("_w","_e"))) for original_file, basename in png_files if "_w" in basename]

# Check if each numerical operator and 00 image is in the base directory since it is the first and last numerical images to be generated. If not, then do loop to generate numbers
if not all(operators in [op.basename(file) for file in glob.glob(op.join(base_dir,"*"))] for operators in ["00_n.png","add_n.png","subtract_n.png", "divide_n.png","multiply_n.png"]):
    # Create Numbers  
    out_dir = base_dir
    # Make analog images
    plt.style.use('dark_background')
    for value in range(1, 31):
        fig, axes = plt.subplots(nrows=5, ncols=6, squeeze=False, figsize=(6, 5))
        for i, ax in enumerate(axes.flat):
            if i + 1 <= value:
                circle = plt.Circle((.5, .5), radius=0.45, fc='white')
                ax.add_patch(circle)
            ax.set(xticklabels=[], yticklabels=[])
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            for spine in ['top', 'left', 'bottom', 'right']:
                ax.spines[spine].set_linewidth(1.5)
        fig.subplots_adjust(hspace=0, wspace=0)
        fig.savefig(op.join(out_dir, f'{value:02d}_a.png'), dpi=72)
        plt.close()

        # Make numeral images for numbers
    plt.style.use('dark_background')
    for value in range(-40, 911):
        fig = plt.figure(figsize=(6, 5), facecolor='black')
        plt.text(0.5, 0.4, value, color='white', size=240, ha='center', va='center')
        for ax in fig.axes:
            ax.set(xticklabels=[], yticklabels=[])
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            for spine in ['top', 'left', 'bottom', 'right']:
                ax.spines[spine].set_linewidth(0)
        fig.savefig(op.join(out_dir, f'{value:02d}_n.png'), dpi=72, bbox_inches='tight')
        plt.close()
    # Make numeral/analog images for operators
    plt.style.use('dark_background')
    operators = {'+': 'add', '-':'subtract', '\u00F7':'divide', '\u00D7':'multiply'}
    for value in ['+', '-', '\u00F7', '\u00D7']:
        fig = plt.figure(figsize=(3, 2), facecolor='black')
        plt.text(0.5, 0.25, value, color='white', size=240, ha='center', va='center')
        for ax in fig.axes:
            ax.set(xticklabels=[], yticklabels=[])
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            for spine in ['top', 'left', 'bottom', 'right']:
                ax.spines[spine].set_linewidth(0)
        fig.savefig(op.join(out_dir, f'{operators[value]}_n.png'), dpi=72, bbox_inches='tight')
        fig.savefig(op.join(out_dir, f'{operators[value]}_a.png'), dpi=72, bbox_inches='tight')
        plt.close()

# Set languages
languages = ["spanish"] if op.exists(op.join(base_dir,"english")) else ["english","spanish"]

for language in languages:
    if not op.exists(op.join(base_dir,f"{language}")):
        os.makedirs(op.join(base_dir,f"{language}"))
        # Make word images for numbers
    out_dir = op.join(base_dir,f"{language}")
    plt.style.use('dark_background')
    for value in range(-40, 911):
        fig = plt.figure(figsize=(6, 5), facecolor='black')
        word = num2words(value).replace('minus', 'negative').replace(' and ', ' ') if language == "english" else num2words(value, lang = "es").replace('minus', 'negative').replace(' and ', ' ')
        if len(word) > 13:
            word = word.replace('hundred ', 'hundred\n')
            word = word.replace('negative ', 'negative\n')

        plt.text(0.5, 0.4, word, color='white', size=240, ha='center', va='center')
        for ax in fig.axes:
            ax.set(xticklabels=[], yticklabels=[])
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            for spine in ['top', 'left', 'bottom', 'right']:
                ax.spines[spine].set_linewidth(0)
        fig.savefig(op.join(out_dir, f'{value:02d}_w.png'), dpi=72, bbox_inches='tight')
        plt.close()
        # Make word images for operators
    plt.style.use('dark_background')
    operators = {'plus': 'add', 'minus':'subtract', 'divided by':'divide', 'times':'multiply'} if language == "english" else {'sumar': 'add', 'menos':'subtract', 'dividido por':'divide', 'multiplicar por':'multiply'} 
    terms = ['plus', 'minus', 'divided by', 'times'] if language == "english" else ['sumar', 'menos', 'dividido por','multiplicar por'] 
    for value in terms:
        n_chars = len(operators[value])
        fig = plt.figure(figsize=(n_chars*2, 5), facecolor='black')
        plt.text(0.5, 0.45, value, color='white', size=240, ha='center', va='center')
        for ax in fig.axes:
            ax.set(xticklabels=[], yticklabels=[])
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            for spine in ['top', 'left', 'bottom', 'right']:
                ax.spines[spine].set_linewidth(0)
        if language == "english":
            fig.savefig(op.join(out_dir, f'{operators[value]}_e.png'), dpi=72, bbox_inches='tight')
        else:
            fig.savefig(op.join(out_dir, f'{operators[value]}_s.png'), dpi=72, bbox_inches='tight')
        plt.close()