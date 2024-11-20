import librosa
import numpy as np
import pandas as pd

import sys
import os


segmented_dataset_path = './pipeline/3-segmented_dataset_wav/'
dest_dataset_path = './pipeline/4-mfccs_dataset/'


# directory_name = sys.argv[1]
directory_name = "Sherif"

src_directory_path = f'{segmented_dataset_path}{directory_name}/'
dest_directory_path = f'{dest_dataset_path}{directory_name}/'

google_drive = False
if google_drive:
    src_directory_path = '/content/drive/MyDrive/thesis_models/' + src_directory_path
    dest_dataset_path = '/content/drive/MyDrive/thesis_models/' + dest_dataset_path
    dest_directory_path = '/content/drive/MyDrive/thesis_models/' + dest_directory_path

if not os.path.exists(dest_directory_path):
    os.makedirs(dest_directory_path)
    print(f"Directory '{dest_directory_path}' created successfully.")
else:
    print(f"Directory '{dest_directory_path}' already exists.")

directory_path = src_directory_path
output_path = dest_directory_path
output_path
file_names = os.listdir(directory_path)
file_names
# # columns = [f'MFCC {i}' for i in range(1, 21)]
# # columns.append('Speaker')
# # df = pd.DataFrame(columns=columns)
# vectors = []
# i = 1
# for file_name in file_names:
#   if file_name.split('.')[-1] != "m4a":
#     continue
#   file_path = directory_path + file_name
#   signal, sr = librosa.load(file_path, duration=3)
#   mfccs = librosa.feature.mfcc(y=signal, n_mfcc=20, sr=sr)
#   # mfcc_vector = get_mfccs_mean_vector(mfccs)
#   # mfcc_vector = np.append(mfcc_vector, speaker)
#   mfcc_vector = mfccs
#   vectors.append(mfcc_vector)
#   i += 1

# librosa.display.specshow(vectors[9], sr=sr)

# columns = [f'MFCC {i}' for i in range(1, 21)]
# columns.append('Speaker')
# df = pd.DataFrame(columns=columns)
speaker = directory_name
i = 0
for file_name in file_names:
    i += 1
    if file_name.split('.')[-1] != "wav":
        continue
    file_path = directory_path + file_name
    signal, sr = librosa.load(file_path, duration=5)
    print("reached the load method")
    mfccs = librosa.feature.mfcc(y=signal, n_mfcc=22, sr=sr)
    # mfcc_vector = get_mfccs_mean_vector(mfccs)
    # mfcc_vector = np.append(mfcc_vector, speaker)
    mfcc_vector = mfccs
    df = pd.DataFrame(mfcc_vector)
    df.to_csv(f'{output_path}{speaker}_{i}.csv', index=False)
    df = pd.read_csv(f'{output_path}{speaker}_{i}.csv')
df