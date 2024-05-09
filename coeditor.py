import argparse
import logging
import tkinter as tk
from tkinter import filedialog
from transformers import AutoTokenizer, T5ForConditionalGeneration

logging.basicConfig(level=logging.INFO)

def edit_text(prompt, text):
    tokenizer = AutoTokenizer.from_pretrained("grammarly/coedit-large")
    model = T5ForConditionalGeneration.from_pretrained("grammarly/coedit-large")
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=256, num_return_sequences=1)
    edited_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return edited_text

def get_file_path_from_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def get_prompt_from_dialog():
    root = tk.Tk()
    root.withdraw()
    prompt = tk.simpledialog.askstring("Input", "Enter the prompt:")
    return prompt

def load_text_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def save_text_to_file(text, output_path):
    with open(output_path, "w") as file:
        file.write(text)

def process_input(args):
    text, prompt = None, None
    if args.gui:
        if args.input_text:
            logging.error("--input_text and --gui cannot be used together.")
            return None, None
        file_path = get_file_path_from_dialog()
        if not file_path:
            logging.error("No file selected.")
            return None, None
        prompt = get_prompt_from_dialog()
    else:
        if not args.input_text and (not args.input_file or not args.prompt):
            logging.error("--input_text or (--input_file and --prompt) arguments are required if --gui is not specified.")
            return None, None
        if args.input_text:
            text = args.input_text
            prompt = args.prompt
        else:
            file_path = args.input_file
            if not os.path.exists(file_path):
                logging.error("Input file does not exist.")
                return None, None
            text = load_text_from_file(file_path)
            prompt = args.prompt

    return text, prompt

def main():
    parser = argparse.ArgumentParser(description="Edit text using a Coedit transformer.")
    parser.add_argument("--gui", action="store_true", help="Use file dialog and prompt dialog.")
    parser.add_argument("--stdout", action="store_true", help="Write output to stdout instead of saving to file.")
    parser.add_argument("--input_text", help="Text to edit.")
    parser.add_argument("--input_file", help="Path to the input text file.")
    parser.add_argument("--prompt", help="Prompt for the editing task.")
    parser.add_argument("--output_file", help="Path to save the edited text.")
    args = parser.parse_args()

    try:
        text, prompt = process_input(args)
    except ValueError as e:
        logging.error(e)
        return

    edited_text = edit_text(prompt, text)

    if args.stdout:
        logging.info("Edited text:\n%s", edited_text)
    else:
        if not args.output_file:
            logging.error("--output_file argument is required if --stdout is not specified.")
            return
        save_text_to_file(edited_text, args.output_file)
        logging.info("Edited text saved to: %s", args.output_file)

if __name__ == "__main__":
    main()
