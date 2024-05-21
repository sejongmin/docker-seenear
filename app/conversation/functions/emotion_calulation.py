import numpy as np
from constant.conversation import *

def calculateEmotionRate(rate, emotion, count):
    sum_emotion_score = rate * count 
    
    now_emotion_score = np.dot(emotion, WEIGHTS)

    sum_emotion_score += now_emotion_score[0][0]
    emotion_rate = sum_emotion_score / (count + 1)

    return emotion_rate

def calculateBadRate(rate, emotion, count):
    sum_bad_score = rate * count

    if emotion in BAD_EMOTIONS:
        sum_bad_score += 1.0
        
    bad_rate = sum_bad_score / (count + 1)

    return bad_rate