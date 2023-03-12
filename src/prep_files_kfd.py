import pandas as pd
import wave
from pathlib import Path
import os
import contextlib

fname = "test.csv"
df = pd.read_csv(fname)

print(df.head())

text_gen = []
segments = []
wav_scp = []

MODE = "TEST"

try:
    os.mkdir(f'../utils/kaldi_dat/{MODE}')
except:
    print("folder exists...")
    exit()

text_file = open(f'../utils/kaldi_dat/{MODE}/text', 'w')
segments_file = open(f'../utils/kaldi_dat/{MODE}/segments', 'w')
wav_scp_file = open(f'../utils/kaldi_dat/{MODE}/wav.scp', 'w')
utt2spk_file = open(f'../utils/kaldi_dat/{MODE}/utt2spk', 'w')
spk2gender = open(f'../utils/kaldi_dat/{MODE}/spk2gender', 'w')
corpus = open(f'../utils/kaldi_dat/{MODE}/corpus.txt', 'w')

for index, row in df.iterrows():
    abs_path = Path(row['wav_filename']).resolve()
    file_id = str(index) + '_' + abs_path.name

    # get gender
    gender = 'm'
    if 'WOMAN' in str(abs_path):
        gender = 'w'

    # get speaker id
    spk = '_'.join(str(abs_path).split('/')[-3:-1])
    utt_id = spk + '_' + file_id + '_utt'

    utt2spk = f"{utt_id} {spk}"

    tscpt = row['transcript'].lower()

    # get duration of file
    with contextlib.closing(wave.open(str(abs_path), 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        segment_row = f"{utt_id} {file_id} 0.0 {duration}"

    # spk2gender: [speaker_id gender]
    # spk2gender.write(f"{spk} {gender}\n")

    # text: [utt_id word1 word2 ...]
    # text_gen.append(' '.join([utt_id, tscpt]))
    text_file.write(' '.join([utt_id, tscpt]) + '\n')

    # segment [utt_id, file_id, sttart_time, end_time]
    # segments.append(segment_row)
    segments_file.write(segment_row + '\n')

    # wav.scp [file_id filepath]
    wav_scp_file.write(f"{file_id} {str(abs_path)}\n")

    # utt2spk [utt_id spkr_id]
    utt2spk_file.write(utt2spk + '\n')

    # corpus: [tscpt]
    # corpus.write(f"{tscpt}\n")
