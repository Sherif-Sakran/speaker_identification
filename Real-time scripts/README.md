### 1. Enrolling speakers
The enrollment process includes both creating the speakers' models of the audio recordings in the directory "speaker_identification/enrolment_recordings/" this is done by running the script enrol_speaker.py

### 2. Removing speakers (if needed)
This removes the GMM speaker model of the specified speaker, and it re-trains the neural network after removing this speaker (if train_CNN flag is True). This is done by running the script remove_speaker.py

### 3. Testing in real time
The real_time_backend_testing.py script recognizes the persons enrolled earlier using two different models: GMM and CNN.

### 4. Real-time testing
This part utilizes the GMM and CNN to recognize the previously enrolled speakers. This is done through the real_time_testing.py
