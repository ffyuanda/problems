# TODO: Install the pynacl library so that the following modules are available
# to your program.
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

import NaClDSEncoder
from Profile import Post, Profile


class NaClProfile(Profile):
    def __init__(self):
        """
        TODO: Complete the initializer method. Your initializer should create the follow three
        public data attributes:

        public_key:str
        private_key:str
        keypair:str

        Whether you include them in your parameter list is up to you. Your decision will frame
        how you expect your class to be used though, so think it through.
        """
        super().__init__()
        self.public_key = ''
        self.private_key = ''
        self.keypair = ''

    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

        TODO: Complete the generate_keypair method.

        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str
        """
        nacl_encoder = NaClDSEncoder.NaClDSEncoder()
        nacl_encoder.generate()
        self.public_key = nacl_encoder.public_key
        self.private_key = nacl_encoder.private_key
        self.keypair = nacl_encoder.keypair
        return self.keypair


    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        TODO: Complete the import_keypair method.

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer.

        NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
        by the NaClDSEncoder
        """
        split = keypair.split('=', 1)
        self.public_key = split[0] + '='
        self.private_key = split[1]
        self.keypair = self.public_key + self.private_key


    """
    TODO: Override the add_post method to encrypt post entries.

    Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
    code that is already written in the parent class.

    NOTE: To call the method you are overriding as it exists in the parent class, you can use the built-in super keyword:

    super().add_post(...)
    """

    """
    TODO: Override the get_posts method to decrypt post entries.

    Since posts will be encrypted when the add_post method is used, you will need to ensure they are 
    decrypted before returning them to the calling code.

    :return: Post

    NOTE: To call the method you are overriding as it exists in the parent class you can use the built-in super keyword:
    super().get_posts()
    """

    """
    TODO: Override the load_profile method to add support for storing a keypair.

    Since the DS Server is now making use of encryption keys rather than username/password attributes, you will 
    need to add support for storing a keypair in a dsu file. The best way to do this is to override the 
    load_profile module and add any new attributes you wish to support.

    NOTE: The Profile class implementation of load_profile contains everything you need to complete this TODO. Just add
    support for your new attributes.
    """

    def encrypt_entry(self, entry: str, public_key: str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.

        TODO: Complete the encrypt_entry method.

        NOTE: A good design approach might be to create private encrypt and decrypt methods that your add_post,
        get_posts and this method can call.

        :return: bytes
        """
        pass