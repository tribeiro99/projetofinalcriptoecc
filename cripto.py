import random
import math
import hashlib
import Cryptodome
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
# Chave pública usada no algoritmo ECC, G representa um ponto gerador na curva e representa a multiplicação escalar
# A partir da fórmula para gerar a chave pública:
# K = k * G
# G é o ponto gerador da curva (um ponto fixo e conhecido por todos).
# k é a chave privada (um número inteiro).
# K é a chave pública (um ponto na curva elíptica).
# A curva é definida pela equação y² = x³ + ax + b
class CurvaEliptica:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def pertence_curva(self, x, y):
        return y**2 == x**3 + self.a * x + self.b

    def gerar_ponto_na_curva(self):
        while True:
            x = random.uniform(-100, 100)
            ldr = x**3 + self.a * x + self.b

            if ldr >= 0:
                y = math.sqrt(ldr)
                if self.pertence_curva(x, y):
                    return (x, y)
                elif self.pertence_curva(x, -y):
                    return (x, -y)

    def gerar_chave_privada(self, intervalo=1000):
        return random.randint(1, intervalo)

    def chave_publica(self, chave_privada, ponto_base):
        x_base, y_base = ponto_base
        x_pub = chave_privada * x_base
        y_pub = chave_privada * y_base
        return (x_pub, y_pub)

    def derivar_chave_secreta(self, ponto_comum):
        x, y = ponto_comum
        return hashlib.sha256(str(x).encode()).digest()

    def criptografar(self, mensagem, chave_secreta):
        cipher = AES.new(chave_secreta, AES.MODE_CBC)
        mensagem_padded = pad(mensagem.encode(), AES.block_size)
        criptografado = cipher.encrypt(mensagem_padded)
        return cipher.iv + criptografado

    def descriptografar(self, criptografado, chave_secreta):
        iv = criptografado[:AES.block_size]
        criptografado = criptografado[AES.block_size:]
        cipher = AES.new(chave_secreta, AES.MODE_CBC, iv)
        mensagem_padded = cipher.decrypt(criptografado)
        return unpad(mensagem_padded, AES.block_size).decode()

if __name__ == "__main__":
    curva = CurvaEliptica(2, 3)

    priv_key1 = curva.gerar_chave_privada()
    pub_key1 = curva.gerar_ponto_na_curva()
    priv_key2 = curva.gerar_chave_privada()
    pub_key2 = curva.gerar_ponto_na_curva()

    ponto_comum1 = curva.chave_publica(priv_key1, pub_key2)
    ponto_comum2 = curva.chave_publica(priv_key2, pub_key1)

    chave_secreta1 = curva.derivar_chave_secreta(ponto_comum1)
    chave_secreta2 = curva.derivar_chave_secreta(ponto_comum2)

    mensagem = "Mensagem secreta"
    criptografado = curva.criptografar(mensagem, chave_secreta1)
    print(f"Mensagem criptografada: {criptografado}")

    descriptografado = curva.descriptografar(criptografado, chave_secreta2)
    print(f"Mensagem descriptografada: {descriptografado}")

