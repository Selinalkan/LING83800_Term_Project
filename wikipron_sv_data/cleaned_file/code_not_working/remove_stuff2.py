#!/usr/bin/env python

"""This script removes the lines with "/ e n . w i k t i o n a r y . o r g" in
    the pronunciation column."""

import argparse
import re
import csv


def main(args: argparse.Namespace) -> None:
    with open("sv2.tsv", "r") as source, open("sv3.tsv", "w") as sink:
        tsv_reader = csv.reader(source, delimiter="\t")
        tsv_writer = csv.writer(sink, delimiter="\t")
        for row in tsv_reader:
            match_obj = re.match(r"(.*)(²?)(\w*)", row[1])
            # "(\w+)(\-)(\w+)",
            # [²ˈˌ‿¹.ʔ]
            if match_obj:
                row = [
                    row[0],
                    match_obj.group(1) + match_obj.group(3),
                ]
            assert row[0] != ""
            tsv_writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input Maori file")
    parser.add_argument(
        "--output", required=True, help="output Maori file as lemmas"
    )
    main(parser.parse_args())
