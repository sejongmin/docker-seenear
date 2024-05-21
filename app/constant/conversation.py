# emotion_classification.py constant
EMOTION_MODEL = 'media/Speech-Emotion-Recognition-Model.h5'
N_MFCC = 13
N_FFT = 2048
HOP_LENGTH = 512
SAMPLE_RATE = 22050
MAX_LENGTH = 100

# emotion_calulation.py constant
WEIGHTS = [[1.0], [0.5], [0.15], [0.1]]
BAD_EMOTIONS = [0, 1]

# views.py constant
TEXT_PATH = 'media/text.txt'
AUDIO_INPUT_WAV_PATH = 'media/input.wav'
AUDIO_INPUT_WEBM_PATH = 'media/input.webm'
AUDIO_OUTPUT_PATH = 'media/output.wav'

UPDATE_POST_MESSAGE = "update was successful"