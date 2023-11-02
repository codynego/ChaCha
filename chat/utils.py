# generate a public and private key using AES algorithm

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()
    serialized_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    serialized_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return serialized_private, serialized_public




def derive_symmetric_key(user_a_public_key, user_b_public_key, salt):
    # Serialize the public keys to bytes
    user_a_public_key_bytes = user_a_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    user_b_public_key_bytes = user_b_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

    # Combine both public keys and salt
    input_data = user_a_public_key_bytes + user_b_public_key_bytes + salt

    # Create a PBKDF2HMAC key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
    )

    # Derive the symmetric key
    symmetric_key = kdf.derive(input_data)

    return symmetric_key