from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

password = "Peter123!"

hashed = password_hash.hash(password)

print("Hash created")
print("Password matches:", password_hash.verify(password, hashed))