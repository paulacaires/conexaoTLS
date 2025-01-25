from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

'''
# Generate our key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

password = b"passphrase"

# Write our key to disk for safe keeping
with open("./keys/key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(password),
    ))
    
'''

# Load the key from the file
with open("./keys/key.pem", "rb") as f:
    pem_data = f.read()  
    
private_key = serialization.load_pem_private_key(pem_data, password = b"passphrase")
print(private_key)

#  =========       Creating a self-signed certificate ===========
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime

# Generate our key
private_key_certificate = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

password_private_key_certificate = b"passphrase"
# Write our key to disk for safe keeping
with open("./keys/key_certificate.pem", "wb") as f:
    f.write(private_key_certificate.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(password_private_key_certificate),
    ))

# Generate the certificate itself 

# Various details about who we are. For a self-signed certificate the
# subject and issuer are always the same.

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"), # Duas letras
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Sao Paulo"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Sorocaba"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FidelMurilloPaula Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, "FMP.com"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key_certificate .public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.now(datetime.timezone.utc)
).not_valid_after(
    # Our certificate will be valid for 10 days
    datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName("localhost")]),
    critical=False,
# Sign our certificate with our private key
).sign(private_key_certificate, hashes.SHA256())

# Write our certificate out to disk.
with open("./certs/certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print(cert)
