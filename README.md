# Speech-to-speech Machine Translation

## ASR

ASR was performed using kaldi the files for which are found under `utils/kaldi_dat` and `utils/kaldi_dat/test`.

The general pre-processing procedure used was to first convert all labels of `Z` and `O` to "zero" for testing purposes and to observe if the mapping between the variations in zero can be learnt. Kaldi is then used to train a GMM-HMM model on the dataset. The phenomes for each utterance in the test dataset is retrieved and is found in `utils/kaldi_dat/test/final_ali.txt` which includes the alignments for each clips in the dataset.

The training procedure is as follows:

- Extract MFCC features
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
  - Train SAT triphones (speaker adaptive training) (4200 states and 40,000 gaussians) - reduces variability between speakers.

An interesting observation is in the labelling of sequence "428OOO9A" where the "O" enunciation is labelled as "Z_B IY_I R_I AO_I" at timestamps 1.73, 1.8, 1.83, and 1.89.

Once the phonemes are captured, an algorithms classifies and groups these phonemes greedily and assignes the appropriate value to it. The final ASR output is stored in `results/asr/test_res.csv`.

This approach gives us 100% accuracy in speech recogntition.
