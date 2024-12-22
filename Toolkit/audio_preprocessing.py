import os
from tkinter import Tk, Label, Button, filedialog, messagebox
from tkinter import ttk
from pydub import AudioSegment

def select_directory():
    global source_path
    source_path = filedialog.askdirectory(title="Select Source Folder")
    if source_path:
        source_label.config(text=f"Source Folder: {source_path}")
    else:
        source_label.config(text="Source Folder: Not selected")

def select_destination():
    global destination_path
    destination_path = filedialog.askdirectory(title="Select Destination Folder")
    if destination_path:
        destination_label.config(text=f"Destination: {destination_path}")
    else:
        destination_label.config(text="Destination: Not selected")

def convert_to_wav():
    if not source_path:
        messagebox.showerror("Error", "Please select a source folder.")
        return
    if not destination_path:
        messagebox.showerror("Error", "Please select a destination folder.")
        return

    try:
        progress_bar["value"] = 0
        files = []
        
        for root_dir, _, files_in_folder in os.walk(source_path):
            for file in files_in_folder:
                file_path = os.path.join(root_dir, file)
                if not file.lower().endswith(".wav"):
                    files.append(file_path)

        total_files = len(files)

        if total_files == 0:
            messagebox.showerror("Error", "No audio files to convert.")
            return

        for i, file_path in enumerate(files):
            try:
                audio = AudioSegment.from_file(file_path)
                
                relative_path = os.path.relpath(os.path.dirname(file_path), source_path)
                output_dir = os.path.join(destination_path, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                output_file = os.path.splitext(os.path.basename(file_path))[0] + ".wav"
                output_path = os.path.join(output_dir, output_file)

                audio.export(output_path, format="wav")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

            progress = (i + 1) / total_files * 100
            progress_bar["value"] = progress
            root.update_idletasks()

        messagebox.showinfo("Success", "Folder conversion completed!")
    except Exception as e:
        print("Error", f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

root = Tk()
root.title("Audio Preprocessing")

source_path = ""
destination_path = ""

Label(root, text="Audio Preprocessing", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

Button(root, text="Select Source Folder", command=select_directory).grid(row=1, column=0, pady=5, padx=10)
source_label = Label(root, text="Source Folder: Not selected", anchor="w")
source_label.grid(row=1, column=1, pady=5, sticky="w")

Button(root, text="Select Destination Folder", command=select_destination).grid(row=2, column=0, pady=5, padx=10)
destination_label = Label(root, text="Destination: Not selected", anchor="w")
destination_label.grid(row=2, column=1, pady=5, sticky="w")

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

Button(root, text="Convert to WAV", command=convert_to_wav, bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
