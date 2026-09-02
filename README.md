# 🖼️ PDI: Amostragem, Quantização & Transformada de Fourier

Uma aplicação interativa desenvolvida em **Python** e **Streamlit** para demonstração prática e didática de conceitos fundamentais do **Processamento Digital de Imagens (PDI)**, como amostragem espacial, teorema de Nyquist, aliasing, quantização de intensidade, dithering, subamostragem de crominância e análise no domínio da frequência (FFT).

---

## 🚀 Funcionalidades

- **Múltiplas Fontes de Imagem:**
  - Upload manual de imagens (`JPG`, `PNG`).
  - Carregamento de imagens de teste locais.
  - Geração de imagens sintéticas parametrizadas via slider.
  
- **Amostragem Espacial & Aliasing:**
  - Redução de resolução espacial parametrizada.
  - Filtro Anti-Aliasing (Passa-Baixa Gaussiano) configurável.
  - **Detecção Automática de Aliasing** com base na taxa de amostragem e no Teorema de Nyquist ($f_s \ge 2 \cdot f_{max}$).

- **Quantização de Intensidade:**
  - Redução da profundidade de bits (1 a 8 bits / 2 a 256 níveis de cinza).
  - Algoritmo de **Dithering de Floyd-Steinberg** para minimização de artefatos visuais.
  - Mapa visual de erro de quantização.

- **Domínio da Frequência (Transformada de Fourier - 2D FFT):**
  - Espectro de Magnitude e Fase da imagem.
  - Visualização gráfica com colormaps (`viridis` e `hsv`).
  - Reconstrução da imagem apenas com informação de magnitude.

- **Subamostragem de Crominância (Espaço de Cor YCbCr):**
  - Simulação dos padrões **4:4:4**, **4:2:2** e **4:2:0**.
  - Comparação visual direta com a imagem original em RGB e mapa de diferença de perdas.

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3](https://www.python.org/)** — Linguagem principal
- **[Streamlit](https://streamlit.io/)** — Interface web interativa
- **[OpenCV (cv2)](https://opencv.org/)** — Processamento de imagem
- **[NumPy](https://numpy.org/)** — Computação científica e manipulação de matrizes
- **[Matplotlib](https://matplotlib.org/)** — Visualização gráfica de espectros

---

## 📦 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o [Python](https://www.python.org/) instalado em sua máquina.

### 1. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio