#!/usr/bin/env python

import argparse


def main(args: argparse.Namespace) -> None:
    sent = []
    with open(args.input, "r") as f:
        for line in f:
            line = line.rstrip()
            sent.append(line)
    with open(args.train, "w") as source:
        for line in sent[: int(len(sent) * 0.8)]:
            print(line, file=source)
    with open(args.dev, "w") as source:
        for line in sent[int(len(sent) * 0.8): int(len(sent) * 0.9)]:
            print(line, file=source)
    with open(args.test, "w") as source:
        for line in sent[int(len(sent) * 0.9):]:
            print(line, file=source)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input sentence file")
    parser.add_argument("--train", required=True, help="output training file")
    parser.add_argument(
        "--dev", required=True, help="output development set sentences"
    )
    parser.add_argument(
        "--test", required=True, help="output training set sentences"
    )
    main(parser.parse_args())
