# 🖼️ Optimize Images Web

Herramienta de línea de comandos para optimizar imágenes para web, convirtiéndolas a formato WebP con redimensionado automático.

## ✨ Características

- ✔ Recorre directorios recursivamente
- ✔ Detecta `.HEIC`, `.jpg`, `.jpeg`, `.png`
- ✔ Redimensiona automáticamente a tamaño web (máx. 1200px de ancho)
- ✔ Convierte todo a formato WebP
- ✔ Nivel de compresión configurable (0-100)
- ✔ Mantiene la estructura de carpetas original
- ✔ Muestra estadísticas de reducción de tamaño

## 📋 Requisitos

- Python 3.7+
- Pillow
- pillow-heif (para soporte HEIC)

## 🔧 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/cristhianA94/optimize_images_web.git
cd optimize_images_web

# Instalar dependencias
pip install Pillow pillow-heif
```

## 🚀 Uso

Ejecuta el script y sigue las instrucciones interactivas:

```bash
python convert-images.py
```

### Flujo interactivo

```
============================================================
🖼️  CONVERTIDOR DE IMÁGENES A WEBP
============================================================

📂 Carpeta de origen (donde están las imágenes):
   [Por defecto: images]
   > mis-fotos

📁 Carpeta de salida (donde se guardarán los WebP):
   [Por defecto: images-webp]
   > output

🎨 Nivel de calidad WebP (0-100):
   [Por defecto: 80 - Recomendado para web]
   > 85

------------------------------------------------------------
   Origen:  mis-fotos
   Salida:  output
   Calidad: 85
------------------------------------------------------------
```

### Parámetros

| Parámetro      | Valor por defecto | Descripción                                             |
| -------------- | ----------------- | ------------------------------------------------------- |
| Carpeta origen | `images`          | Directorio con las imágenes originales                  |
| Carpeta salida | `images-webp`     | Directorio donde se guardan los WebP                    |
| Calidad        | `80`              | Nivel de compresión WebP (0-100, mayor = mejor calidad) |

### Guía de calidad

| Nivel | Uso recomendado                    |
| ----- | ---------------------------------- |
| 60-70 | Thumbnails, imágenes pequeñas      |
| 75-85 | **Web general (recomendado)**      |
| 85-95 | Fotografía, alta calidad           |
| 100   | Sin pérdida (archivos más grandes) |

## 📊 Ejemplo de salida

```
============================================================
📂 ESCANEANDO IMÁGENES EN: images
============================================================

📊 RESUMEN DE IMÁGENES ENCONTRADAS:
------------------------------------------------------------
  .HEIC  |   2048.5 KB | foto1.heic
  .JPG   |   1523.2 KB | subfolder/foto2.jpg
  .PNG   |   3421.8 KB | icons/logo.png
------------------------------------------------------------

📈 ESTADÍSTICAS:
  .HEIC: 1 archivos
  .JPG: 1 archivos
  .PNG: 1 archivos

  Total: 3 imágenes
  Tamaño total: 6.83 MB

¿Deseas convertir 3 imágenes a WebP? (s/n): s

============================================================
🔄 CONVIRTIENDO A WEBP...
============================================================

============================================================
✅ CONVERSIÓN COMPLETADA
============================================================
  Convertidas: 3/3

  Tamaño original: 6.83 MB
  Tamaño final: 1.24 MB
  Reducción total: 81.8%

  📁 Imágenes guardadas en: images-webp
```

## 📁 Estructura de salida

El script mantiene la estructura de carpetas original:

```
images/                     images-webp/
├── foto1.heic        →     ├── foto1.webp
├── subfolder/              ├── subfolder/
│   └── foto2.jpg     →     │   └── foto2.webp
└── icons/                  └── icons/
    └── logo.png      →         └── logo.webp
```

## 📄 Licencia

MIT License
