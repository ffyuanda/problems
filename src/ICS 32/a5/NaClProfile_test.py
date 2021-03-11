from Profile import Profile, Post
from NaClProfile import NaClProfile
bio = ''
np = NaClProfile()
kp = np.generate_keypair()
bio = np.nacl_profile_encrypt(bio)
bio = np.nacl_profile_decrypt(bio)
# np = NaClProfile()
# kp = np.generate_keypair()
# print(np.public_key)
# print(np.private_key)
# print(np.keypair)
#
# # Test encryption with 3rd party public key
# ds_pubkey = "jIqYIh2EDibk84rTp0yJcghTPxMWjtrt5NW4yPZk3Cw="
# ee = np.encrypt_entry("Encrypted Message for DS Server", ds_pubkey)
# print(ee)
# # print(np.nacl_profile_decrypt(ee, ds_pubkey))
#
# # Add a post to the profile and check that it is decrypted.
# np.add_post(Post("Hello Salted World!"))
# p_list = np.get_posts()
# print(p_list[0].get_entry())
#
# # Save the profile
# path = "C:\\Users\\ThinkPad\\Desktop\\test\\mark.dsu"
# np.save_profile(path)
#
# print("Open DSU file to check if message is encrypted.")
# input("Press Enter to Continue")
#
# # Create a new NaClProfile object and load the dsu file.
# np2 = NaClProfile()
# np2.load_profile(path)
# # print('np2 keypair:', np2.keypair, len(np2.keypair))
# # Import the keys
# np2.import_keypair(kp)
#
# # Verify the post decrypts properly
# p_list = np2.get_posts()
# print(p_list[0].get_entry())


