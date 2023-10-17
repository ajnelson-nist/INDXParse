#! /usr/bin/env python

#   Alex Nelson, NIST, contributed to this file.  Contributions of NIST
#   are not subject to US Copyright.

import argparse
import logging

from indxparse.BinaryParser import Mmap
from indxparse.MFT import Cache, MFTTree, MFTTreeNode


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse MFT " "filesystem structures.")
    parser.add_argument(
        "-c",
        action="store",
        metavar="cache_size",
        type=int,
        dest="cache_size",
        default=1024,
        help="Size of cache.",
    )
    parser.add_argument(
        "-v", action="store_true", dest="verbose", help="Print debugging information"
    )
    parser.add_argument("filename", action="store", help="Input MFT file path")

    results = parser.parse_args()

    if results.verbose:
        logging.basicConfig(level=logging.DEBUG)

    with Mmap(results.filename) as buf:
        record_cache = Cache(results.cache_size)
        path_cache = Cache(results.cache_size)

        tree = MFTTree(buf)
        tree.build(record_cache=record_cache, path_cache=path_cache)

        def rec(node: MFTTreeNode, prefix: str) -> None:
            print(prefix + node.get_filename())
            for child in node.get_children_nodes():
                rec(child, prefix + "  ")

        rec(tree.get_root(), "")


if __name__ == "__main__":
    main()
