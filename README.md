# Speech-to-speech Machine Translation

## ASR

ASR was performed using kaldi the files for which are found under `utils/kaldi_dat` and `utils/kaldi_dat/test`.

The general pre-processing procedure used was to first convert all labels of `Z` and `O` to "zero" for testing purposes and to observe if the mapping between the variations in zero can be learnt. Kaldi is then used to train a GMM-HMM model on the dataset. The phenomes for each utterance in the test dataset is retrieved and is found in `utils/kaldi_dat/test/final_ali.txt` which includes the alignments for each clips in the dataset.

The training procedure is as follows (note that all files for training that have been used is found in `utils/kaldi_dat/`):

- Extract MFCC features (WSJ's `stepps/make_mfcc.sh`)
- Monophones
  - Train monophones
  - Align monophones
- Triphones
  - Train delta-based triphones (2000 HMM states and 10,000 Gaussians)
  - Align delta-based triphones
  - Train delta + delta-delta triphones (2500 HMM states and 15,000 Gaussians)
  - Align delta + delta-delta triphones
  - Train LDA-MLLT triphones (Linear Discriminant Analysis – Maximum Likelihood Linear Transform) (3500 states and 20,000 gaussians)
  - Align LDA-MLLT triphones with FMLLR (Feature space maximum likelihood linear regression)
  - Train SAT triphones (speaker adaptive training) (4200 states and 40,000 gaussians) reduces variability between speakers. -- `tri4a`.

For inference, the following steps are performed:

- setup relevant files (found in `utils/kaldi_dat/test/`).
- Extract MFCC similar to training.
- Use the acoustic model trained as per the details above (`tri4a`) to align the data.
- Extract alignment
  - Extract CTM outputs from the alignment files gathered above.
  - The CTM files are then concatenated
  - The CTM files contain phoneme IDs. Use `src/asr/id2phone.R` to combine the phones used during training of the AM (time-wise alignments are given in `utils/kaldi_dat/test/final_ali.txt`)
  - Combine the above time-separated phonemes and run greedy matching (`src/asr/merge.py`) to generate the results at `results/asr/test_res.csv` which has the phoneme sequence and the predictions.

An interesting observation is in the labelling of sequence "428OOO9A" where the "O" enunciation is labelled as "Z_B IY_I R_I AO_I" at timestamps 1.73, 1.8, 1.83, and 1.89.

Once the phonemes are captured, an algorithms classifies and groups these phonemes greedily and assignes the appropriate value to it. The final ASR output is stored in `results/asr/test_res.csv`.

## Machine Translation

Tensorflow is used to create an encoder-decoder architecture trained on 15,000 datapoints for 50 epochs. The final translation results using the model is found in `results/mt/mt_res.csv` where the column `hindi_target` is the ground truth and the column `hindi_translated` is the hypothesis. The model weights are at: [en_hi_weights.h5](https://iiitaphyd-my.sharepoint.com/:f:/g/personal/abhishekh_sivakumar_students_iiit_ac_in/EoH8w_GCcdRGhA277upbpmUB6Zv_GuMkCaioz1xmzzCoQw?e=keyEPf)

Architecture:

```
Layer (type)                    Output Shape         Param #     Connected to
==================================================================================================
input_5 (InputLayer)            (None, None)         0
__________________________________________________________________________________________________
input_6 (InputLayer)            (None, None)         0
__________________________________________________________________________________________________
embedding_3 (Embedding)         (None, None, 200)    2000        input_5[0][0]
__________________________________________________________________________________________________
embedding_4 (Embedding)         (None, None, 200)    2600        input_6[0][0]
__________________________________________________________________________________________________
lstm_3 (LSTM)                   [(None, 200), (None, 320800      embedding_3[0][0]
__________________________________________________________________________________________________
lstm_4 (LSTM)                   [(None, None, 200),  320800      embedding_4[0][0]
                                                                 lstm_3[0][1]
                                                                 lstm_3[0][2]
__________________________________________________________________________________________________
dense_2 (Dense)                 (None, None, 13)     2613        lstm_4[0][0]
==================================================================================================
Total params: 648,813
Trainable params: 648,813
Non-trainable params: 0
```

Sample:

```
one one one two two three
एक एक दो एक दो तीन
```

The approach gives us a WER of 0.0103
