import os
from coqui_stt_training.util.config import Config
from coqui_stt_training.util.config import initialize_globals_from_args
from coqui_stt_training.train import train


initialize_globals_from_args(
    alphabet_config_path="../utils/en_alphabet.txt",
    checkpoint_dir="../models/ckpt_dir",
    train_files=["train.csv"],
    test_files=["test.csv"],
    load_train="init",
    n_hidden=50,
    epochs=20,
)

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
train()
