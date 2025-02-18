import os
import rawpy
import imageio
from PIL import Image
from datetime import datetime

def identificar_formato_e_converter(arquivo, pasta_destino):
    # Tenta abrir com PIL (para formatos como PNG, JPG, TIFF, etc.)
    try:
        with Image.open(arquivo) as img:
            if img.format in ['PNG', 'TIFF', 'BMP', 'GIF']:
                nome_jpeg = os.path.splitext(os.path.basename(arquivo))[0] + ".jpg"
                caminho_saida = os.path.join(pasta_destino, nome_jpeg)
                img.convert('RGB').save(caminho_saida, 'JPEG', quality=90)
                return f"✅ Convertido: {arquivo} -> {nome_jpeg}"
    except Exception as e:
        pass

    # Tenta abrir como arquivo RAW (usando rawpy para arquivos .cr2, .nef, .dng, etc.)
    try:
        with rawpy.imread(arquivo) as raw:
            imagem_rgb = raw.postprocess()
            nome_jpeg = os.path.splitext(os.path.basename(arquivo))[0] + ".jpg"
            caminho_saida = os.path.join(pasta_destino, nome_jpeg)
            imageio.imwrite(caminho_saida, imagem_rgb, quality=90)
            return f"✅ Convertido: {arquivo} -> {nome_jpeg}"
    except Exception as e:
        return f"❌ ERRO ao converter {arquivo}: {e}"

def converter_pasta(pasta_origem):
    pasta_destino = os.path.join(pasta_origem, "Convertidas_JPEG")
    os.makedirs(pasta_destino, exist_ok=True)

    log_path = os.path.join(pasta_origem, "log_conversao.txt")
    with open(log_path, "w", encoding="utf-8") as log:
        log.write("===== Início da Conversão =====\n")
        log.write(f"Data/Hora: {datetime.now()}\n")
        log.write(f"Pasta de origem: {pasta_origem}\n")
        log.write(f"Pasta de destino: {pasta_destino}\n\n")

        # Encontrar todos os arquivos na pasta
        arquivos = [f for f in os.listdir(pasta_origem) if os.path.isfile(os.path.join(pasta_origem, f))]
        if not arquivos:
            log.write("⚠️ Nenhum arquivo encontrado!\n")
            print("⚠️ Nenhum arquivo encontrado!")
            return

        log.write(f"🔎 {len(arquivos)} arquivos encontrados.\n")

        convertidos = 0
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta_origem, arquivo)
            resultado = identificar_formato_e_converter(caminho_arquivo, pasta_destino)
            log.write(resultado + "\n")
            print(resultado)

            if "✅ Convertido" in resultado:
                convertidos += 1

        log.write(f"\n✅ {convertidos} imagens foram convertidas com sucesso!\n")
        log.write("===== Fim da Conversão =====\n")
    
    print("✅ Processo concluído! Verifique a pasta e o log.")

if __name__ == "__main__":
    pasta = input("Digite o caminho da pasta de imagens: ")
    if os.path.exists(pasta):
        converter_pasta(pasta)
    else:
        print("❌ Caminho inválido. Verifique o diretório.")
