import nacl.utils
import NaClDSEncoder
import os
import json
import copy
from nacl.public import PrivateKey, PublicKey, Box, EncryptedMessage
from Profile import Post, Profile
from pathlib import Path

"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class NaClProfile(Profile):
    def __init__(self, dsuserver=None, username=None, password=None):
        """
        public data attributes:

        public_key:str
        private_key:str
        keypair:str

        Whether you include them in your parameter list is up to you. Your decision will frame
        how you expect your class to be used though, so think it through.
        """
        super().__init__(dsuserver, username, password)
        self.public_key = ''
        self.private_key = ''
        self.keypair = ''

    def delete_post(self, index: int) -> None:
        """
        Delete a post from the self_posts list using a index.
        :param index: the index of the post
        :return: None
        """
        self._posts.pop(index)

    def edit_post(self, index: int, title: str, entry: str):
        """
        Sets a specific post in the self_posts list, change its title and entry.
        :param index: the index of the post we want to access in self_posts list
        :param title: str BEFORE encryption
        :param entry: str BEFORE encryption
        :return:
        """
        title = self.nacl_profile_encrypt(title)
        entry = self.nacl_profile_encrypt(entry)
        self._posts[index].set_title(title)
        self._posts[index].set_entry(entry)

    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

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

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer.
        """
        split = keypair.split('=', 1)
        self.public_key = split[0] + '='
        self.private_key = split[1]
        self.keypair = keypair

    def add_bio(self, bio: str) -> None:
        """
        Add a bio (str) to the NaclProfile by encrypting it.
        :param bio: input bio str
        :return: None
        """
        bio = self.nacl_profile_encrypt(bio)
        self.bio = bio

    def get_bio(self) -> str:
        """
        Return the encrypted bio to the decrypting form.
        :return: decrypted bio
        """
        return self.nacl_profile_decrypt(self.bio)

    def add_post(self, post: Post) -> Post:
        """
        Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
        code that is already written in the parent class.

        :return the post after encryption
        """
        entry = post.get_entry()
        encrypted_entry = self.nacl_profile_encrypt(entry)
        post.set_entry(encrypted_entry)

        title = post.get_title()
        encrypted_title = self.nacl_profile_encrypt(title)
        post.set_title(encrypted_title)

        super().add_post(post)
        return post

    def get_posts(self) -> list:
        """
        Since posts will be encrypted when the add_post method is used, you will need to ensure they are
        decrypted before returning them to the calling code.

        :return: list of posts
        """
        # use deepcopy to avoid changing the actual encrypted message in the post
        # in this case accidentally decrypting them
        posts = super().get_posts()
        out_posts = copy.deepcopy(posts)

        for post in out_posts:
            entry = post.get_entry()
            title = post.get_title()

            entry = self.nacl_profile_decrypt(entry)
            title = self.nacl_profile_decrypt(title)

            post.set_entry(entry)
            post.set_title(title)

        return out_posts

    def load_profile(self, path: str) -> None:
        """
        Since the DS Server is now making use of encryption keys rather than username/password attributes, you will
        need to add support for storing a keypair in a dsu file. The best way to do this is to override the
        load_profile module and add any new attributes you wish to support.
        """
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.import_keypair(obj['keypair'])
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'], post_obj['title'])
                    self._posts.append(post)
                f.close()
            except json.decoder.JSONDecodeError as ex:
                if str(ex) == 'Expecting value: line 1 column 1 (char 0)':
                    raise DsuFileError('the dsu file is empty') from ex
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

    def encrypt_entry(self, entry: str, public_key: str = 'empty') -> str:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.

        :return: a str after encode-decode an EncryptedMessage object
        """
        if public_key == 'empty':
            public_key = self.public_key
        return self.nacl_profile_encrypt(entry, public_key)

    def nacl_profile_encrypt(self, msg: str, public_key: str = 'empty') -> str:
        """
        It reads in a plaintext (str) and encrypt it into a str after
        encode-decode an EncryptedMessage object.
        :param msg: plaintext string
        :param public_key: by default to be self.public_key if not provided
        :return: a str after encode-decode an EncryptedMessage object
        """
        if public_key == 'empty':
            public_key = self.public_key

        encoder = NaClDSEncoder.NaClDSEncoder()
        public_key = encoder.encode_public_key(public_key)
        private_key = encoder.encode_private_key(self.private_key)

        the_box = Box(private_key, public_key)
        # convert the msg input into the byte version of itself
        # since the box.encrypt() method needs a byte object as parameter
        bmsg = msg.encode(encoding='UTF-8')
        bencrypted = the_box.encrypt(bmsg, encoder=nacl.encoding.Base64Encoder)
        # convert the bencrypted object (EncryptedMessage) back to str for JSON
        # serialization
        encrypted = bencrypted.decode(encoding='UTF-8')
        return encrypted

    def nacl_profile_decrypt(self, encrypted: str, public_key: str = 'empty') -> str:
        """
        It reads in a str after encode-decode an EncryptedMessage object
        and decrypt it to a plaintext (str).
        :param encrypted: a str after the encode-decode an EncryptedMessage object
        :param public_key: by default to be self.public_key if not provided
        :return: plaintext string
        """
        if public_key == 'empty':
            public_key = self.public_key

        encoder = NaClDSEncoder.NaClDSEncoder()
        public_key = encoder.encode_public_key(public_key)
        private_key = encoder.encode_private_key(self.private_key)

        the_box = Box(private_key, public_key)
        # convert the encrypted input into the byte version of itself
        # since the box.decrypt() method needs a byte object as parameter
        bencrypted = encrypted.encode(encoding='UTF-8')

        bdecrypted = the_box.decrypt(bencrypted, encoder=nacl.encoding.Base64Encoder)
        # needs to be decoded to convert from byte to str
        decrypted = bdecrypted.decode(encoding='UTF-8')
        return decrypted
