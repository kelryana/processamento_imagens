# 🖼️ PDI: Amostragem, Quantização & Transformada de Fourier
<img width="2507" height="918" alt="image" src="https://github.com/user-attachments/assets/3850b70a-7b88-4dc7-8bd4-d912a591cb53" />

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
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar e ativar o Ambiente Virtual

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**No Windows (CMD / PowerShell):**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as dependências
```bash
pip install streamlit opencv-python matplotlib numpy
```

### 4. Executar a aplicação Streamlit
```bash
streamlit run app.py
```
*(Substitua `app.py` pelo nome exato do seu arquivo Python principal, se for diferente).*

Acesse a aplicação no navegador em `http://localhost:8501`.

---

## 📁 Estrutura do Projeto

```text
├── imagens_teste/        # (Opcional) Pasta com imagens para testes locais
├── app.py                # Código principal da aplicação Streamlit
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Documentação do projeto
```

---
