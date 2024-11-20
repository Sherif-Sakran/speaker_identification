from scipy.io import wavfile
import numpy as np
import os
import sys

def trim_wav(input_file, output_folder, segment_name, offset=0):
    # Read the WAV file
    sample_rate, audio_data = wavfile.read(input_file)

    # Define the duration of each segment in samples (5 seconds)
    segment_duration = 5 * sample_rate

    # Calculate the number of segments
    num_segments = len(audio_data) // segment_duration
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Trim the audio into segments
    for i in range(num_segments):
        start_sample = i * segment_duration
        end_sample = (i + 1) * segment_duration
        segment = audio_data[start_sample:end_sample]
        # Save each segment as a separate WAV file
        output_file = os.path.join(output_folder, f"{segment_name}_{i+1+offset}.wav")
        wavfile.write(output_file, sample_rate, segment)


if __name__ == "__main__":

    file_name = sys.argv[1] + '_enrollment.wav'
    # file_name = "hi_enrollment.wav"

    src_directory_path = './pipeline/2-preprocessed_dataset_wav/'
    dest_directory_path = './pipeline/3-segmented_dataset_wav/'


    input_wavfile = os.path.join(src_directory_path, file_name)
    segment_name = file_name.split('.')[0].split('_')[0]
    offset = 0 # counter starts at 1 + offset (for assembling a person's class from different recordings)
    output_folder = dest_directory_path + file_name.split('_')[0]
    output_folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Directory '{output_folder}' created successfully.")
    else:
        print(f"Directory '{output_folder}' already exists.")

    trim_wav(input_wavfile, output_folder, segment_name, offset)