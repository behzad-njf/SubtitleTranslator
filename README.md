# Subtitle Translator

This Python script allows you to translate subtitle files (e.g., `.srt`) from one language to another using the `deep-translator` library and Google Translate. The script handles progress tracking and supports resuming from where it left off in case of interruptions.

## Features
- Translates subtitles from any source language to any target language.
- Supports `.srt` subtitle format.
- Automatically generates output file names.
- Resumes translation from the last completed line if interrupted.
- Provides a color-coded progress bar for tracking.

## Prerequisites

- Python 3.6 or higher
- `deep-translator` library
- `tqdm` library for progress bar

Install the required libraries using:
```bash
pip install deep-translator tqdm
```

## Usage

Run the script using the following command:

```bash
python subtitle_translator.py <file_path> -f <source_language_code> -t <destination_language_code> [-o <output_file_path>]
```

### Positional Arguments:
- `<file_path>`: Path to the subtitle file to be translated.

### Optional Arguments:
- `-f` / `--from`: Source language code (e.g., `en` for English, `es` for Spanish). Required.
- `-t` / `--to`: Target language code (e.g., `fa` for Farsi, `fr` for French). Required.
- `-o` / `--output`: Path to save the translated subtitle file. If not provided, the script will automatically generate a name.

### Example:

Translate an English subtitle file (`example.srt`) to Spanish:

```bash
python subtitle_translator.py example.srt -f en -t es
```

Specify an output file name:

```bash
python subtitle_translator.py example.srt -f en -t es -o translated_example.srt
```

## Output File Naming
If no output file is specified, the script will generate a file name by replacing the source language code in the original file name with the target language code or appending the target language code as a suffix. For example:

- Input: `movie_en.srt`
- Output: `movie_es.srt`

## Error Handling
- Lines that fail to translate due to errors will remain in their original form in the output file.
- The script saves progress after each line to prevent data loss in case of interruption.

## Contributions
Contributions are welcome! Feel free to fork this repository, make improvements, and create pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Enjoy seamless subtitle translation with this script!

