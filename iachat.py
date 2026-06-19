import requests
import random
from datetime import date, timedelta

# Substitua pela sua API key da NASA (ou use "DEMO_KEY", que tem limite baixo de uso)
print("Olhe a data caso nao apareca nada")
NASA_API_KEY = "l1qecWoXtmTBg8DArocFi7Ul0xWBjTAAFRZop21I"
APOD_URL = "https://api.nasa.gov/planetary/apod"


def buscar_imagem_por_tema(tema, tentativas=45):

    tema = tema.lower()
    hoje = date.today()
    inicio_apod = date(1995, 6, 16)  # primeira foto do APOD

    for _ in range(tentativas):
        dias_totais = (hoje - inicio_apod).days
        data_aleatoria = inicio_apod + timedelta(days=random.randint(0, dias_totais))

        params = {
            "api_key": NASA_API_KEY,
            "date": data_aleatoria.isoformat(),
        }

        try:
            resposta = requests.get(APOD_URL, params=params, timeout=600)
            resposta.raise_for_status()
        except requests.RequestException as erro:
            print(f"Erro ao consultar a NASA: {erro}")
            continue

        dados = resposta.json()
        titulo = dados.get("title", "")
        explicacao = dados.get("explanation", "")

        if tema in titulo.lower() or tema in explicacao.lower():
            return dados

    return None


def mostrar_resultado(dados):
    print("\n" + "=" * 60)
    print(f"Titulo: {dados.get('title')}")
    print(f"Data: {dados.get('date')}")
    print("-" * 60)
    print(dados.get("explanation"))
    print("-" * 60)

    tipo_midia = dados.get("media_type")
    url_imagem = dados.get("hdurl") or dados.get("url")

    print(f"Link da imagem/video: {url_imagem}")

    if tipo_midia == "image" and url_imagem:
        nome_arquivo = "imagem_universo.jpg"
        try:
            img_resposta = requests.get(url_imagem, timeout=20)
            img_resposta.raise_for_status()
            with open(nome_arquivo, "wb") as arquivo:
                arquivo.write(img_resposta.content)
            print(f"Imagem salva como: {nome_arquivo}")
        except requests.RequestException as erro:
            print(f"Nao foi possivel baixar a imagem: {erro}")
    else:
        print("(Este resultado e um video, abra o link acima para ver)")

    print("=" * 60 + "\n")


def main():
    print("Fale algo sobre o universo (ex: 'marte', 'lua', 'galaxia', 'buraco negro')")
    tema = input("> ").strip()

    if not tema:
        print("Voce nao digitou nada!")
        return

    print(f"\nBuscando imagens relacionadas a '{tema}'... aguarde...")
    dados = buscar_imagem_por_tema(tema)

    if dados:
        mostrar_resultado(dados)
    else:
        print(f"\nNao encontrei nenhuma imagem relacionada a '{tema}' nas tentativas feitas. \nTente um termo mais generico (ex: 'estrela', 'planeta', 'nebulosa') ou rode novamente.")
 


if __name__ == "__main__":
    main()
