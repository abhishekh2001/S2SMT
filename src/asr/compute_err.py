import pandas as pd
import jiwer

totext = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    "O": "zero",
    "Z": "zero"
}


def er(sr, tg):
    sr = sr.split(' ')[1:]
    tg = [totext[x].lower() for x in tg]

    return ' '.join(sr).lower(), ' '.join(tg).lower()


fname = "../results/asr/test_res.csv"
df = pd.read_csv(fname, usecols=['file', 'transcript'])

ground_truth = []
hypothesis = []
for i, row in df.iterrows():
    fname = row['file']
    trans = row['transcript']

    tg = fname.split('.')[0].split('_')[-1][:-1]
    hp, gt = er(trans, tg)
    ground_truth.append(gt)
    hypothesis.append(hp)

print(ground_truth[0], hypothesis[0])

print("word error rate: ", jiwer.wer(ground_truth, hypothesis))
