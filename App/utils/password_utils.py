import bcrypt

def hash_password(password: str, rounds: int = 12) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

# Prueba...
if __name__ == "__main__":
    original = "mi_contraseña_segura"
    wrong = "no_es_esta"

    print("=== PRUEBA ===\n")
    print("-> Hasheando contraseña...")
    stored_hash = hash_password(original)
    print("Hash guardado:", stored_hash)

    print("\n-> Verificando contraseña CORRECTA...")
    if verify_password(original, stored_hash):
        print("Contraseña correcta")
    else:
        print("Contraseña incorrecta")

    print("\n-> Verificando contraseña INCORRECTA...")
    if verify_password(wrong, stored_hash):
        print("ERROR: la contraseña incorrecta fue aceptada")
    else:
        print("Contraseña incorrecta rechazada")