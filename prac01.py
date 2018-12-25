import os
import config

config_data = {}
for key, val in os.environ.items():
    if key.startswith('KAGGLE_'):
        config_key = key.replace('KAGGLE_', '', 1).lower()
        config_data[config_key] = val

print(config_data)
