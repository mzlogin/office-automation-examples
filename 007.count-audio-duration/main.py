import librosa
import os
import math

total_duration = 0

for root, dirs, files in os.walk('.'):
    for file_name in files:
        if file_name.endswith('.m4a'):
            file_path = os.path.join(root, file_name)
            duration = math.ceil(librosa.get_duration(path=file_path))
            print(f"{file_path}: {duration} seconds")
            total_duration += duration

print(f"Total duration: {total_duration} seconds")