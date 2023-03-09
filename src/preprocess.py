import os
import csv
import argparse

parser = argparse.ArgumentParser(description='init preprocessing')
parser.add_argument("--train", action="store_true")
parser.add_argument("--test", action="store_true")
parser.add_argument("--inference", action="store_true")


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
    "o": "oh"
}


def gen_fdets(root_dir, out_fname):
    file_paths = []
    transcripts = []
    file_sizes = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".wav"):
                file_paths.append(os.path.join(root, file))
                file_sizes.append(os.path.getsize(
                    os.path.join(root, file)))
                tscpt = os.path.splitext(file)[0][:-1]
                tscpt = tscpt.replace("Z", "0")
                tscpt = " ".join(tscpt.split()).lower()
                tscpt = " ".join(
                    [totext[x] if x in totext.keys() else x for x in tscpt])
                transcripts.append(tscpt)

    print("writing ", out_fname)
    # create a new CSV file
    csv_file = open(out_fname, mode="w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["wav_filename", "wav_filesize", "transcript"])

    # write the file paths and filenames to the CSV file
    for i in range(len(file_paths)):
        csv_writer.writerow(
            [str(file_paths[i]), file_sizes[i], transcripts[i]])

    # close the CSV file
    csv_file.close()


if __name__ == '__main__':
    args = parser.parse_args()

    # directory to search for .wav files
    root_dir = "../data/"
    train_dir = os.path.join(root_dir, "TRAIN")
    test_dir = os.path.join(root_dir, "TEST")
    inf_dir = os.path.join(root_dir, "INFERENCE")

    if args.train:
        gen_fdets(train_dir, "train.csv")
    if args.test:
        gen_fdets(test_dir, "test.csv")
    if args.inference:
        gen_fdets(inf_dir, "inf.csv")
