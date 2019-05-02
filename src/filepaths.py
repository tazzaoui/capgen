import os

"""
Global data path definitions
"""

DATA_PATH = os.path.abspath("../data")
MODEL_DIR = os.path.abspath("../model")
CAP_DIR = os.path.join(DATA_PATH, "annotations")
CAP_FILE = os.path.join(CAP_DIR, "captions_train2014.json")
TRAIN_IMG_DIR = os.path.join(DATA_PATH, "train2014")
VOCAB_FILE = os.path.join(DATA_PATH, "vocab.pkl")
