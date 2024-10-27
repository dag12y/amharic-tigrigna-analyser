import json
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from collections import Counter
import sys
import os
from ttkthemes import ThemedTk

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(__file__)

amh_json_path = os.path.join(application_path, 'data.json')
tig_json_path = os.path.join(application_path, 'data.json')

# Load the dictionary from the JSON file
with open(amh_json_path, 'r', encoding='utf-8') as file:
    conversion_dict_amharic = json.load(file)

with open(tig_json_path, 'r', encoding='utf-8') as file:
    conversion_dict_tigrigna = json.load(file)

def transliterate(word, conversion_dict):
    translit = ""
    for letter in word:
        if letter in conversion_dict:
            translit += conversion_dict[letter]
        else:
            translit += letter
    return translit

def convert_text(text, conversion_dict):
    converted = ''.join([transliterate(char, conversion_dict) for char in text])
    converted = (converted
                 .replace('ə ', ' ')
                 .replace('ə\n', '\n')
                 .rstrip('ə'))
    return converted

def clean_text(text):
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def char_frequency(text):
    return dict(Counter([char for char in text if char != ' ']))

def word_frequency(text):
    words = text.split()
    return dict(Counter(words))

def phoneme_frequency(phonemes):
    return dict(Counter([phoneme for phoneme in phonemes if phoneme != ' ']))

def display_table(tree, data, headers):
    tree.delete(*tree.get_children())
    tree["columns"] = headers
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=150, anchor="center")
    for row in data:
        tree.insert("", "end", values=row)

