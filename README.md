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
  - Train LDA-MLLT (Linear Discriminant Analysis – Maximum Likelihood Linear Transform) triphones (3500 states and 20,000 gaussians)
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

This approach gives us 100% accuracy in speech recogntition.
