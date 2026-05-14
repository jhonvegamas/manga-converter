<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/MangaConv-v1.0-6b4cf5?style=for-the-badge&logo=python&logoColor=white&labelColor=0a1530">
    <img src="https://img.shields.io/badge/MangaConv-v1.0-6b4cf5?style=for-the-badge&logo=python&logoColor=white&labelColor=0a1530" alt="MangaConv">
  </picture>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/PDF-%E2%9E%A1%EF%B8%8F-CBZ-6b4cf5" alt="PDF to CBZ">
</p>

---

# MangaConv

**Convert manga & manhwa PDFs to CBZ — optimized for e-readers like Kindle, PocketBook, Kobo, and reMarkable.**

MangaConv is a modern desktop GUI application that transforms your comic and manga PDF collections into device-optimized CBZ files. It automatically detects whether a PDF is **manga** (standard pages) or **manhwa** (tall scroll-format pages), splits oversized pages for comfortable reading, and resizes images to match your e-reader's screen — all with a clean, intuitive interface.

---

## ✨ Features

- **Automatic mode detection** — AI-free heuristic distinguishes manga from manhwa by analyzing aspect ratios across the first 50 pages
- **Smart page splitting** — Tall manhwa/webtoon pages are split into readable sections that fit your device screen
- **20+ built-in device profiles** — Optimized resolutions for PocketBook, Kindle, Kobo, and reMarkable models
- **Real-time preview** — See before/after thumbnails as you tweak settings
- **Image adjustments** — Gamma correction, grayscale conversion, autocontrast
- **Custom profiles** — Save your own resolution presets
- **Batch conversion** — Process multiple PDFs at once with parallel workers
- **Output to CBZ** — Standard comic book zip format with JPEG compression (quality 92)
- **Modern GUI** — Clean Notion-inspired design built with customtkinter
- **Lightweight & offline** — No internet required, runs entirely on your machine

---

## 🖼️ Screenshots

> _Screenshots coming soon — the app features a navy header, drop zone, device selector, gamma slider, before/after preview panels, and a progress bar._

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Install

```bash
# Clone the repository
git clone https://github.com/yourusername/MangaConv.git
cd MangaConv

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Build a standalone executable (optional)

```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller MangaConv.spec

# The executable will be in the dist/ directory
```

---

## 📖 Usage

1. **Launch** — Run `python main.py` (or the compiled `.exe`)
2. **Select PDF** — Drag and drop one or more PDF files onto the drop zone, or click to browse
3. **Choose mode** — Auto (recommended), Manga, or Manhwa
4. **Pick your device** — Select from built-in profiles (Kindle Paperwhite, PocketBook InkPad, etc.) or enter custom resolution
5. **Adjust image** — Tweak gamma, enable grayscale, or autocontrast as needed
6. **Preview** — See the effect of your settings in real-time
7. **Convert** — Click "Convertir a CBZ" and select an output folder
8. **Enjoy!** — Your CBZ files are ready to transfer to your e-reader

### Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+O` | Open PDF files |

---

## 📱 Supported Devices

| Brand | Models |
|-------|--------|
| **PocketBook** | Verse Pro Color, InkPad Color 3, Era, Touch HD 3 |
| **Kindle** | Basic 11 (2024), Paperwhite 5/6, Scribe (2022/2025), Oasis 2/3, Voyage, Colorsoft |
| **Kobo** | Libra Colour, Clara BW, Clara Colour, Elipsa 2E, Sage, Forma |
| **reMarkable** | reMarkable 2, Paper Pro |
| **Custom** | Any resolution you define |

---

## 🧠 How it works

1. **Detection**: Scans the first 50 pages — if ≥30% have an aspect ratio >2:1, it's classified as manhwa
2. **Extraction**: Uses PyMuPDF (fitz) to extract high-quality page images
3. **Processing**: Applies gamma, grayscale, autocontrast, and device-specific resize
4. **Splitting**: Manhwa pages are divided into screen-sized sections
5. **Packaging**: All images are zipped into a `.cbz` file with JPEG compression

---

## 🛠️ Tech Stack

