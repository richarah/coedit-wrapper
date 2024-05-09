# coeditor

#### What is this?

* A tool for editing text using a Coedit transformer model, à la Grammarly. Can be used purely in textmode, with GUI (Tk) or as a module.
* **Please note: This is a work in progress!**

Requirements
------------

* Python 3.x

* Transformers

* Tkinter (for use with `--gui`)

Usage
-----

`python coeditor.py [options]`

### Options

* `--gui`: Use a graphical user interface instead of taking input via arguments.
* `--stdout`: Print edited text to standard output instead of saving it to a file.
* `--input_text TEXT`: Specify text to edit directly.
* `--input_file FILE`: Specify the path to the input text file.
* `--prompt PROMPT`: Specify the prompt for editing.
* `--output_file FILE`: Specify the path to save the edited text (required if not using `--stdout`).

Examples
--------

1. Edit text from a file and save the edited text to another file:
   `python coeditor.py --input_file input.txt --prompt "Make the text more casual." --output_file edited.txt`

2. Edit text using the GUI and print the edited text to standard output:
   `python coeditor.py --gui --stdout`

3. Edit text directly and save the edited text to a file:
   `python coeditor.py --input_text "Input text to edit." --prompt "Make the text more formal." --output_file edited.txt`
