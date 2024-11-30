import os
import re
import argparse
from tqdm import tqdm
from deep_translator import GoogleTranslator

def get_color(percentage):
    """Return color based on the completion percentage."""
    if percentage < 50:
        return '\033[38;5;214m'  # Orange
    elif percentage < 90:
        return '\033[38;5;154m'  # Light Green
    else:
        return '\033[38;5;82m'   # Green

def reset_color():
    return '\033[0m'

def create_output_filename(file_path, src_lang, dest_lang):
    """Generate the output file name by replacing the source language in the file name with the destination language."""
    base_name, ext = os.path.splitext(file_path)
    # Remove src_lang if it exists in the file name and replace it with dest_lang
    updated_base_name = re.sub(rf"{src_lang}\b", f"{dest_lang}", base_name, flags=re.IGNORECASE)
    # If src_lang was not in the file name, just add dest_lang suffix
    if updated_base_name == base_name:
        updated_base_name = f"{base_name}_{dest_lang}"
    return f"{updated_base_name}{ext}"

def translate_subtitle(file_path, src_lang, dest_lang, output_file):
    # Load the subtitle file
    with open(file_path, 'r') as file:
        srt_content = file.readlines()

    # Initialize translator
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    translated_srt_content = []

    # Check if output file exists to resume from last progress
    start_line = 0
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            translated_srt_content = file.readlines()
            start_line = len(translated_srt_content)

    # Translate each line starting from where we left off
    with tqdm(total=len(srt_content), initial=start_line, desc="Translating", unit="line") as pbar:
        for i in range(start_line, len(srt_content)):
            line = srt_content[i]
            if line.strip() and not line.strip().isdigit() and '-->' not in line:
                # Translate dialogue
                try:
                    translation = translator.translate(line.strip())
                    translated_srt_content.append(translation + '\n')
                except Exception as e:
                    print(f"Error translating line {i}: {e}")
                    translated_srt_content.append(line)  # Keep original line if translation fails
            else:
                # Keep timing and numbering as is
                translated_srt_content.append(line)

            # Save progress immediately to avoid data loss in case of interruption
            with open(output_file, 'a') as file:
                file.write(translated_srt_content[-1])

            # Update progress bar with color
            percentage = (i + 1) / len(srt_content) * 100
            color = get_color(percentage)
            pbar.set_description(f"{color}Translating{reset_color()}")
            pbar.update(1)

    print(f"Translation complete. Saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate subtitles to a different language.")

    # Required positional argument for the subtitle file
    parser.add_argument("file_path", help="Path to the subtitle file to translate")

    # Optional language arguments with shorthand -f and -t
    parser.add_argument("-f", "--from", dest="src_lang", required=True, help="Source language code (e.g., 'en')")
    parser.add_argument("-t", "--to", dest="dest_lang", required=True, help="Destination language code (e.g., 'fa')")

    # Optional output argument with shorthand -o
    parser.add_argument("-o", "--output", dest="output_file", help="Path to save the translated subtitle file")

    args = parser.parse_args()

    # Automatically generate output file name if not provided
    if not args.output_file:
        args.output_file = create_output_filename(args.file_path, args.src_lang, args.dest_lang)

    translate_subtitle(args.file_path, args.src_lang, args.dest_lang, args.output_file)
