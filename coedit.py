import argparse
import os
import tkinter as tk
from tkinter import filedialog
from transformers import AutoTokenizer, T5ForConditionalGeneration

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

def main():
    parser = argparse.ArgumentParser(description="Edit text using a Coedit transformer.")
    parser.add_argument("--gui", action="store_true", help="Use file dialog and prompt dialog.")
    parser.add_argument("--stdout", action="store_true", help="Write output to stdout instead of saving to file.")
    parser.add_argument("--input_text", help="Text to edit.")
    parser.add_argument("--input_file", help="Path to the input text file.")
    parser.add_argument("--prompt", help="Prompt for the editing task.")
    parser.add_argument("--output_file", help="Path to save the edited text.")
    args = parser.parse_args()

    if args.gui:
        if args.input_text:
            print("--input_text and --gui cannot be used together.")
            return
        file_path = get_file_path_from_dialog()
        prompt = get_prompt_from_dialog()
    else:
        if not args.input_text and (not args.input_file or not args.prompt):
            parser.error("--input_text or (--input_file and --prompt) arguments are required if --gui is not specified.")
        if args.input_text:
            text = args.input_text
            prompt = args.prompt
        else:
            file_path = args.input_file
            prompt = args.prompt

    if not args.input_text:
        with open(file_path, "r") as file:
            text = file.read()

    edited_text = edit_text(prompt, text)

    if args.stdout:
        print("Edited text:\n", edited_text)
    else:
        if not args.output_file:
            parser.error("--output_file argument is required if --stdout is not specified.")
        output_path = args.output_file
        with open(output_path, "w") as file:
            file.write(edited_text)
        print("Edited text saved to:", output_path)

if __name__ == "__main__":
    main()
