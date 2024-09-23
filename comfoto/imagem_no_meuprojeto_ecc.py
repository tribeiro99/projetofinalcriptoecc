import random
import math
import hashlib
import PySimpleGUI as sg
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from PIL import Image

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
        return b64encode(cipher.iv + criptografado).decode('utf-8')

    def descriptografar(self, criptografado, chave_secreta):
        try:
            criptografado = b64decode(criptografado)
            iv = criptografado[:AES.block_size]
            criptografado = criptografado[AES.block_size:]
            cipher = AES.new(chave_secreta, AES.MODE_CBC, iv)
            mensagem_padded = cipher.decrypt(criptografado)
            return unpad(mensagem_padded, AES.block_size).decode()
        except Exception as e:
            print(f"Erro ao descriptografar: {e}")
            return None

def mostrar_imagem(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)
        imagem = imagem.resize((300, 200))  
        imagem.save("/tmp/imagem_temp.png")  
        return "/tmp/imagem_temp.png"
    except Exception as e:
        print(f"Erro ao abrir a imagem: {e}")
        return None

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

    chave_secreta1 = chave_secreta1[:32]  
    chave_secreta2 = chave_secreta2[:32]  

    caminho_imagem = "/home/ribeiro/Transferências/armando/fotoprograma_redimensionada.jpeg"
    imagem_temp = mostrar_imagem(caminho_imagem)

    if imagem_temp:
        layout = [
            [sg.Image(filename=imagem_temp)],
            [sg.Text("Digite a mensagem para criptografar:")],
            [sg.Input(key="mensagem_para_criptografar")], 
            [sg.Button("Criptografar")],
            [sg.Text("Digite a mensagem criptografada para descriptografar:")],
            [sg.Input(key="mensagem_criptografada")],  
            [sg.Button("Descriptografar")],
            [sg.Text("Resultado:")],
            [sg.Output(size=(50, 10))],  
            [sg.Button("Sair")]
        ]

        window = sg.Window("Projeto Criptografia e Descriptografaria by Tiago Ribeiro", layout, margins=(100, 50))

        while True:
            event, values = window.read()

            if event == "Sair" or event == sg.WIN_CLOSED:
                break

            if event == "Criptografar":
                mensagem = values["mensagem_para_criptografar"]
                if mensagem:
                    criptografado = curva.criptografar(mensagem, chave_secreta1)
                    print(f"Mensagem criptografada: {criptografado}") 
                else:
                    print("Por favor, digite uma mensagem para criptografar.")

            if event == "Descriptografar":
                criptografado = values["mensagem_criptografada"]
                if criptografado:
                    descriptografado = curva.descriptografar(criptografado, chave_secreta1)
                    if descriptografado:
                        print(f"Mensagem descriptografada: {descriptografado}")  
                    else:
                        print("Erro ao descriptografar a mensagem.")
                else:
                    print("Por favor, insira a mensagem criptografada para descriptografar.")

        window.close()
    else:
        print("Falha ao carregar a imagem.")

