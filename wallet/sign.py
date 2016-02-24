from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.hazmat.bindings.openssl.binding import Binding


class PKCS7Signer:

    def __init__(self, certificate, key, wwdr, password):
        """
        certificate - path to your public certificate, in PEM format
        key - private key that goes with your certificate, in PEM format
        wwdr - path to the Apple WWDR intermediate certifiacte, in PEM format
        password - string password for your private key
        """

        passwordBytes = password.encode('ascii') # now it is type `bytes`

        with open(certificate, "rb") as f:
            self.signcert = x509.load_pem_x509_certificate(f.read(), openssl.backend)
        with open(wwdr, "rb") as f:
            self.wwdr_cert = x509.load_pem_x509_certificate(f.read(), openssl.backend)
        with open(key, "rb") as k:
            self.key = serialization.load_pem_private_key(k.read(), passwordBytes, openssl.backend)



    def sign(payload):
        """
        payload - the data to sign (bytes)
        Return: the signature, in binary DER format (bytes)
        """
        # Build a STACK_OF(X509 *). These are the intermediate certificates
        # in your signature.
        stack_of_wwdr = Binding.lib.sk_X509_new_null();
        Binding.lib.sk_X509_push(stack_of_wwdr, wwdr_cert._x509)

        # initialize a buffer to hold the input payload, in cdata-land.
        bio = openssl.backend._bytes_to_bio(payload)

        flags = Binding.lib.CMS_DETACHED | Binding.lib.CMS_BINARY

        result = Binding.lib.CMS_sign(signcert._x509, key._evp_pkey, stack_of_wwdr, bio[0], flags)

        # initialize a buffer to hold the output signature.
        bio_out = openssl.backend._create_mem_bio_gc()
        Binding.lib.i2d_CMS_bio_stream(bio_out, result, bio[0], flags)
        # read the signature from cdata-land into python-land `bytes`
        bites = openssl.backend._read_mem_bio(bio_out)
        return bites
