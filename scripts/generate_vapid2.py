from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat
import base64

# generate private key
priv = ec.generate_private_key(ec.SECP256R1())
pub = priv.public_key()

# public key in uncompressed point
pub_bytes = pub.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
# VAPID public key is base64url without padding
vapid_public_b64 = base64.urlsafe_b64encode(pub_bytes).decode('utf-8').rstrip('=')

# private key PEM
priv_pem = priv.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode('utf-8')

# private key raw bytes (for pywebpush you can pass PEM)
print('VAPID_PUBLIC_KEY=', vapid_public_b64)
# save to .env
with open('.env','a') as f:
    f.write(f"VAPID_PUBLIC_KEY={vapid_public_b64}\n")
    f.write(f"VAPID_PRIVATE_PEM='''{priv_pem}'''\n")
print('Saved keys to .env')
