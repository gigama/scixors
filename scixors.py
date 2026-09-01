#!/usr/bin/env python3
"""
scixors.py - binary XOR utility for two files or two strings.
"""

import argparse
import sys


def read_inputs(args):
    """Return (label, bytes) tuples for the two inputs, based on -f or -s."""
    if args.f:
        path1, path2 = args.f
        try:
            with open(path1, "rb") as fh:
                data1 = fh.read()
        except OSError as exc:
            sys.exit(f"Error reading file '{path1}': {exc}")
        try:
            with open(path2, "rb") as fh:
                data2 = fh.read()
        except OSError as exc:
            sys.exit(f"Error reading file '{path2}': {exc}")
        return ("file", path1, data1), ("file", path2, data2)
    else:
        str1, str2 = args.s
        data1 = str1.encode("utf-8")
        data2 = str2.encode("utf-8")
        return ("string", str1, data1), ("string", str2, data2)


def repeat_to_length(data, target_len):
    """Repeat 'data' end-to-end until it reaches target_len bytes."""
    if len(data) == 0:
        sys.exit("Error: cannot repeat a zero-length input to match size.")
    reps = (target_len // len(data)) + 1
    return (data * reps)[:target_len]


def equalize(data1, data2):
    """Repeat the shorter of two byte sequences so both share the same length."""
    len1, len2 = len(data1), len(data2)
    if len1 == len2:
        return data1, data2
    target = max(len1, len2)
    if len1 < len2:
        data1 = repeat_to_length(data1, target)
    else:
        data2 = repeat_to_length(data2, target)
    return data1, data2


def bytes_to_bits(data):
    return "".join(f"{byte:08b}" for byte in data)


def bits_to_bytes(bits):
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))


def xor_bytes(data1, data2):
    return bytes(b1 ^ b2 for b1, b2 in zip(data1, data2))


def xor_from_bit(data1, data2, bit_pos):
    """
    XOR two equal-length byte sequences starting at bit_pos (0-indexed).
    Bits before bit_pos are dropped from both inputs; only the XOR of the
    remaining tail bits (from bit_pos to the end) is returned.
    """
    bits1 = bytes_to_bits(data1)
    bits2 = bytes_to_bits(data2)

    xored_tail = "".join(
        "1" if b1 != b2 else "0"
        for b1, b2 in zip(bits1[bit_pos:], bits2[bit_pos:])
    )
    return bits_to_bytes(xored_tail)


def main():
    parser = argparse.ArgumentParser(
        description="Compute the binary XOR of two files or two strings."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", nargs=2, metavar=("FILE1", "FILE2"),
        help="Two input file names to XOR."
    )
    group.add_argument(
        "-s", nargs=2, metavar=("STRING1", "STRING2"),
        help="Two input strings to XOR."
    )
    parser.add_argument(
        "-o", required=True, metavar="OUTFILE",
        help="Output file to write the XOR result to."
    )
    parser.add_argument(
        "-b", type=int, default=None, metavar="BITPOS",
        help="Bit position (0-indexed) in the larger input at which to begin "
             "the XOR; bits before this position are copied unchanged from "
             "the larger input."
    )
    args = parser.parse_args()

    unit = "size" if args.f else "length"
    (label1, name1, data1), (label2, name2, data2) = read_inputs(args)

    print(f"Input 1 ({name1}) {unit}: {len(data1)} bytes")
    print(f"Input 2 ({name2}) {unit}: {len(data2)} bytes")

    # Determine which original input is the larger one, before equalization.
    larger_original = data1 if len(data1) >= len(data2) else data2

    eq1, eq2 = equalize(data1, data2)

    if args.b is not None:
        bit_length = len(larger_original) * 8
        if args.b < 0 or args.b > bit_length - 1:
            sys.exit(
                f"Error: -b must be between 0 and {bit_length - 1} "
                f"(bit length of the larger input minus 1)."
            )
        result = xor_from_bit(eq1, eq2, args.b)
        print(f"XOR starting at bit {args.b} of {bit_length} total bits "
              f"(first {args.b} bits dropped from both inputs)")
    else:
        result = xor_bytes(eq1, eq2)

    try:
        with open(args.o, "wb") as fh:
            fh.write(result)
    except OSError as exc:
        sys.exit(f"Error writing output file '{args.o}': {exc}")

    print(f"Output file ({args.o}) size: {len(result)} bytes")


if __name__ == "__main__":
    main()
