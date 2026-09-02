import os
import urllib.request

# Criar a pasta para as imagens de teste se ela não existir
folder_name = "imagens_teste"
os.makedirs(folder_name, exist_ok=True)

# Lista de imagens com URLs diretas e públicas
images_to_download = {
    "1_cameraman_fourier.png": "https://raw.githubusercontent.com/camieac/image-processing-matlab/master/lab01/images/cameraman.tif",
    "2_siemens_star_aliasing.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Siemens_star_spoke_pattern.svg/1024px-Siemens_star_spoke_pattern.svg.png",
    "3_por_do_sol_quantizacao.jpg": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1000&q=80",
    "4_arara_chroma.jpg": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?auto=format&fit=crop&w=1000&q=80",
}

print("Iniciando o download das imagens de teste...")

for filename, url in images_to_download.items():
    filepath = os.path.join(folder_name, filename)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with (
            urllib.request.urlopen(req) as response,
            open(filepath, "wb") as out_file,
        ):
            out_file.write(response.read())
        print(f"  [OK] Baixado: {filename}")
    except Exception as e:
        print(f"  [ERRO] Falha ao baixar {filename}: {e}")

print(
    f"\nConcluído! As imagens foram salvas na pasta '{os.path.abspath(folder_name)}'."
)