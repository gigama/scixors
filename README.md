# scixors

### Simply Combine XORs

The XOR algorithm is a simple encryption method that uses the XOR (exclusive or) operation to encrypt and decrypt data. It works by applying the XOR operation between the plaintext and a key, and the same key is used again to decrypt the ciphertext back to the original plaintext.

### How It Works
The XOR algorithm operates by performing the following steps:

1. **Encryption**:
- The plaintext (the original data) is combined with a key using the XOR operation.  When the plaintext bit is 0 and the key bit is 1, the result is 1.
When both bits are the same, the result is 0.
- Each bit of the plaintext is XORed with the corresponding bit of the key.

2. **Decryption**:
- The same key is applied to the ciphertext (the encrypted data) using the XOR operation.
- This process reverses the encryption, returning the original plaintext.

### Key Characteristics
- Self-Inverse: The XOR operation is self-inverse, meaning that applying it twice with the same key will return the original data.
- Simplicity: The algorithm is easy to implement and computationally inexpensive.
- Security: While simple, the XOR algorithm can be vulnerable to attacks, especially if the key is short or reused.
