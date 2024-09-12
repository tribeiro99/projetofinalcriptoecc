import random

    encrypted_message = ""
    for char in message:
        if char.isalpha():  
            shift = ord('a') if char.islower() else ord('A')
            encrypted_message += chr((ord(char) - shift + key) % 26 + shift)
        else:
            encrypted_message += char 
            return encrypted_message

    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():  
            shift = ord('a') if char.islower() else ord('A')
            decrypted_message += chr((ord(char) - shift - key) % 26 + shift)
        else:
            decrypted_message += char      return decrypted_message 

key = random.randint(1, 25)  
encrypted_message = encrypt(message, key)
print(f"Mensagem criptografada: {encrypted_message}")

print(f"Mensagem descriptografada: {decrypted_message}")

print(f"Chave utilizada: {key}")