def main():
    def process_text():
        amharic_text = entry_amharic.get("1.0", tk.END).strip()
        tigrigna_text = entry_tigrigna.get("1.0", tk.END).strip()

        if not amharic_text or not tigrigna_text:
            messagebox.showerror("Input Error", "Please enter both Amharic and Tigrigna text.")
            return

        # Clean the input texts
        amharic_text_cleaned = clean_text(amharic_text)
        tigrigna_text_cleaned = clean_text(tigrigna_text)

        # Character-level analysis
        global amharic_char_freq, tigrigna_char_freq, shared_chars, char_overlap_ratio_amharic, char_overlap_ratio_tigrigna
        amharic_char_freq = char_frequency(amharic_text_cleaned)
        tigrigna_char_freq = char_frequency(tigrigna_text_cleaned)
        amharic_chars = set(amharic_char_freq.keys())
        tigrigna_chars = set(tigrigna_char_freq.keys())
        shared_chars = amharic_chars.intersection(tigrigna_chars)
        char_overlap_ratio_amharic = len(shared_chars) / len(amharic_chars) if amharic_chars else 0
        char_overlap_ratio_tigrigna = len(shared_chars) / len(tigrigna_chars) if tigrigna_chars else 0
        avg_char_overlap = (char_overlap_ratio_amharic + char_overlap_ratio_tigrigna) / 2

        # Word-level analysis
        global amharic_word_freq, tigrigna_word_freq, shared_words, word_overlap_ratio_amharic, word_overlap_ratio_tigrigna
        amharic_word_freq = word_frequency(amharic_text_cleaned)
        tigrigna_word_freq = word_frequency(tigrigna_text_cleaned)
        amharic_words = set(amharic_word_freq.keys())
        tigrigna_words = set(tigrigna_word_freq.keys())
        shared_words = amharic_words.intersection(tigrigna_words)
        word_overlap_ratio_amharic = len(shared_words) / len(amharic_words) if amharic_words else 0
        word_overlap_ratio_tigrigna = len(shared_words) / len(tigrigna_words) if tigrigna_words else 0
        avg_word_overlap = (word_overlap_ratio_amharic + word_overlap_ratio_tigrigna) / 2

        # Phoneme-level analysis
        global amharic_phonemes, tigrigna_phonemes, amharic_phoneme_freq, tigrigna_phoneme_freq
        global shared_phonemes, phoneme_overlap_ratio_amharic, phoneme_overlap_ratio_tigrigna
        amharic_phonemes = convert_text(amharic_text_cleaned, conversion_dict_amharic)
        tigrigna_phonemes = convert_text(tigrigna_text_cleaned, conversion_dict_tigrigna)
        amharic_phoneme_freq = phoneme_frequency(amharic_phonemes)
        tigrigna_phoneme_freq = phoneme_frequency(tigrigna_phonemes)
        amharic_phonemes_set = set(amharic_phoneme_freq.keys())
        tigrigna_phonemes_set = set(tigrigna_phoneme_freq.keys())
        shared_phonemes = amharic_phonemes_set.intersection(tigrigna_phonemes_set)
        phoneme_overlap_ratio_amharic = len(shared_phonemes) / len(amharic_phonemes_set) if amharic_phonemes_set else 0
        phoneme_overlap_ratio_tigrigna = len(shared_phonemes) / len(tigrigna_phonemes_set) if tigrigna_phonemes_set else 0
        avg_phoneme_overlap = (phoneme_overlap_ratio_amharic + phoneme_overlap_ratio_tigrigna) / 2

        # Update phoneme conversion tab
        phoneme_text.delete("1.0", tk.END)
        phoneme_text.insert(tk.END, f"Amharic Phonemes:\n{amharic_phonemes}\n\nTigrigna Phonemes:\n{tigrigna_phonemes}")

        # Display all overlap ratios
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Character Overlap:\n"
                                f"Amharic: {char_overlap_ratio_amharic:.2f}\n"
                                f"Tigrigna: {char_overlap_ratio_tigrigna:.2f}\n"
                                f"Average: {avg_char_overlap:.2f}\n\n"
                                f"Word Overlap:\n"
                                f"Amharic: {word_overlap_ratio_amharic:.2f}\n"
                                f"Tigrigna: {word_overlap_ratio_tigrigna:.2f}\n"
                                f"Average: {avg_word_overlap:.2f}\n\n"
                                f"Phoneme Overlap:\n"
                                f"Amharic: {phoneme_overlap_ratio_amharic:.2f}\n"
                                f"Tigrigna: {phoneme_overlap_ratio_tigrigna:.2f}\n"
                                f"Average: {avg_phoneme_overlap:.2f}")
        result_text.config(state=tk.DISABLED)

        # Show the results frame after processing text
        frame_results.pack(pady=10, fill=tk.BOTH, expand=True)
        notebook.select(0)  # Select the first tab by default

        status_bar.config(text="Text processed successfully")

    def on_option_select(event):
        choice = combo_options.get()
        language = combo_language.get()
        data = []
        headers = []
        
        if choice == "Character Frequency":
            if language == "Amharic":
                headers = ["Character", "Frequency"]
                data = [[char, freq] for char, freq in amharic_char_freq.items()]
            elif language == "Tigrigna":
                headers = ["Character", "Frequency"]
                data = [[char, freq] for char, freq in tigrigna_char_freq.items()]
        elif choice == "Word Frequency":
            if language == "Amharic":
                headers = ["Word", "Frequency"]
                data = [[word, freq] for word, freq in amharic_word_freq.items()]
            elif language == "Tigrigna":
                headers = ["Word", "Frequency"]
                data = [[word, freq] for word, freq in tigrigna_word_freq.items()]
        elif choice == "Phoneme Distribution":
            if language == "Amharic":
                headers = ["Phoneme", "Frequency"]
                data = [[phoneme, freq] for phoneme, freq in amharic_phoneme_freq.items()]
            elif language == "Tigrigna":
                headers = ["Phoneme", "Frequency"]
                data = [[phoneme, freq] for phoneme, freq in tigrigna_phoneme_freq.items()]
        elif choice == "Character Level Overlap":
            headers = ["Shared Characters", "Amharic Ratio", "Tigrigna Ratio"]
            data = [[char, f"{char_overlap_ratio_amharic:.2f}", f"{char_overlap_ratio_tigrigna:.2f}"] for char in shared_chars] if shared_chars else []
        elif choice == "Word Level Overlap":
            headers = ["Shared Words", "Amharic Ratio", "Tigrigna Ratio"]
            data = [[word, f"{word_overlap_ratio_amharic:.2f}", f"{word_overlap_ratio_tigrigna:.2f}"] for word in shared_words] if shared_words else []
        elif choice == "Phoneme Level Overlap":
            headers = ["Shared Phonemes", "Amharic Ratio", "Tigrigna Ratio"]
            data = [[phoneme, f"{phoneme_overlap_ratio_amharic:.2f}", f"{phoneme_overlap_ratio_tigrigna:.2f}"] for phoneme in shared_phonemes] if shared_phonemes else []
        
        # Update the Treeview with the selected data
        display_table(tree, data, headers)
        # Adjust column widths
        for col in headers:
            max_length = max(len(str(value)) for row in data for value in row)
            tree.column(col, width=max_length * 10)  # Adjust width as needed
        
        # Ensure the Treeview is scrollable if necessary
        if len(data) > 10:  # Arbitrary number for scrolling; adjust as needed
            vsb.set(0.0, 1.0)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            vsb.pack_forget()

    def save_results():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                # Write overlap ratios
                file.write(result_text.get("1.0", tk.END))
                file.write("\n\n")
                
                # Write selected analysis results
                choice = combo_options.get()
                language = combo_language.get()
                file.write(f"Analysis: {choice}\n")
                file.write(f"Language: {language}\n\n")
                
                for child in tree.get_children():
                    values = tree.item(child)["values"]
                    file.write("\t".join(map(str, values)) + "\n")
                
                # Write phoneme conversion results
                file.write("\n\nPhoneme Conversion:\n")
                file.write(phoneme_text.get("1.0", tk.END))
            
            messagebox.showinfo("Save Successful", f"Results saved to {file_path}")

    def show_about():
        about_window = tk.Toplevel(root)
        about_window.title("About")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        about_text = """
        Amharic and Tigrigna Analyzer

        Version: 1.0
        
        This application analyzes Amharic and Tigrigna text and provides various analysis options.

        Features:
        - Analyze character frequencies
        - Analyze word frequencies
        - Compare phoneme distributions
        - Calculate character level overlaps
        - Calculate word level overlaps
        - Calculate phoneme level overlaps

        Developed by: Dagm yibabe
        Contact: dagimyibabe19@gmail.com
        telgram: @dag19yi

        © 2023 All rights reserved.
        """
        
        text_widget = tk.Text(about_window, wrap=tk.WORD, padx=20, pady=20)
        text_widget.pack(expand=True, fill=tk.BOTH)
        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)  # Make the text read-only

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(about_window, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)

    # Tkinter GUI setup
    root = ThemedTk(theme="arc")
    root.title("Amharic and Tigrigna Analyzer")
    root.geometry("1200x800")
    root.resizable(True, True)

    # Set background color
    root.configure(bg="#F0F0F0")  # Light gray

    # Menu bar
    menubar = tk.Menu(root, bg="#333333", fg="white")
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
    menubar.add_cascade(label="File", menu=file_menu, background="#333333", foreground="white")
    file_menu.add_command(label="Exit", command=root.quit)

    help_menu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
    menubar.add_cascade(label="Help", menu=help_menu, background="#333333", foreground="white")
    help_menu.add_command(label="About", command=show_about)

    # Main content frame
    main_frame = ttk.Frame(root, padding="20 20 20 20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Header
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 20))

    # Center the title
    header_frame.columnconfigure(0, weight=1)
    title_label = ttk.Label(header_frame, text="Amharic and Tigrigna Analyzer", 
                            font=("Helvetica", 24, "bold"))
    title_label.grid(row=0, column=0, pady=10)

    # Input fields for Amharic and Tigrigna texts
    input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10 10 10 10")
    input_frame.pack(fill=tk.X, pady=(0, 20))

    label_amharic = ttk.Label(input_frame, text="Amharic Text:")
    label_amharic.grid(row=0, column=0, padx=10, pady=5, sticky='e')
    entry_amharic = scrolledtext.ScrolledText(input_frame, width=40, height=3, font=("Arial", 12))
    entry_amharic.grid(row=0, column=1, padx=10, pady=5)

    label_tigrigna = ttk.Label(input_frame, text="Tigrigna Text:")
    label_tigrigna.grid(row=1, column=0, padx=10, pady=5, sticky='e')
    entry_tigrigna = scrolledtext.ScrolledText(input_frame, width=40, height=3, font=("Arial", 12))
    entry_tigrigna.grid(row=1, column=1, padx=10, pady=5)

    # Frame for buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)

    # Button to process text
    button_process = ttk.Button(button_frame, text="Process Text", command=process_text)
    button_process.pack(side=tk.LEFT, padx=10)

    # Save button
    button_save = ttk.Button(button_frame, text="Save Results", command=save_results)
    button_save.pack(side=tk.LEFT, padx=10)

    # Results frame with notebook
    frame_results = ttk.LabelFrame(main_frame, text="Results", padding="10 10 10 10")
    frame_results.pack_forget()  # Initially hidden

    notebook = ttk.Notebook(frame_results)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Tab for analysis options
    tab_analysis = ttk.Frame(notebook)
    notebook.add(tab_analysis, text="Analysis")

    frame_options = ttk.Frame(tab_analysis)
    frame_options.pack(pady=10)

    label_options = ttk.Label(frame_options, text="Choose Analysis Option:")
    label_options.grid(row=0, column=0, padx=10, pady=5, sticky='e')
    combo_options = ttk.Combobox(frame_options, width=30, font=("Arial", 12))
    combo_options.grid(row=0, column=1, padx=10, pady=5)

    label_language = ttk.Label(frame_options, text="Choose Language:")
    label_language.grid(row=1, column=0, padx=10, pady=5, sticky='e')
    combo_language = ttk.Combobox(frame_options, width=30, font=("Arial", 12))
    combo_language.grid(row=1, column=1, padx=10, pady=5)

    # Treeview for displaying data
    tree_frame = ttk.Frame(tab_analysis)
    tree_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(tree_frame, columns=[], show='headings')
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=vsb.set)

    # Result text widget for displaying overlap ratios
    result_text = tk.Text(tab_analysis, wrap=tk.WORD, height=12, width=50, font=("Arial", 12))
    result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Tab for phoneme conversion
    tab_phonemes = ttk.Frame(notebook)
    notebook.add(tab_phonemes, text="Phoneme Conversion")

    phoneme_text = scrolledtext.ScrolledText(tab_phonemes, wrap=tk.WORD, width=80, height=20)
    phoneme_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Dropdown menu options for analysis types
    options = ["Character Frequency", "Word Frequency", "Phoneme Distribution",
               "Character Level Overlap", "Word Level Overlap", "Phoneme Level Overlap"]
    combo_options['values'] = options
    combo_options.bind("<<ComboboxSelected>>", on_option_select)
    combo_language['values'] = ["Amharic", "Tigrigna"]
    combo_language.bind("<<ComboboxSelected>>", on_option_select)

    # Status bar
    status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
