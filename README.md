# Amharic and Tigrigna Analyzer

## Description

The Amharic and Tigrigna Analyzer is a powerful desktop application designed to analyze and compare texts in Amharic and Tigrigna languages. It provides various analysis options including character frequency, word frequency, phoneme distribution, and overlap calculations at character, word, and phoneme levels.

## Features

- Input fields for Amharic and Tigrigna texts
- Character frequency analysis
- Word frequency analysis
- Phoneme distribution analysis
- Character level overlap calculation
- Word level overlap calculation
- Phoneme level overlap calculation
- Phoneme conversion display
- Results saving functionality
- User-friendly GUI with themed interface

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository or download the source code.
3. Install the required dependencies:
   ```
   pip install tkinter ttkthemes
   ```
4. Place the `data.json` file in the same directory as the script. This file should contain the phoneme conversion dictionaries for both Amharic and Tigrigna.

## Usage

1. Run the script:
   ```
   python app.py
   ```
2. Enter Amharic text in the "Amharic Text" field.
3. Enter Tigrigna text in the "Tigrigna Text" field.
4. Click the "Process Text" button to analyze the input.
5. Use the dropdown menus to select different analysis options and languages.
6. View the results in the table and text areas.
7. Use the "Save Results" button to save the analysis to a text file.

## Analysis Options

- Character Frequency: Displays the frequency of each character in the selected language.
- Word Frequency: Shows the frequency of each word in the selected language.
- Phoneme Distribution: Presents the distribution of phonemes in the selected language.
- Character Level Overlap: Compares shared characters between Amharic and Tigrigna.
- Word Level Overlap: Compares shared words between Amharic and Tigrigna.
- Phoneme Level Overlap: Compares shared phonemes between Amharic and Tigrigna.

## Dependencies

- Python 3.x
- tkinter
- ttkthemes

## File Structure

- `app.py`: The main application script.
- `data.json`: JSON file containing phoneme conversion dictionaries for Amharic and Tigrigna.

## Author

Dagm Yibabe

Contact: dagimyibabe19@gmail.com
Telegram: @dag19yi

## License

© 2023 All rights reserved.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page] if you want to contribute.

## Show your support

Give a ⭐️ if this project helped you!
