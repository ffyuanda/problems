# NaClDSEncoder.py
# 
# ICS 32 Winter 2020
# Assignment #4: Encrypting the Platform
#
# v0.2
# 
# The following module is designed to abstract the encoding procedures required
# when using the NaCl library. By default, NaCl works with bytes, but bytes are
# not very human friendly. So to make keypairs a little easier to work with, this 
# module will handle the generation of keys and encoding of keys into the 
# PublicKey and PrivateKey objects required by NaCl encryption functions.

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box


class NaClDSEncoder:
    def generate(self):
        """
        The generate method handles the creation of a private and public keys. These keys
        are also combined to form a keypair. Call this function when your program needs to 
        generate new keys.
        """
        # call the key generator function from the nacl library.
        raw = PrivateKey.generate()
        # the raw keypair, stored as PrivateKey.
        self.raw_keypair = raw
        # the private key, encoded from bytes to string
        self.private_key = raw.encode(encoder=nacl.encoding.Base64Encoder).decode(encoding = 'UTF-8')
        # the public key, encoded from bytes to string
        self.public_key = raw.public_key.encode(encoder=nacl.encoding.Base64Encoder).decode(encoding = 'UTF-8')
        # the keypair, useful for storage, but primarily a convenience attribute
        # that simply concatenates the public and private keys and stores them as a string.
        self.keypair = self.public_key + self.private_key
    
    def encode_public_key(self, public_key:str) -> PublicKey:
        """
        encode_public_key takes an public_key string as a parameter and generates
        a PublicKey object.
        """
        return PublicKey(public_key, nacl.encoding.Base64Encoder)
    
    def encode_private_key(self, private_key:str) -> PrivateKey:
        """
        encode_private_key takes an private_key string as a parameter and generates
        a PrivateKey object.
        """
        return PrivateKey(private_key, nacl.encoding.Base64Encoder)