import numpy as np

WINDOW_SIZE = 10   # 🔥 FINAL FIX

def create_sequence(data):
    sequences = []
    
    for i in range(len(data) - WINDOW_SIZE):
        sequences.append(data[i:i+WINDOW_SIZE])
    
    return np.array(sequences)