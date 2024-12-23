import os
from tkinter import Tk, Label, Button, filedialog, messagebox, ttk, StringVar, Entry
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import noisereduce as nr
import scipy.io.wavfile as wav
import numpy as np

# Function to select a folder
def select_directory():
    global source_path
    source_path = filedialog.askdirectory(title="Select Source Folder")
    if source_path:
        source_label.config(text=f"Source Folder: .../{source_path.split('/')[-1]}")
    else:
        source_label.config(text="Source Folder: Not selected")

# Function to select the destination folder
def select_destination():
    global destination_path
    destination_path = filedialog.askdirectory(title="Select Destination Folder")
    if destination_path:
        destination_label.config(text=f"Destination: .../{destination_path.split('/')[-1]}")
    else:
        destination_label.config(text="Destination: Not selected", width=35)

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


def convert_to_format():
    """Convert audio files to the selected format."""
    if not source_path:
        messagebox.showerror("Error", "Please select a source folder.")
        return
    if not destination_path:
        messagebox.showerror("Error", "Please select a destination folder.")
        return
    
    # Get the selected output format
    output_format = output_format_var.get().strip()
    if not output_format:
        output_format = "wav"  # Default format

    try:
        progress_bar["value"] = 0  # Reset progress bar
        files = []
        for root_dir, _, filenames in os.walk(source_path):  # Recursive file search
            files.extend(os.path.join(root_dir, f) for f in filenames if not f.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')))
        total_files = len(files)

        if total_files == 0:
            messagebox.showerror("Error", "No audio files to convert.")
            return

        # Convert each file and update progress
        for i, file_path in enumerate(files):
            audio = AudioSegment.from_file(file_path)
            rel_path = os.path.relpath(file_path, source_path)
            output_path = os.path.join(destination_path, os.path.splitext(rel_path)[0] + "." + output_format)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure subdirectory structure
            audio.export(output_path, format=output_format)

            # Update progress bar
            progress = (i + 1) / total_files * 100
            progress_bar["value"] = progress
            root.update_idletasks()  # Update the GUI

        messagebox.showinfo("Success", "Folder conversion completed!")
    except Exception as e:
        print("Error", f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to select a folder for silence removal
def select_directory_silence():
    global source_path_silence
    source_path_silence = filedialog.askdirectory(title="Select Source Folder")
    if source_path_silence:
        source_label_silence.config(text=f"Source Folder: .../{source_path_silence.split('/')[-1]}")
    else:
        source_label_silence.config(text="Source Folder: Not selected")

# Function to select the destination folder for silence removal
def select_destination_silence():
    global destination_path_silence
    destination_path_silence = filedialog.askdirectory(title="Select Destination Folder")
    if destination_path_silence:
        destination_label_silence.config(text=f"Destination: .../{destination_path_silence.split('/')[-1]}")
    else:
        destination_label_silence.config(text="Destination: Not selected", width=35)

# Function to remove silence from audio files
def remove_silence_from_files():
    if not source_path_silence:
        messagebox.showerror("Error", "Please select a source folder.")
        return
    if not destination_path_silence:
        messagebox.showerror("Error", "Please select a destination folder.")
        return

    try:
        silence_threshold = silence_thresh_var.get()
        if not silence_threshold.strip():
            messagebox.showerror("Error", "Please enter a valid silence threshold (e.g., -50).")
            return

        silence_threshold = int(silence_threshold)

        progress_bar_silence["value"] = 0  # Reset progress bar
        files = []
        for root_dir, _, filenames in os.walk(source_path_silence):  # Recursive file search
            files.extend(os.path.join(root_dir, f) for f in filenames if f.lower().endswith((".wav", ".mp3", ".flac")))
        total_files = len(files)

        if total_files == 0:
            messagebox.showerror("Error", "No audio files to process.")
            return

        # Process each file and remove silence
        for i, file_path in enumerate(files):
            audio = AudioSegment.from_file(file_path)

            # Detect non-silent chunks
            nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=silence_threshold)
            if nonsilent_ranges:
                # Combine non-silent chunks
                processed_audio = sum(audio[start:end] for start, end in nonsilent_ranges)

                # Save the processed audio
                rel_path = os.path.relpath(file_path, source_path_silence)
                output_path = os.path.join(destination_path_silence, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                processed_audio.export(output_path, format="wav")
            else:
                print(f"File {file_path} contains only silence and was skipped.")

            # Update progress bar
            progress = (i + 1) / total_files * 100
            progress_bar_silence["value"] = progress
            root.update_idletasks()  # Update the GUI

        messagebox.showinfo("Success", "Silence removal completed!")
    except Exception as e:
        print("Error", f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to select a folder for segmentation
def select_directory_segmentation():
    global source_path_segmentation
    source_path_segmentation = filedialog.askdirectory(title="Select Source Folder")
    if source_path_segmentation:
        source_label_segmentation.config(text=f"Source Folder: .../{source_path_segmentation.split('/')[-1]}")
    else:
        source_label_segmentation.config(text="Source Folder: Not selected")

# Function to select the destination folder for segmentation
def select_destination_segmentation():
    global destination_path_segmentation
    destination_path_segmentation = filedialog.askdirectory(title="Select Destination Folder")
    if destination_path_segmentation:
        destination_label_segmentation.config(text=f"Destination: .../{destination_path_segmentation.split('/')[-1]}")
    else:
        destination_label_segmentation.config(text="Destination: Not selected", width=35)

# Function to segment audio files
def segment_audio_files():
    if not source_path_segmentation:
        messagebox.showerror("Error", "Please select a source folder.")
        return
    if not destination_path_segmentation:
        messagebox.showerror("Error", "Please select a destination folder.")
        return

    try:
        # Get utterance length from entry
        utterance_length = int(utterance_length_var.get())
        if utterance_length <= 0:
            messagebox.showerror("Error", "Please enter a valid utterance length.")
            return

        progress_bar_segmentation["value"] = 0  # Reset progress bar
        files = []
        for root_dir, _, filenames in os.walk(source_path_segmentation):  # Recursive file search
            files.extend(os.path.join(root_dir, f) for f in filenames if f.lower().endswith((".wav", ".mp3", ".flac")))
        total_files = len(files)

        if total_files == 0:
            messagebox.showerror("Error", "No audio files to segment.")
            return

        # Process each file and segment it
        for i, file_path in enumerate(files):
            audio = AudioSegment.from_file(file_path)
            total_duration = len(audio) / 1000  # Duration in seconds

            # Create a folder for the segments
            rel_path = os.path.relpath(file_path, source_path_segmentation)
            file_name = os.path.splitext(rel_path)[0]
            output_folder = os.path.join(destination_path_segmentation, file_name)
            os.makedirs(output_folder, exist_ok=True)

            # Segment the audio
            for j in range(0, int(total_duration), utterance_length):
                segment = audio[j * 1000: (j + utterance_length) * 1000]  # Convert to milliseconds
                segment.export(os.path.join(output_folder, f"{file_name}_{j // utterance_length + 1}.wav"), format="wav")

            # Update progress bar
            progress = (i + 1) / total_files * 100
            progress_bar_segmentation["value"] = progress
            root.update_idletasks()  # Update the GUI

        messagebox.showinfo("Success", "Segmentation completed!")
    except Exception as e:
        print("Error", f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")


def select_source_directory_trimmer():
    """Select source directory for Trimmer."""
    global source_folder_trimmer
    source_folder_trimmer = filedialog.askdirectory()
    source_label_trimmer.config(text=f"Source Folder: .../{source_folder_trimmer.split('/')[-1]}")


def select_destination_directory_trimmer():
    """Select destination directory for Trimmer."""
    global destination_folder_trimmer
    destination_folder_trimmer = filedialog.askdirectory()
    destination_label_trimmer.config(text=f"Destination: .../{destination_folder_trimmer.split('/')[-1]}")


def trim_utterances():
    """Trim audio files to the specified length."""
    if not source_folder_trimmer or not destination_folder_trimmer:
        messagebox.showwarning("Warning", "Please select both source and destination folders!")
        return

    try:
        utterance_length = float(utterance_length_var.get())
        if utterance_length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid utterance length! Please enter a positive number.")
        return

    # Get all audio files (including from subfolders)
    audio_files = []
    for root_dir, _, files in os.walk(source_folder_trimmer):
        audio_files.extend([os.path.join(root_dir, f) for f in files if f.lower().endswith(('.mp3', '.wav', '.ogg', '.flac'))])

    progress_bar_trimmer["maximum"] = len(audio_files)
    progress_bar_trimmer["value"] = 0

    for idx, file_path in enumerate(audio_files):
        try:
            audio = AudioSegment.from_file(file_path)
            trimmed_audio = audio[:utterance_length * 1000]  # Convert seconds to milliseconds

            # Ensure subfolder structure is maintained
            relative_path = os.path.relpath(file_path, source_folder_trimmer)
            dest_path = os.path.join(destination_folder_trimmer, relative_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Save the trimmed audio
            trimmed_audio.export(dest_path, format=os.path.splitext(dest_path)[1][1:])
            progress_bar_trimmer["value"] += 1
            root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to trim {file_path}: {e}")

    messagebox.showinfo("Success", "Trimming completed successfully!")


def select_source_directory_noise_reduction():
    """Select source directory for Noise Reduction."""
    global source_folder_noise_reduction
    source_folder_noise_reduction = filedialog.askdirectory()
    source_label_noise_reduction.config(text=f"Source Folder: .../{source_folder_noise_reduction.split('/')[-1]}")


def select_destination_directory_noise_reduction():
    """Select destination directory for Noise Reduction."""
    global destination_folder_noise_reduction
    destination_folder_noise_reduction = filedialog.askdirectory()
    destination_label_noise_reduction.config(text=f"Destination: .../{destination_folder_noise_reduction.split('/')[-1]}")


def reduce_noise():
    """Reduce noise in audio files."""
    if not source_folder_noise_reduction or not destination_folder_noise_reduction:
        messagebox.showwarning("Warning", "Please select both source and destination folders!")
        return

    # Get all audio files (including from subfolders)
    audio_files = []
    for root_dir, _, files in os.walk(source_folder_noise_reduction):
        audio_files.extend([os.path.join(root_dir, f) for f in files if f.lower().endswith(('.wav'))])

    if not audio_files:
        messagebox.showwarning("Warning", "No WAV files found in the source folder!")
        return

    progress_bar_noise_reduction["maximum"] = len(audio_files)
    progress_bar_noise_reduction["value"] = 0

    for idx, file_path in enumerate(audio_files):
        try:
            rate, data = wav.read(file_path)

            # Handle stereo by converting to mono
            if len(data.shape) > 1:
                data = data.mean(axis=1).astype(np.int16)

            reduced_noise = nr.reduce_noise(y=data.astype(float), sr=rate)

            # Ensure subfolder structure is maintained
            relative_path = os.path.relpath(file_path, source_folder_noise_reduction)
            dest_path = os.path.join(destination_folder_noise_reduction, relative_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            wav.write(dest_path, rate, reduced_noise.astype(np.int16))

            # Update progress bar
            progress_bar_noise_reduction["value"] += 1
            root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process {file_path}: {e}")

    messagebox.showinfo("Success", "Noise reduction completed successfully!")

def select_source_directory_audio_normalization():
    """Select source directory for Audio Normalization."""
    global source_folder_audio_normalization
    source_folder_audio_normalization = filedialog.askdirectory()
    source_label_audio_normalization.config(text=f"Source Folder: .../{source_folder_audio_normalization.split('/')[-1]}")


def select_destination_directory_audio_normalization():
    """Select destination directory for Audio Normalization."""
    global destination_folder_audio_normalization
    destination_folder_audio_normalization = filedialog.askdirectory()
    destination_label_audio_normalization.config(text=f"Destination: .../{destination_folder_audio_normalization.split('/')[-1]}")


def normalize_audio_files():
    """Normalize volume of audio files."""
    if not source_folder_audio_normalization or not destination_folder_audio_normalization:
        messagebox.showwarning("Warning", "Please select both source and destination folders!")
        return

    # Get all audio files (including from subfolders)
    audio_files = []
    for root_dir, _, files in os.walk(source_folder_audio_normalization):
        audio_files.extend([os.path.join(root_dir, f) for f in files if f.lower().endswith(('.wav'))])

    if not audio_files:
        messagebox.showwarning("Warning", "No WAV files found in the source folder!")
        return

    progress_bar_audio_normalization["maximum"] = len(audio_files)
    progress_bar_audio_normalization["value"] = 0

    for idx, file_path in enumerate(audio_files):
        try:
            # Load audio file
            audio = AudioSegment.from_file(file_path)

            # Normalize audio
            normalized_audio = audio.normalize()

            # Ensure subfolder structure is maintained
            relative_path = os.path.relpath(file_path, source_folder_audio_normalization)
            dest_path = os.path.join(destination_folder_audio_normalization, relative_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Save normalized audio
            normalized_audio.export(dest_path, format="wav")

            # Update progress bar
            progress_bar_audio_normalization["value"] += 1
            root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process {file_path}: {e}")

    messagebox.showinfo("Success", "Audio normalization completed successfully!")


button_bg_color = "green"
button_fg_color = "white"
progress_bar_length = 500

tab_title_order = 0
source_directory_order = 1
destination_directory_order = 2
input_field_order = 3
progress_bar_order = 4
button_order = 5

# Initialize main window
root = Tk()
root.title("Audio Preprocessing")

# Create notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Conversion tab
conversion_frame = ttk.Frame(notebook)
notebook.add(conversion_frame, text="Conversion")


Label(conversion_frame, text="Format Conversion", font=("Arial", 16)).grid(row=tab_title_order, column=0, columnspan=2, pady=10)

# Source selection
Button(conversion_frame, text="Select Source Folder", command=select_directory).grid(row=source_directory_order, column=0, pady=5, padx=10)
source_label = Label(conversion_frame, text="Source Folder: Not selected")
source_label.grid(row=1, column=1)

# Destination selection
Button(conversion_frame, text="Select Destination Folder", command=select_destination).grid(row=destination_directory_order, column=0, pady=5, padx=10)
destination_label = Label(conversion_frame, text="Destination: Not selected", width=35)
destination_label.grid(row=2, column=1)

# Output format input
Label(conversion_frame, text="Output Format:").grid(row=input_field_order, column=0)
output_format_var = StringVar(value="wav")
Entry(conversion_frame, textvariable=output_format_var).grid(row=input_field_order, column=1)

# Progress bar
progress_bar = ttk.Progressbar(conversion_frame, length=progress_bar_length, mode="determinate")
progress_bar.grid(row=progress_bar_order, column=0, columnspan=2, pady=10, padx=10)

# Convert button
Button(conversion_frame, text="Convert", command=convert_to_format, bg=button_bg_color, fg=button_fg_color, width=15).grid(row=button_order, column=0, pady=10, columnspan=2)

# Silence removal tab
silence_frame = ttk.Frame(notebook)
notebook.add(silence_frame, text="Silence Removal")

Label(silence_frame, text="Silence Removal", font=("Arial", 16)).grid(row=tab_title_order, column=0, columnspan=2, pady=10)

# Source selection for silence removal
Button(silence_frame, text="Select Source Folder", command=select_directory_silence).grid(row=source_directory_order, column=0, pady=5, padx=10)
source_label_silence = Label(silence_frame, text="Source Folder: Not selected")
source_label_silence.grid(row=source_directory_order, column=1)

# Destination selection for silence removal
Button(silence_frame, text="Select Destination Folder", command=select_destination_silence).grid(row=destination_directory_order, column=0, pady=5, padx=10)
destination_label_silence = Label(silence_frame, text="Destination: Not selected", width=35)
destination_label_silence.grid(row=destination_directory_order, column=1)

# Silence threshold entry
Label(silence_frame, text="Silence Threshold:").grid(row=input_field_order, column=0)
silence_thresh_var = StringVar(value='-50')
Entry(silence_frame, textvariable=silence_thresh_var).grid(row=input_field_order, column=1)

# Remove silence button
Button(silence_frame, text="Remove Silence", command=remove_silence_from_files, bg=button_bg_color, fg=button_fg_color, width=15).grid(row=button_order, column=0, pady=10, columnspan=2)

# Progress bar for silence removal
progress_bar_silence = ttk.Progressbar(silence_frame, length=progress_bar_length, mode="determinate")
progress_bar_silence.grid(row=progress_bar_order, column=0, columnspan=2, pady=10, padx=10)

# Segmentation tab
segmentation_frame = ttk.Frame(notebook)
notebook.add(segmentation_frame, text="Segmentation")

Label(segmentation_frame, text="Audio Segmentation", font=("Arial", 16)).grid(row=tab_title_order, column=0, columnspan=2, pady=10)

# Utterance length entry
Label(segmentation_frame, text="Utterance Length (s):").grid(row=input_field_order, column=0)
utterance_length_var = StringVar(value='3')
Entry(segmentation_frame, textvariable=utterance_length_var).grid(row=input_field_order, column=1)

# Source selection for segmentation
Button(segmentation_frame, text="Select Source Folder", command=select_directory_segmentation).grid(row=source_directory_order, column=0, pady=5, padx=10)
source_label_segmentation = Label(segmentation_frame, text="Source Folder: Not selected")
source_label_segmentation.grid(row=source_directory_order, column=1)

# Destination selection for segmentation
Button(segmentation_frame, text="Select Destination Folder", command=select_destination_segmentation).grid(row=destination_directory_order, column=0, pady=5, padx=10)
destination_label_segmentation = Label(segmentation_frame, text="Destination: Not selected", width=35)
destination_label_segmentation.grid(row=destination_directory_order, column=1)

# Progress bar for segmentation
progress_bar_segmentation = ttk.Progressbar(segmentation_frame, length=progress_bar_length, mode="determinate")
progress_bar_segmentation.grid(row=progress_bar_order, column=0, columnspan=2, pady=10, padx=10)

# Segment audio button
Button(segmentation_frame, text="Segment Audio", command=segment_audio_files, bg=button_bg_color, fg=button_fg_color, width=15).grid(row=button_order, column=0, pady=10, columnspan=2)

# Trimmer tab
trimmer_frame = ttk.Frame(notebook)
notebook.add(trimmer_frame, text="Trimmer")

Label(trimmer_frame, text="Utterance Trimmer", font=("Arial", 16)).grid(row=tab_title_order, column=0, columnspan=2, pady=10)

Button(trimmer_frame, text="Select Source Folder", command=select_source_directory_trimmer).grid(row=source_directory_order, column=0, pady=5, padx=10)
source_label_trimmer = Label(trimmer_frame, text="Source Folder: Not selected")
source_label_trimmer.grid(row=source_directory_order, column=1)

Button(trimmer_frame, text="Select Destination Folder", command=select_destination_directory_trimmer).grid(row=destination_directory_order, column=0, pady=5, padx=10)
destination_label_trimmer = Label(trimmer_frame, text="Destination: Not selected", width=35)
destination_label_trimmer.grid(row=destination_directory_order, column=1)

Label(trimmer_frame, text="Utterance Length (s):").grid(row=input_field_order, column=0)
utterance_length_var = StringVar(value="3")
Entry(trimmer_frame, textvariable=utterance_length_var).grid(row=input_field_order, column=1)

progress_bar_trimmer = ttk.Progressbar(trimmer_frame, length=progress_bar_length, mode="determinate")
progress_bar_trimmer.grid(row=progress_bar_order, column=0, columnspan=2, pady=10, padx=10)

Button(trimmer_frame, text="Trim", command=trim_utterances, bg=button_bg_color, fg=button_fg_color, width=15).grid(row=button_order, column=0, columnspan=2, pady=10)

# Noise Reduction Tab
noise_reduction_frame = ttk.Frame(notebook)
notebook.add(noise_reduction_frame, text="Noise Reduction")

Label(noise_reduction_frame, text="Noise Reduction", font=("Arial", 16)).grid(row=tab_title_order, column=0, columnspan=2, pady=10)

Button(noise_reduction_frame, text="Select Source Folder", command=select_source_directory_noise_reduction).grid(row=source_directory_order, column=0, pady=5, padx=10)
source_label_noise_reduction = Label(noise_reduction_frame, text="Source Folder: Not selected")
source_label_noise_reduction.grid(row=source_directory_order, column=1)

Button(noise_reduction_frame, text="Select Destination Folder", command=select_destination_directory_noise_reduction).grid(row=destination_directory_order, column=0, pady=5, padx=10)
destination_label_noise_reduction = Label(noise_reduction_frame, text="Destination: Not selected", width=35)
destination_label_noise_reduction.grid(row=destination_directory_order, column=1)
Label(noise_reduction_frame, text="").grid(row=input_field_order, column=0)

progress_bar_noise_reduction = ttk.Progressbar(noise_reduction_frame, length=progress_bar_length, mode="determinate")
progress_bar_noise_reduction.grid(row=progress_bar_order, column=0, columnspan=2, pady=10, padx=10)

Button(noise_reduction_frame, text="Reduce Noise", command=reduce_noise, bg=button_bg_color, fg=button_fg_color, width=15).grid(row=button_order, column=0, columnspan=2, pady=10)

# Audio Normalization Tab
audio_normalization_frame = ttk.Frame(notebook)
notebook.add(audio_normalization_frame, text="Audio Normalization")

Label(audio_normalization_frame, text="Audio Normalization", font=("Arial", 16)).grid(row=tab_title_order, column=0, columnspan=2, pady=10)

Button(audio_normalization_frame, text="Select Source Folder", command=select_source_directory_audio_normalization).grid(row=source_directory_order, column=0, pady=5, padx=10)
source_label_audio_normalization = Label(audio_normalization_frame, text="Source Folder: Not selected", width=35)
source_label_audio_normalization.grid(row=source_directory_order, column=1)

Button(audio_normalization_frame, text="Select Destination Folder", command=select_destination_directory_audio_normalization).grid(row=destination_directory_order, column=0, pady=5, padx=10)
destination_label_audio_normalization = Label(audio_normalization_frame, text="Destination: Not selected", width=35)
destination_label_audio_normalization.grid(row=destination_directory_order, column=1)
Label(audio_normalization_frame, text="").grid(row=input_field_order, column=0)

progress_bar_audio_normalization = ttk.Progressbar(audio_normalization_frame, length=progress_bar_length, mode="determinate")
progress_bar_audio_normalization.grid(row=progress_bar_order, column=0, columnspan=2, pady=10, padx=10)

Button(audio_normalization_frame, text="Normalize Audio", command=normalize_audio_files, bg=button_bg_color, fg=button_fg_color, width=15).grid(row=button_order, column=0, columnspan=2, pady=10)

root.mainloop()
