from py_vapid import Vapid
v = Vapid()
keys = v.generate_keys()
public = keys['public_key']
private = keys['private_key']
print({'publicKey': public, 'privateKey': private})
with open('../.env', 'a') as f:
    f.write(f"VAPID_PUBLIC_KEY={public}\n")
    f.write(f"VAPID_PRIVATE_KEY={private}\n")
print('Saved keys to .env')
