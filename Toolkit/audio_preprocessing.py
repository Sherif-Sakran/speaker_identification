import os
from tkinter import Tk, Label, Button, filedialog, messagebox, ttk
from pydub import AudioSegment

# Function to select a folder
def select_directory():
    global source_path
    source_path = filedialog.askdirectory(title="Select Source Folder")
    if source_path:
        source_label.config(text=f"Source Folder: {source_path}")
    else:
        source_label.config(text="Source Folder: Not selected")

# Function to select the destination folder
def select_destination():
    global destination_path
    destination_path = filedialog.askdirectory(title="Select Destination Folder")
    if destination_path:
        destination_label.config(text=f"Destination: {destination_path}")
    else:
        destination_label.config(text="Destination: Not selected")

# Function to convert audio files in a folder to WAV with progress bar
def convert_to_wav():
    if not source_path:
        messagebox.showerror("Error", "Please select a source folder.")
        return
    if not destination_path:
        messagebox.showerror("Error", "Please select a destination folder.")
        return

    try:
        progress_bar["value"] = 0  # Reset progress bar
        files = []
        for root_dir, _, filenames in os.walk(source_path):  # Recursive file search
            files.extend(os.path.join(root_dir, f) for f in filenames if not f.lower().endswith(".wav"))
        total_files = len(files)

        if total_files == 0:
            messagebox.showerror("Error", "No audio files to convert.")
            return

        # Convert each file and update progress
        for i, file_path in enumerate(files):
            audio = AudioSegment.from_file(file_path)
            rel_path = os.path.relpath(file_path, source_path)
            output_path = os.path.join(destination_path, os.path.splitext(rel_path)[0] + ".wav")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure subdirectory structure
            audio.export(output_path, format="wav")

            # Update progress bar
            progress = (i + 1) / total_files * 100
            progress_bar["value"] = progress
            root.update_idletasks()  # Update the GUI

        messagebox.showinfo("Success", "Folder conversion completed!")
    except Exception as e:
        print("Error", f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function placeholder for Silence Removal tab
def remove_silence():
    messagebox.showinfo("Silence Removal", "This feature is under development.")

# Initialize main window
root = Tk()
root.title("Audio Preprocessing")

# Create notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Conversion tab
conversion_frame = ttk.Frame(notebook)
notebook.add(conversion_frame, text="Conversion")

Label(conversion_frame, text="Conversion", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

# Source selection buttons
Button(conversion_frame, text="Select Source Folder", command=select_directory).grid(row=1, column=0, pady=5, padx=10)
source_label = Label(conversion_frame, text="Source Folder: Not selected", anchor="w")
source_label.grid(row=1, column=1, pady=5, sticky="w")

# Destination selection
Button(conversion_frame, text="Select Destination Folder", command=select_destination).grid(row=2, column=0, pady=5, padx=10)
destination_label = Label(conversion_frame, text="Destination: Not selected", anchor="w")
destination_label.grid(row=2, column=1, pady=5, sticky="w")

# Progress bar
progress_bar = ttk.Progressbar(conversion_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

# Convert button
Button(conversion_frame, text="Convert to WAV", command=convert_to_wav, bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

# Silence Removal tab
silence_removal_frame = ttk.Frame(notebook)
notebook.add(silence_removal_frame, text="Silence Removal")

Label(silence_removal_frame, text="Silence Removal", font=("Arial", 16)).pack(pady=10)

# Placeholder for silence removal functionality
Button(silence_removal_frame, text="Remove Silence (Coming Soon)", command=remove_silence).pack(pady=20)

root.mainloop()
