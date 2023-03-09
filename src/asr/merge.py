from collections import defaultdict
import pandas as pd

file_dets = defaultdict()

lex = {}
with open("lexicon.txt", "r") as f:
    for line in f:
        l = line.split()
        if l[0] == '<oov>':
            continue
        lex[l[0]] = [l[1:]]
lex['one'].append(['hh', 'w', 'ah', 'n'])
lex['two'].append(['t', 'uw'])


print(lex)


def get_transcript(ph_seq):
    cur_seq = []
    res = ''
    for s in ph_seq:
        ph = s.split('_')[0]
        if ph == 'SIL':
            cur_seq = []
            continue
        cur_seq.append(ph)
        for k in lex:
            match = False
            for types in lex[k]:
                if cur_seq == types:
                    match = True

            if match:
                res = res + ' ' + k
                cur_seq = []
                continue
            if len(cur_seq) > 5:
                cur_seq = []

    return res


with open("final_ali.txt", "r") as f:
    next(f)
    for line in f:
        d = line.split('\t')
        fname = d[0].split('.')[0]
        t = float(d[3])
        if fname not in file_dets:
            file_dets[fname] = []
        file_dets[fname].append([t, d[6]])


final_df = pd.DataFrame(columns=['file', 'ph seq', 'transcript'])


j = 0
for f in file_dets:
    seq = [x[1] for x in sorted(file_dets[f])]
    tr = get_transcript(seq)
    final_df = final_df.append(
        pd.Series([f, ' '.join(seq), tr], index=final_df.columns), ignore_index=True)

    # if j == 4:
    #     exit()

    j += 1

final_df.to_csv('res.csv')
