import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.layers import BatchNormalization, Dropout
import tensorflow as tf
import matplotlib.pyplot as plt
import pickle
import time


# Function to read and preprocess data from a directory
def read_and_preprocess_data(directory):
    class_data = []
    labels = []

    for class_label, class_name in enumerate(os.listdir(directory)):
        class_path = os.path.join(directory, class_name)
        for file_name in os.listdir(class_path):
            file_path = os.path.join(class_path, file_name)
            df = pd.read_csv(file_path)
            # print(df)
            # Assuming each CSV file contains a 20x129 2D array
            class_data.append(df.values)
            labels.append(class_name)

    return class_data, labels

# def cnn_model(classes_num):
#     model = Sequential()
#     model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(22, 216)))
#     model.add(MaxPooling1D(pool_size=2))
#     model.add(Flatten())
#     model.add(Dense(128, activation='relu'))
#     model.add(Dense(classes_num, activation='softmax'))
#     return model

def cnn_model(classes_num):
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(22, 216)))
    model.add(BatchNormalization())  # Batch normalization added
    model.add(MaxPooling1D(pool_size=2))
    model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())  # Batch normalization added
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))  # Dropout layer added
    model.add(Dense(classes_num, activation='softmax'))
    return model

def complex_cnn_model(classes_num):
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(22, 216)))
    model.add(BatchNormalization())  # Batch normalization added
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))  # Dropout layer added
    model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())  # Batch normalization added
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))  # Dropout layer added
    model.add(Conv1D(filters=256, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())  # Batch normalization added
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))  # Dropout layer added
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(classes_num, activation='softmax'))
    return model

def fully_connected(classes_num):
    model = Sequential()
    model.add(Flatten(input_shape=(22, 216)))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(classes_num, activation='softmax'))
    return model

# Conv-1 7 × 7 32 2 × 2 32 × 17 × 47
# Conv-2 5 × 5 64 1 × 1 64 × 13 × 43
# Conv-3 3 × 3 128 1 × 1 128 × 11 × 41
# Conv-4 3 × 3 256 1 × 1 256 × 9 × 39
# Conv-5 3 × 3 256 1 × 1 256 × 7 × 37
# fc-1 - 1024 - -
# fc-2 - 256 - -
# fc-3 - 1251 - -

def cnn_model_2(classes_num):
    model = Sequential()
    model.add(Conv1D(filters=32, kernel_size=7, strides=2, activation='relu', input_shape=(22, 216)))
    model.add(Conv1D(filters=64, kernel_size=5, strides=1, activation='relu'))
    model.add(Conv1D(filters=128, kernel_size=3, strides=1, activation='relu'))
    model.add(BatchNormalization())  # Batch normalization added
    # model.add(Dropout(0.25))  # Dropout layer added
    # model.add(Conv1D(filters=256, kernel_size=3, strides=1, activation='relu'))
    # model.add(Conv1D(filters=256, kernel_size=3, strides=1, activation='relu'))
    # model.add(BatchNormalization())  # Batch normalization added
    # model.add(MaxPooling1D(pool_size=2))
    # model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))  # Dropout layer added
    model.add(Flatten())
    model.add(Dropout(0.25))  # Dropout layer added
    model.add(Dense(1024, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))  # Dropout layer added
    model.add(Dense(128, activation='relu'))
    # model.add(Dense(1024, activation='relu'))
    model.add(Dense(classes_num, activation='softmax'))
    return model

def cnn_for_speaker_identification(classes_num):
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(22, 216)))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))

    model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    # model.add(BatchNormalization())
    model.add(Dropout(0.25))
    model.add(Dense(classes_num, activation='softmax'))
    return model

if __name__ == "__main__":
    # Load training data
    training_directory = "./pipeline/4-mfccs_dataset/training/"

    classes_num = len(os.listdir(training_directory))
    X_train, y_train = read_and_preprocess_data(training_directory)

    # Convert lists to numpy arrays
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    # One-hot encode labels
    label_encoder = LabelEncoder()
    y_train = to_categorical(label_encoder.fit_transform(y_train))

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    # Define the CNN model
    # model = fully_connected(classes_num)
    # model = cnn_model(classes_num)
    # model = cnn_model_2(classes_num)
    # model = complex_cnn_model(classes_num)
    model = cnn_for_speaker_identification(classes_num)

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Display the model summary
    print(model.summary())


    # Train the model
    logdir='logs'
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
    time1 = time.time()
    hist = model.fit(X_train, y_train, epochs=100, batch_size=8, validation_data=(X_val, y_val))
    print(f"time taken for training: {time.time() - time1} seconds")
    # model.fit(X_train, y_train, epochs=100, batch_size=32)
    val_accuracy = hist.history['val_accuracy'][-1]
    
    model.save(f'./pipeline/5-generated_models/speaker_identifier.h5')

    # Save the label encoder
    with open(f'./pipeline/5-generated_models/speaker_identifier.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    

    # fig = plt.figure()
    # plt.plot(hist.history['loss'], color='teal', label='loss')
    # plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
    # fig.suptitle('Loss', fontsize=20)
    # plt.legend(loc="upper left")
    # plt.show()
    # fig = plt.figure()
    # plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
    # plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
    # fig.suptitle('Accuracy', fontsize=20)
    # plt.legend(loc="upper left")
    # plt.show()

