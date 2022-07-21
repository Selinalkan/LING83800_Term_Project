#!/usr/bin/env python

"""This script removes the lines with "/ e n . w i k t i o n a r y . o r g" in the
    pronunciation column."""

import argparse
import re
import csv


def main(args: argparse.Namespace) -> None:
    with open("sv__.tsv", "r") as source, open("sv2.tsv", "w") as sink:
        tsv_reader = csv.reader(source, delimiter="\t")
        tsv_writer = csv.writer(sink, delimiter="\t")
        data = [
            row
            for row in tsv_reader
            if "²" in row[1]
        ]
        tsv_writer.writerows(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input Maori file")
    parser.add_argument(
        "--output", required=True, help="output Maori file as lemmas"
    )
    main(parser.parse_args())
