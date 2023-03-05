import pandas as pd
import wave
from pathlib import Path
import os
import contextlib

fname = "test.csv"
df = pd.read_csv(fname)

text_gen = []
segments = []
wav_scp = []

text_file = open('../utils/kaldi/test/text', 'w')
segments_file = open('../utils/kaldi/test/segments', 'w')
wav_scp_file = open('../utils/kaldi/test/wav.scp', 'w')
utt2spk_file = open('../utils/kaldi/test/utt2spk', 'w')

for index, row in df.iterrows():
    abs_path = Path(row['wav_filename']).resolve()
    file_id = str(index) + '_' + abs_path.name
    

    # get speaker id
    spk = '_'.join(str(abs_path).split('/')[-3:-1])
    utt_id = spk + '_' + file_id + '_utt'

    utt2spk = f"{utt_id} {spk}"

    tscpt = row['transcript']

    # get duration of file
    with contextlib.closing(wave.open(str(abs_path), 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        segment_row = f"{utt_id} {file_id} 0.0 {duration}"

    

    # text: [utt_id word1 word2 ...]
    # text_gen.append(' '.join([utt_id, tscpt]))
    text_file.write(' '.join([utt_id, tscpt.upper()]) + '\n')

    # segment [utt_id, file_id, sttart_time, end_time]
    # segments.append(segment_row)
    segments_file.write(segment_row + '\n')

    # wav.scp [file_id filepath]
    wav_scp_file.write(f"{file_id} {str(abs_path)}\n")

    # utt2spk [utt_id spkr_id]
    utt2spk_file.write(utt2spk + '\n')




with open('text', 'w') as f:
    f.writelines(text_gen)
