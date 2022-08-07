#!/usr/bin/env python

import argparse
import csv
import g2p


def main(args: argparse.Namespace) -> None:
    try:
        correct = 0
        total = 0
        with open(args.input, "r") as source:
            tsv_reader = csv.reader(source, delimiter="\t")
            for word, pron in tsv_reader:
                pred = g2p.g2p(word)
                if pron == pred:
                    correct += 1
                total += 1
        ACC = correct / total
        WER = 100 * (1 - ACC)

        print(f"Accuracy:\t{ACC}")
        print(f"WER:\t\t{WER}")
    except:
        print("NameOfException: logic")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", required=True, help="input the wikipron pronunciation file"
    )
    main(parser.parse_args())
