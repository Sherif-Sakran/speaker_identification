import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GMM
from FeatureExtraction import extract_features
#from speakerfeatures import extract_features
import warnings
import os
import sys
warnings.filterwarnings("ignore")

coeffecients22 = True
preprocessed = False
training = True
notNormalized = False
dest = "4-gmm_models"

if not preprocessed:
    if training:
        mfcc_dir = "./3-mfcc_training"
        source   = "2-wav_training"   
    # else:
    #     mfcc_dir = "./3-mfcc_testing"
    #     source   = "2-wav_testing"

    if notNormalized:
        dest = dest + "_unnormalized/"
        mfcc_dir = mfcc_dir + "_unnormalized/"
        source = source + "_unnormalized/"
    else:
        dest = dest + "/"
        mfcc_dir = mfcc_dir + "/"
        source = source + "/"

    if notNormalized:
        dest = dest + "_unnormalized/"
        mfcc_dir = mfcc_dir + "_unnormalized/"
        source = source + "_unnormalized/"
    # else:
    #     dest = dest + "/"
    #     mfcc_dir = mfcc_dir + "/"
    #     source = source + "/"

else:
    dest = "4-gmm_models_preprocessed/"
    if training:
        source   = "3-wav_training_noise_preprocessed/"   
    else:
        source   = "3-wav_testing_noise_preprocessed/"

if coeffecients22:
    dest = "./4-new_test_22_coeffecients/" + dest

directories = os.listdir(source)
print(directories)
for directory in directories:
    # 1 speaker
    # directory = directories[0]

    # List all files in the directory
    file_paths = os.listdir(source + directory)
    # print(file_paths)
    # Extracting features for each speaker (5 files per speakers)
    features = np.asarray(())
    for path in file_paths:
        path = directory + "/" + path    
        path = path.strip()   
        print (path)
        
        # read the audio
        sr,audio = read(source+path)
        
        # extract 40 dimensional MFCC & delta MFCC features
        vector   = extract_features(audio,sr)
        
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
        print(features.shape)
        # when features of 5 files of speaker are concatenated, then do model training
        # -> if count == 5: --> edited below

        # speaker_dir = mfcc_dir + directory
        # speaker_name = path.split("/")[1].split(".")[0]

        # if not os.path.exists(speaker_dir):
        #     os.makedirs(speaker_dir)
        # # Assuming 'features' is the 2D array containing the features
        # csv_path = speaker_dir + "/" + speaker_name + ".csv"
        # np.savetxt(csv_path, vector, delimiter=",")
        # print("Features saved to", csv_path)
        

    if training:            
        gmm = GMM(n_components = 5, covariance_type='diag',n_init = 3)
        gmm.fit(features)
        # dumping the trained gaussian model
        picklefile = directory + ".gmm"
        
        cPickle.dump(gmm,open(dest + picklefile,'wb'))
        print ('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)   
        features = np.asarray(())