- **[customtkinter](https://github.com/TomSchimansky/CustomTkinter)** — Modern tkinter UI framework
- **[PyMuPDF (fitz)](https://pypi.org/project/PyMuPDF/)** — PDF rendering & image extraction
- **[Pillow](https://python-pillow.org/)** — Image processing (resize, gamma, autocontrast)
- **ThreadPoolExecutor** — Parallel page processing for fast conversion

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## ⭐ Support

If you find this tool useful, please consider giving it a ⭐ on GitHub — it helps others discover it too!

---

<br>

<p align="center">
  <b>English</b> &nbsp;·&nbsp; <a href="#mangaconv-1">Español</a>
</p>

<br>
<br>
<br>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/MangaConv-v1.0-6b4cf5?style=for-the-badge&logo=python&logoColor=white&labelColor=0a1530">
    <img src="https://img.shields.io/badge/MangaConv-v1.0-6b4cf5?style=for-the-badge&logo=python&logoColor=white&labelColor=0a1530" alt="MangaConv">
  </picture>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Licencia-MIT-green" alt="Licencia">
  <img src="https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Plataforma">
  <img src="https://img.shields.io/badge/PDF-%E2%9E%A1%EF%B8%8F-CBZ-6b4cf5" alt="PDF a CBZ">
</p>

---

# MangaConv

**Convierte PDFs de manga y manhwa a CBZ — optimizado para lectores electrónicos como Kindle, PocketBook, Kobo y reMarkable.**

MangaConv es una aplicación moderna de escritorio con interfaz gráfica que transforma tus colecciones de cómics y manga en archivos CBZ optimizados para tu dispositivo. Detecta automáticamente si un PDF es **manga** (páginas normales) o **manhwa** (formato de scroll alargado), divide páginas sobredimensionadas para una lectura cómoda y redimensiona las imágenes para que coincidan con la pantalla de tu lector — todo con una interfaz limpia e intuitiva.

---

## ✨ Características

- **Detección automática de modo** — Heurística que distingue manga de manhwa analizando las proporciones de las primeras 50 páginas
- **División inteligente de páginas** — Páginas alargadas de manhwa/webtoon se dividen en secciones que caben en tu pantalla
- **Más de 20 perfiles de dispositivo** — Resoluciones optimizadas para PocketBook, Kindle, Kobo y reMarkable
- **Vista previa en tiempo real** — Compara antes/después mientras ajustas la configuración
- **Ajustes de imagen** — Corrección gamma, conversión a escala de grises, autocontraste
- **Perfiles personalizados** — Guarda tus propias resoluciones
- **Conversión por lotes** — Procesa múltiples PDFs a la vez con workers paralelos
- **Salida a CBZ** — Formato estándar de cómic en zip con compresión JPEG (calidad 92)
- **GUI moderna** — Diseño limpio inspirado en Notion construido con customtkinter
- **Ligero y sin conexión** — No requiere internet, funciona completamente en tu máquina

---

## 🖼️ Capturas de pantalla

> _Capturas próximamente — la app incluye encabezado azul marino, zona de arrastre, selector de dispositivo, slider gamma, paneles de vista previa y barra de progreso._

---

## 🚀 Instalación

### Requisitos

- Python 3.10 o superior
- pip (instalador de paquetes de Python)

### Instalar

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/MangaConv.git
cd MangaConv

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

### Crear un ejecutable independiente (opcional)

```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar
pyinstaller MangaConv.spec

# El ejecutable estará en el directorio dist/
```

---

## 📖 Cómo usar

1. **Inicia** — Ejecuta `python main.py` (o el `.exe` compilado)
2. **Selecciona PDF** — Arrastra uno o varios PDFs a la zona de carga, o haz clic para buscar
3. **Elige modo** — Auto (recomendado), Manga o Manhwa
4. **Selecciona tu dispositivo** — Escoge entre los perfiles predefinidos (Kindle Paperwhite, PocketBook InkPad, etc.) o ingresa una resolución personalizada
5. **Ajusta la imagen** — Modifica gamma, activa escala de grises o autocontraste
6. **Vista previa** — Observa el efecto de los ajustes en tiempo real
7. **Convierte** — Haz clic en "Convertir a CBZ" y elige la carpeta de destino
8. **¡Disfruta!** — Tus archivos CBZ están listos para transferir a tu lector

### Atajos de teclado

| Tecla | Acción |
|-------|--------|
| `Ctrl+O` | Abrir archivos PDF |

---

## 📱 Dispositivos compatibles

| Marca | Modelos |
|-------|---------|
| **PocketBook** | Verse Pro Color, InkPad Color 3, Era, Touch HD 3 |
| **Kindle** | Basic 11 (2024), Paperwhite 5/6, Scribe (2022/2025), Oasis 2/3, Voyage, Colorsoft |
| **Kobo** | Libra Colour, Clara BW, Clara Colour, Elipsa 2E, Sage, Forma |
| **reMarkable** | reMarkable 2, Paper Pro |
| **Personalizado** | Cualquier resolución que definas |

---

## 🧠 Cómo funciona

1. **Detección**: Escanea las primeras 50 páginas — si ≥30% tienen una relación de aspecto >2:1, se clasifica como manhwa
2. **Extracción**: Usa PyMuPDF (fitz) para extraer imágenes de página de alta calidad
3. **Procesamiento**: Aplica gamma, escala de grises, autocontraste y redimensionamiento específico del dispositivo
4. **División**: Las páginas de manhwa se parten en secciones del tamaño de la pantalla
5. **Empaquetado**: Todas las imágenes se comprimen en un archivo `.cbz` con compresión JPEG

---

## 🛠️ Tecnologías

- **[customtkinter](https://github.com/TomSchimansky/CustomTkinter)** — Framework moderno de interfaz gráfica para tkinter
- **[PyMuPDF (fitz)](https://pypi.org/project/PyMuPDF/)** — Renderizado y extracción de imágenes de PDF
- **[Pillow](https://python-pillow.org/)** — Procesamiento de imágenes (redimensionar, gamma, autocontraste)
- **ThreadPoolExecutor** — Procesamiento paralelo de páginas para conversión rápida

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT — consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Siéntete libre de abrir un issue o enviar un pull request.

---

## ⭐ Apoyo

Si esta herramienta te resulta útil, considera darle una ⭐ en GitHub — ¡ayuda a que otros también la descubran!

---

<br>

<p align="center">
  <a href="#mangaconv">English</a> &nbsp;·&nbsp; <b>Español</b>
</p>
