import hashlib

m = hashlib.md5(b"this is a test").hexdigest()

print('Output 1 : ', m)

