# scixors.py

## Simply Combine XORs

A command-line tool that computes the binary XOR of two files or two strings.

### Usage

```
python3 scixors.py (-f FILE1 FILE2 | -s STRING1 STRING2) -o OUTFILE [-b BITPOS]
```

### Options

| Option | Required | Description |
|---|---|---|
| `-f FILE1 FILE2` | One of `-f`/`-s` | Two input file names, read in binary mode. |
| `-s STRING1 STRING2` | One of `-f`/`-s` | Two input strings, given directly on the command line and encoded as UTF-8. |
| `-o OUTFILE` | Yes | Path to write the XOR result to. |
| `-b BITPOS` | No | A 0-indexed bit position in the larger input at which the XOR operation begins (see below). |

Exactly one of `-f` or `-s` must be given, and each takes exactly two arguments. `-o` is always required.

### How it works

1. **Read the inputs.** With `-f`, both files are read as raw bytes. With `-s`, both strings are encoded to bytes using UTF-8.

2. **Report input sizes.** The byte length of each input is printed to stdout before any processing happens.

3. **Equalize lengths.** If the two inputs are not the same length, the shorter one is repeated end-to-end (wrapping around as many times as needed) and then truncated so both inputs are exactly the same length as the longer one. For example, `"ab"` repeated to match a 5-byte input becomes `"ababa"`.

4. **XOR the bytes.** Each byte of the first (equalized) input is XORed with the corresponding byte of the second (equalized) input, producing an output of the same length.

5. **Optional bit offset (`-b`).** If `-b BITPOS` is given, the XOR is not applied to the whole output. Instead:
   - `BITPOS` is a bit index (0-indexed) into the **larger of the two original inputs** (before equalization). It must satisfy `0 <= BITPOS <= (bit length of the larger input) - 1`.
   - The first `BITPOS` bits are dropped from **both** equalized inputs.
   - The remaining bits (from `BITPOS` to the end) of both equalized inputs are XORed together as usual.
   - The output is therefore shorter than the equalized input length by `BITPOS` bits — this lets you XOR only a trailing portion of the data, discarding the leading bits of both inputs.

6. **Write the output.** The resulting bytes are written to the file named by `-o`.

7. **Report the result.** The size of the output file is printed to stdout, along with the bit position used (if `-b` was given).

### Examples

XOR two strings, writing the result to `out.bin`:

```
python3 scixors.py -s "hello" "hi" -o out.bin
```

XOR two files:

```
python3 scixors.py -f a.dat b.dat -o result.dat
```

XOR two strings, but only from bit 8 onward (the first byte is dropped from both equalized strings):

```
python3 scixors.py -s "abcdefgh" "xy" -o out.bin -b 8
```

### Notes

- XOR is symmetric: XORing the output with either equalized input recovers the other equalized input (for the XORed portion).
- If one input is empty (zero length) while the other is not, `scixors.py` cannot repeat it to match length and will exit with an error.
- Input sizes/lengths and the final output size are always printed to stdout, regardless of whether `-b` is used.

---

## XOR

The XOR algorithm is a simple encryption method that uses the XOR (exclusive or) operation to encrypt and decrypt data. It works by applying the XOR operation between the plaintext and a key, and the same key is used again to decrypt the ciphertext back to the original plaintext.

### How It Works
The XOR algorithm operates by performing the following steps:

1. **Encryption**:
- The plaintext (the original data) is combined with a key using the XOR operation.  
- When the plaintext bit is 0 and the key bit is 1, the result is 1.  When both bits are the same, the result is 0.
- Each bit of the plaintext is XORed with the corresponding bit of the key.

2. **Decryption**:
- The same key is applied to the ciphertext (the encrypted data) using the XOR operation.
- This process reverses the encryption, returning the original plaintext.

### Key Characteristics
- Self-Inverse: The XOR operation is self-inverse, meaning that applying it twice with the same key will return the original data.
- Simplicity: The algorithm is easy to implement and computationally inexpensive.
- Security: While simple, the XOR algorithm can be vulnerable to attacks, especially if the key is short or reused.
