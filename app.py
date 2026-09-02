import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(
    layout="wide", page_title="PDI: Amostragem, Quantização & Fourier"
)

st.title("Processamento Digital de Imagens")
st.write(
    "Demonstração prática dos conceitos de Amostragem, Quantização, Aliasing e Transformada de Fourier."
)

# --- SELEÇÃO DA FONTE DA IMAGEM ---
st.sidebar.subheader("Fonte da Imagem")
modo_imagem = st.sidebar.radio(
    "Escolha a origem da imagem:",
    ["Upload Manual", "Imagens de Teste Locais", "Imagem Sintética"],
)

TEST_DIR = "imagens_teste"
img_orig = None
img_rgb = None
uploaded_file = None

if modo_imagem == "Upload Manual":
    uploaded_file = st.sidebar.file_uploader(
        "Envie uma imagem", type=["jpg", "png", "jpeg"]
    )
    if uploaded_file is not None:
        file_bytes = np.asarray(
            bytearray(uploaded_file.read()), dtype=np.uint8
        )
        img_orig = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        img_rgb = cv2.cvtColor(
            cv2.imdecode(file_bytes, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB
        )

elif modo_imagem == "Imagens de Teste Locais":
    if os.path.exists(TEST_DIR):
        arquivos = [
            f
            for f in os.listdir(TEST_DIR)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        if arquivos:
            imagem_selecionada = st.sidebar.selectbox(
                "Selecione uma imagem de teste:", arquivos
            )
            caminho_img = os.path.join(TEST_DIR, imagem_selecionada)
            img_orig = cv2.imread(caminho_img, cv2.IMREAD_GRAYSCALE)
            img_bgr = cv2.imread(caminho_img, cv2.IMREAD_COLOR)
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        else:
            st.sidebar.warning(
                f"Nenhuma imagem encontrada na pasta '{TEST_DIR}'."
            )
    else:
        st.sidebar.error(
            f"A pasta '{TEST_DIR}' não existe. Execute o script de download primeiro."
        )

# Fallback para imagem sintética caso nada seja selecionado/carregado
if img_orig is None:
    freq_control = st.sidebar.slider("Frequência da imagem sintética", 1, 20, 8)
    x = np.linspace(0, 10, 512)
    y = np.linspace(0, 10, 512)
    X, Y = np.meshgrid(x, y)
    img_orig = ((np.sin(freq_control * (X**2 + Y**2)) * 127 + 128)).astype(
        np.uint8
    )
    img_rgb = cv2.cvtColor(img_orig, cv2.COLOR_GRAY2RGB)
    freq_control_val = freq_control
else:
    freq_control_val = None

H_orig, W_orig = img_orig.shape

# --- AMOSTRAGEM ESPACIAL ---
st.sidebar.subheader("Amostragem Espacial")
scale_factor = st.sidebar.slider(
    "Fator de Amostragem (%)", 1, 100, 100, step=2
)
apply_antialiasing = st.sidebar.checkbox(
    "Aplicar Filtro Anti-Aliasing (Passa-Baixa)", value=False
)

if apply_antialiasing:
    sigma = st.sidebar.slider(
        "Sigma do filtro Gaussiano", 0.5, 5.0, 1.5, step=0.1
    )
    ksize = int(6 * sigma) | 1
    img_sampled = cv2.GaussianBlur(img_orig, (ksize, ksize), sigma)
else:
    img_sampled = img_orig.copy()

new_W = max(1, int(W_orig * (scale_factor / 100.0)))
new_H = max(1, int(H_orig * (scale_factor / 100.0)))
img_low_res = cv2.resize(
    img_sampled, (new_W, new_H), interpolation=cv2.INTER_NEAREST
)
img_display_sampled = cv2.resize(
    img_low_res, (W_orig, H_orig), interpolation=cv2.INTER_NEAREST
)

# ==============================================================================
# CÁLCULO DE ALIASING SIMPLIFICADO (TEOREMA DE NYQUIST: fs >= 2 * fmax)
# ==============================================================================
if freq_control_val is not None:
    # 1. Quantidade de pixels disponíveis na largura após a amostragem (f_s)
    pixels_amostrados = new_W
    
    # 2. Mínimo de pixels necessários para capturar as ondas sem aliasing (2 * f_max)
    # Cada unidade do slider representa 'ciclos de onda' na imagem
    pixels_minimos_nyquist = 2 * freq_control_val
    
    # 3. Se temos menos pixels que o mínimo exigido por Nyquist, ocorre aliasing!
    aliasing_warning = pixels_amostrados < pixels_minimos_nyquist
else:
    # Para imagens reais, verificamos se há frequências altas fora do raio amostragem
    freq_orig = np.fft.fft2(img_orig)
    freq_shift_orig = np.fft.fftshift(freq_orig)
    magnitude_orig = 20 * np.log(np.abs(freq_shift_orig) + 1)
    h, w = magnitude_orig.shape
    center_h, center_w = h // 2, w // 2
    
    # Raio de Nyquist baseado na nova resolução
    radius = int(min(h, w) * (scale_factor / 100.0) / 2.0)
    
    mask = np.zeros((h, w), dtype=bool)
    Y_grid, X_grid = np.ogrid[:h, :w]
    mask[(Y_grid - center_h) ** 2 + (X_grid - center_w) ** 2 <= radius**2] = True
    
    energy_inside = np.sum(magnitude_orig[mask])
    energy_outside = np.sum(magnitude_orig[~mask]) if np.sum(~mask) > 0 else 0
    aliasing_warning = energy_outside > energy_inside * 0.1 and scale_factor < 100

# Se o filtro passa-baixa anti-aliasing for aplicado, ele remove o aliasing
if apply_antialiasing:
    aliasing_warning = False

# --- QUANTIZAÇÃO DE INTENSIDADE ---
st.sidebar.subheader("Quantização de Intensidade")
bits = st.sidebar.slider("Profundidade de Bits", 1, 8, 8)
use_dithering = st.sidebar.checkbox(
    "Aplicar Dithering (Floyd-Steinberg)", value=False
)


def quantize(img, num_bits):
    levels = 2**num_bits
    factor = 255 / (levels - 1) if levels > 1 else 255
    quantized = np.round(img / factor) * factor
    return quantized.astype(np.uint8)


def floyd_steinberg_dithering(img, num_bits):
    levels = 2**num_bits
    factor = 255 / (levels - 1) if levels > 1 else 255
    img_float = img.astype(float)
    h, w = img_float.shape
    for y in range(h):
        for x in range(w):
            old_val = img_float[y, x]
            new_val = np.round(old_val / factor) * factor
            img_float[y, x] = new_val
            err = old_val - new_val
            if x + 1 < w:
                img_float[y, x + 1] += err * 7 / 16
            if x - 1 >= 0 and y + 1 < h:
                img_float[y + 1, x - 1] += err * 3 / 16
            if y + 1 < h:
                img_float[y + 1, x] += err * 5 / 16
            if x + 1 < w and y + 1 < h:
                img_float[y + 1, x + 1] += err * 1 / 16
    return np.clip(img_float, 0, 255).astype(np.uint8)


if use_dithering and bits < 8:
    img_quantized = floyd_steinberg_dithering(img_display_sampled, bits)
else:
    img_quantized = quantize(img_display_sampled, bits)

quantization_error = np.abs(
    img_display_sampled.astype(float) - img_quantized.astype(float)
).astype(np.uint8)

# Transformada de Fourier
f_transform = np.fft.fft2(img_quantized)
f_shift = np.fft.fftshift(f_transform)
magnitude_spectrum = 20 * np.log(np.abs(f_shift) + 1)
phase_spectrum = np.angle(f_shift)

# --- SUBAMOSTRAGEM DE CROMINÂNCIA ---
st.sidebar.subheader("Subamostragem de Crominância (YCbCr)")
chroma_subsampling = st.sidebar.selectbox(
    "Padrão de Subamostragem", ["4:4:4", "4:2:2", "4:2:0"]
)


def apply_chroma_subsampling(img_input_rgb, pattern):
    ycbcr = cv2.cvtColor(img_input_rgb, cv2.COLOR_RGB2YCrCb)
    y, cb, cr = cv2.split(ycbcr)
    h, w = y.shape
    if pattern == "4:4:4":
        cb_sampled, cr_sampled = cb, cr
    elif pattern == "4:2:2":
        cb_sampled = cv2.resize(
            cb, (w // 2, h), interpolation=cv2.INTER_NEAREST
        )
        cb_sampled = cv2.resize(
            cb_sampled, (w, h), interpolation=cv2.INTER_NEAREST
        )
        cr_sampled = cv2.resize(
            cr, (w // 2, h), interpolation=cv2.INTER_NEAREST
        )
        cr_sampled = cv2.resize(
            cr_sampled, (w, h), interpolation=cv2.INTER_NEAREST
        )
    else:
        cb_sampled = cv2.resize(
            cb, (w // 2, h // 2), interpolation=cv2.INTER_NEAREST
        )
        cb_sampled = cv2.resize(
            cb_sampled, (w, h), interpolation=cv2.INTER_NEAREST
        )
        cr_sampled = cv2.resize(
            cr, (w // 2, h // 2), interpolation=cv2.INTER_NEAREST
        )
        cr_sampled = cv2.resize(
            cr_sampled, (w, h), interpolation=cv2.INTER_NEAREST
        )
    ycbcr_sampled = cv2.merge([y, cb_sampled, cr_sampled])
    return cv2.cvtColor(ycbcr_sampled, cv2.COLOR_YCrCb2RGB)


img_chroma = apply_chroma_subsampling(img_rgb, chroma_subsampling)

# --- INTERFACE DE EXIBIÇÃO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Imagem Original")
    st.image(img_rgb, use_container_width=True)
    if aliasing_warning:
        st.warning(
            "⚠️ Aliasing detectado! A taxa de amostragem está abaixo do limite de Nyquist."
        )
    else:
        st.success("✅ Amostragem adequada (acima do limite de Nyquist)")

with col2:
    st.subheader("Imagem Processada")
    st.image(
        img_quantized,
        caption=f"Resolução: {new_W}x{new_H} | {bits} bits ({2**bits} níveis)",
        use_container_width=True,
    )
    bytes_per_pixel = bits / 8.0
    size_bytes = new_W * new_H * bytes_per_pixel
    st.info(f"**Tamanho Bruto:** {size_bytes / 1024:.2f} KB")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Erro de Quantização")
    st.image(quantization_error, use_container_width=True)
    st.caption("Áreas mais claras indicam maior perda de informação")

with col4:
    st.subheader("Espectro de Fourier (Magnitude)")
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(magnitude_spectrum, cmap="viridis")
    plt.colorbar(im, ax=ax)
    ax.set_title("Magnitude da FFT (baixas freq. no centro)")
    st.pyplot(fig)
    plt.close(fig)

col5, col6 = st.columns(2)

with col5:
    st.subheader("Espectro de Fourier (Fase)")
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(phase_spectrum, cmap="hsv")
    plt.colorbar(im, ax=ax)
    ax.set_title("Fase da FFT")
    st.pyplot(fig)
    plt.close(fig)

with col6:
    st.subheader("Reconstrução com Magnitude")
    magnitude_only = np.abs(f_shift)
    reconstructed_mag = np.fft.ifft2(np.fft.ifftshift(magnitude_only)).real
    st.image(
        np.clip(reconstructed_mag, 0, 255).astype(np.uint8),
        use_container_width=True,
    )
    st.caption(
        "Imagem reconstruída apenas com magnitude (perda de estrutura)"
    )

st.subheader("Subamostragem de Crominância (YCbCr)")
col7, col8, col9 = st.columns(3)
with col7:
    st.image(img_chroma, use_container_width=True)
    st.caption(f"Crominância: {chroma_subsampling}")
with col8:
    st.image(img_rgb, use_container_width=True)
    st.caption("Original RGB")
with col9:
    diff_chroma = np.abs(
        img_rgb.astype(float) - img_chroma.astype(float)
    ).astype(np.uint8)
    st.image(diff_chroma, use_container_width=True)
    st.caption("Diferença (perda visual)")

with st.expander("Resumo Teórico e Observações"):
    st.markdown(f"""
    **Amostragem e Nyquist**
    - Status: {'⚠️ ALIASING DETECTADO' if aliasing_warning else '✅ Amostragem adequada'}
    - Resolução atual: {new_W}x{new_H}
    - Fator de amostragem: {scale_factor}%
    
    **Quantização**
    - Profundidade atual: {bits} bits ({2**bits} níveis)
    - Erro médio de quantização: {np.mean(quantization_error):.2f}
    - {'Dithering aplicado' if use_dithering and bits < 8 else 'Sem dithering'}
    
    **Subamostragem de Crominância**
    - Padrão atual: {chroma_subsampling}
    - Redução de dados: {'Nenhuma' if chroma_subsampling == '4:4:4' else '50%' if chroma_subsampling == '4:2:2' else '75%'}
    
    **Transformada de Fourier**
    - A magnitude mostra a força de cada frequência
    - A fase determina a posição espacial das estruturas
    - Reconstrução apenas com magnitude perde detalhes estruturais
    """)