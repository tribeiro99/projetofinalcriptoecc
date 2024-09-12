from fastecdsa import keys, curve, ecdsa

# Gerar par de chaves
priv_key, pub_key = keys.gen_keypair(curve.P256)
print("Chave Privada (Decimal):", priv_key)

# Converter coordenadas da chave pública de hexadecimal para decimal
x_decimal = int(pub_key.x)  # Converte coordenada X para decimal
y_decimal = int(pub_key.y)  # Converte coordenada Y para decimal

print("Chave Pública (Decimal):")
print("X:", x_decimal)
print("Y:", y_decimal)

# Assinatura da mensagem
message = "I am a message"
(r, s) = ecdsa.sign(message, priv_key)
print("Assinatura (r, s):", (r, s))

# Verificação da assinatura
valid = ecdsa.verify((r, s), message, pub_key)
print("Verificação:", valid)

