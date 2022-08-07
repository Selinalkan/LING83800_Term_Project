#!/usr/bin/env python

import argparse
import csv
import g2p


def main(args: argparse.Namespace) -> None:
    correct = 0
    total = 0
    with open(args.input, "r") as source:
        tsv_reader = csv.reader(source, delimiter="\t")
        for word, pron in tsv_reader:
            pred = g2p.g2p(word)
            if pron == pred:
                correct += 1
            total += 1
    WER = 100 * correct / total

    print(f"WER:\t{WER}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", required=True, help="input the wikipron evaluation file"
    )
    main(parser.parse_args())
