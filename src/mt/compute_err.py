import pandas as pd
import jiwer

fname = "../results/mt/mt_res.csv"
df = pd.read_csv(fname, usecols=['hindi_target', 'hindi_translated'])

ground_truth = df['hindi_target'].tolist()
hypothesis = df['hindi_translated'].tolist()
hypothesis = [x[:-4] for x in hypothesis]

print(ground_truth[0], hypothesis[0])

print("word error rate: ", jiwer.wer(ground_truth, hypothesis))
