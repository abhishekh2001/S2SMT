import pandas as pd
import jiwer
from nltk.translate.bleu_score import corpus_bleu

fname = "../results/mt/mt_res.csv"
df = pd.read_csv(fname)

ground_truth = df['hindi_target'].tolist()
ground_truth = [x.strip() for x in ground_truth]
hypothesis = df['hindi_translated'].tolist()
hypothesis = [x[:-4].strip() for x in hypothesis]

print(ground_truth[0], hypothesis[0])

print("word error rate: ", jiwer.wer(ground_truth, hypothesis))

ref_list = [[x] for x in ground_truth]
hyp_list = hypothesis
v = corpus_bleu(ref_list, hyp_list)

print("bleu score: ", v)



inc = pd.DataFrame(columns=['file', 'transcript', 'hindi_target', 'hindi_translated'])
for i in range(len(hypothesis)):
    if hypothesis[i] != ground_truth[i]:
        print(f"{i}: {hypothesis[i]} : {ground_truth[i]}")
        x = {'file': df.loc[i, 'file'],
                'transcript': df.loc[i, 'transcript'],
                'hindi_target': ground_truth[i],
                'hindi_translated': hypothesis[i]}
        print(x)
        inc = inc.append(x, ignore_index=True)
        print(len(inc))

inc.to_csv('../results/mt/inc.csv')
