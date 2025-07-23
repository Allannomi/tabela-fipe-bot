import requests
import json

def obter_tabela() -> list | None:
    url =  'https://parallelum.com.br/fipe/api/v1/carros/marcas'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def obter_modelos(modelo:int) -> list | None:
    url = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{modelo}/modelos'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def obter_anos(modelo:int,anos:int) -> list | None:
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{modelo}/modelos/{anos}/anos" 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            return None
    except requests.exceptions.RequestException:
        return None   

def obter_valor(modelo:int, anos:int, ano_carro:str) -> list | None:
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{modelo}/modelos/{anos}/anos/{ano_carro}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def main():
    marcas = obter_tabela()
    if marcas is not None:
        for tabela in marcas:
            if 'codigo' in tabela and 'nome' in tabela:
                print(f"{tabela['codigo']:<3} | {tabela['nome']}")
    else:
        print("algo deu errado")
    while True:
        try:
            modelo = int(input("digite o codigo da marca: "))
            break
        except ValueError:
            print("digite apenas numeros")


    dados_modelo = obter_modelos(modelo)
    resultado = []

    if dados_modelo is not None and 'modelos' in dados_modelo:
        lista_modelos = dados_modelo['modelos']
        for lista in lista_modelos:
            if 'nome' in lista:
                print(f"{lista['codigo']} | {lista['nome']}")
                lista_json = {
                    "codigo_modelo": lista['codigo'],
                    "modelo": lista['nome']
                }
                resultado.append(lista_json)
        try:
            with open("carros.json", 'w', encoding="utf-8") as arquivo:
                json.dump(resultado, arquivo, indent=4, ensure_ascii=False)
            print("seu arquivo foi salvo em 'dados.json' com sucesso")
        except:
            print("não conseguimos salvar sua json")
    else:
        print("falha ao obter o modelo")


    while True:
        try:
            escolha = int(input("digite o codigo do carro: "))
            break
        except ValueError:
            print("digite apenas numero")
    
    anos = obter_anos(modelo,escolha)
    resultado_anos = []

    if anos is not None:
        for tab_anos in anos:
            if 'nome' in tab_anos and 'codigo' in tab_anos:
                print(f"{tab_anos['codigo']} | {tab_anos['nome']}")
                todos_anos = {
                    "codigo": tab_anos['codigo'],
                    "nome": tab_anos['nome'] 
                }
                resultado_anos.append(todos_anos)
        try:
            with open ("anos.json", 'w', encoding="utf-8") as arquivo:
                json.dump(resultado_anos, arquivo, indent=4, ensure_ascii=False)
            print("json salva com sucesso")
        except:
            print("não conseguimos salvar a json")
    else:
        print("algo deu errado")

    codigo_ano = input("digite o ano do carro: ")

    ano_carro = obter_valor(modelo, escolha , codigo_ano)
    resultado_valor = []

    if ano_carro is not None:
        if 'Valor' in ano_carro and 'Modelo' in ano_carro and 'Marca' in ano_carro:
            print(f"{ano_carro['Valor']} | {ano_carro['Marca']} | {ano_carro['Modelo']}")
            valores = {
                "valor": ano_carro['Valor'],
                "Marca": ano_carro['Marca'],
                "Modelo": ano_carro['Modelo']
            }
            with open("valor.json", 'w', encoding="utf-8") as arquivo:
                json.dump(valores, arquivo, indent=4, ensure_ascii= False)
                print("json salva com sucesso")
        else:
            print("nao tem todas essas respostas")
    else:
        print("erro")

if __name__ == "__main__":
    main()