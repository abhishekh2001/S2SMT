import pandas as pd

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
    tg = [totext[x].upper() for x in tg]

    inc = 0
    for i, v in zip(sr, tg):
        inc += (i != v)

    return inc / len(tg)


fname = "../results/asr/test_res.csv"
df = pd.read_csv(fname, usecols=['file', 'transcript'])

tot_err = 0
for i, row in df.iterrows():
    fname = row['file']
    trans = row['transcript']

    tg = fname.split('.')[0].split('_')[-1][:-1]
    tot_err += er(trans, tg)

tot_err = tot_err / len(df)

print(tot_err)
