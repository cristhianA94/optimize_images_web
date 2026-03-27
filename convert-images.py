import os
from PIL import Image
import pillow_heif

# CONFIGURACIÓN
DEFAULT_MAX_WIDTH = 1200   # ancho máximo por defecto
DEFAULT_MAX_HEIGHT = 0     # alto máximo por defecto (0 = sin límite)
SUPPORTED_EXTENSIONS = (".heic", ".jpg", ".jpeg", ".png")

pillow_heif.register_heif_opener()


def get_user_input():
    """Solicita al usuario la configuración de conversión."""
    print("\n" + "=" * 60)
    print("🖼️  CONVERTIDOR DE IMÁGENES A WEBP")
    print("=" * 60)
    
    # Carpeta de origen
    print("\n📂 Carpeta de origen (donde están las imágenes):")
    print("   [Por defecto: images]")
    input_dir = input("   > ").strip()
    if not input_dir:
        input_dir = "images"
    
    # Carpeta de salida
    print("\n📁 Carpeta de salida (donde se guardarán los WebP):")
    print("   [Por defecto: images-webp]")
    output_dir = input("   > ").strip()
    if not output_dir:
        output_dir = "images-webp"
    
    # Calidad
    print("\n🎨 Nivel de calidad WebP (0-100):")
    print("   [Por defecto: 80 - Recomendado para web]")
    quality_input = input("   > ").strip()
    if not quality_input:
        quality = 80
    else:
        try:
            quality = int(quality_input)
            if quality < 0 or quality > 100:
                print("   ⚠️ Valor fuera de rango. Usando 80.")
                quality = 80
        except ValueError:
            print("   ⚠️ Valor inválido. Usando 80.")
            quality = 80
    
    # Ancho
    print(f"\n📐 Ancho de las imágenes (en píxeles):")
    print(f"   [Por defecto: {DEFAULT_MAX_WIDTH} - Usar 0 para mantener original]")
    width_input = input("   > ").strip()
    if not width_input:
        max_width = DEFAULT_MAX_WIDTH
    else:
        try:
            max_width = int(width_input)
            if max_width < 0:
                print(f"   ⚠️ Valor inválido. Usando {DEFAULT_MAX_WIDTH}.")
                max_width = DEFAULT_MAX_WIDTH
        except ValueError:
            print(f"   ⚠️ Valor inválido. Usando {DEFAULT_MAX_WIDTH}.")
            max_width = DEFAULT_MAX_WIDTH
    
    # Alto
    print(f"\n📏 Alto de las imágenes (en píxeles):")
    print(f"   [Por defecto: 0 - Mantener proporción según ancho]")
    height_input = input("   > ").strip()
    if not height_input:
        max_height = DEFAULT_MAX_HEIGHT
    else:
        try:
            max_height = int(height_input)
            if max_height < 0:
                print("   ⚠️ Valor inválido. Usando 0 (sin límite).")
                max_height = 0
        except ValueError:
            print("   ⚠️ Valor inválido. Usando 0 (sin límite).")
            max_height = 0
    
    # Formato de salida
    print("\n🗂️  Formato de salida (webp / jpg):")
    print("   [Por defecto: webp]")
    format_input = input("   > ").strip().lower()
    if format_input in ("jpg", "jpeg"):
        output_format = "jpg"
    else:
        output_format = "webp"

    print("\n" + "-" * 60)
    print(f"   Origen:  {input_dir}")
    print(f"   Salida:  {output_dir}")
    print(f"   Calidad: {quality}")
    print(f"   Ancho: {max_width if max_width > 0 else 'Original'}")
    print(f"   Alto:  {max_height if max_height > 0 else 'Proporcional'}")
    print(f"   Formato: {output_format.upper()}")
    print("-" * 60)
    
    return input_dir, output_dir, quality, max_width, max_height, output_format


def resize_image(img, target_width, target_height):
    """Redimensiona la imagen a las dimensiones especificadas.
    
    - Si ambas dimensiones están definidas (>0): fuerza esas dimensiones exactas
    - Si solo ancho está definido: calcula alto proporcionalmente
    - Si solo alto está definido: calcula ancho proporcionalmente
    - Si ninguna está definida (ambas 0): devuelve imagen original
    """
    width, height = img.size
    
    if target_width > 0 and target_height > 0:
        # Ambas definidas: forzar dimensiones exactas
        new_width, new_height = target_width, target_height
    elif target_width > 0:
        # Solo ancho: calcular alto proporcional
        ratio = target_width / width
        new_width = target_width
        new_height = int(height * ratio)
    elif target_height > 0:
        # Solo alto: calcular ancho proporcional
        ratio = target_height / height
        new_width = int(width * ratio)
        new_height = target_height
    else:
        # Sin límites: mantener original
        return img
    
    # Solo redimensionar si es diferente
    if new_width != width or new_height != height:
        return img.resize((new_width, new_height), Image.LANCZOS)
    
    return img


def scan_images(input_dir):
    print("\n" + "=" * 60)
    print("📂 ESCANEANDO IMÁGENES EN:", input_dir)
    print("=" * 60)
    
    images_found = []
    total_size = 0
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                relative_path = os.path.relpath(file_path, input_dir)
                extension = os.path.splitext(file)[1].upper()
                
                images_found.append({
                    "path": file_path,
                    "relative": relative_path,
                    "name": file,
                    "size_kb": file_size,
                    "extension": extension
                })
                total_size += file_size
    
    # Mostrar resumen de imágenes encontradas
    print(f"\n📊 RESUMEN DE IMÁGENES ENCONTRADAS:")
    print("-" * 60)
    
    ext_count = {}
    for img in images_found:
        ext = img["extension"]
        ext_count[ext] = ext_count.get(ext, 0) + 1
        print(f"  {img['extension']:6} | {img['size_kb']:8.1f} KB | {img['relative']}")
    
    print("-" * 60)
    print(f"\n📈 ESTADÍSTICAS:")
    for ext, count in sorted(ext_count.items()):
        print(f"  {ext}: {count} archivos")
    print(f"\n  Total: {len(images_found)} imágenes")
    print(f"  Tamaño total: {total_size / 1024:.2f} MB")
    
    return images_found


def convert_images(images, input_dir, output_dir, quality, max_width, max_height, output_format="webp"):
    print("\n" + "=" * 60)
    print("🔄 CONVIRTIENDO A WEBP...")
    print("=" * 60)
    
    os.makedirs(output_dir, exist_ok=True)
    
    converted = 0
    errors = 0
    total_original = 0
    total_converted = 0
    
    for img_info in images:
        input_path = img_info["path"]
        relative_path = os.path.relpath(os.path.dirname(input_path), input_dir)
        
        output_subdir = os.path.join(output_dir, relative_path)
        os.makedirs(output_subdir, exist_ok=True)
        
        output_name = os.path.splitext(img_info["name"])[0] + "." + output_format
        output_path = os.path.join(output_subdir, output_name)
        
        try:
            with Image.open(input_path) as img:
                img = img.convert("RGB")
                original_dims = img.size
                img = resize_image(img, max_width, max_height)
                new_dims = img.size
                
                pil_format = "WEBP" if output_format == "webp" else "JPEG"
                save_kwargs = {"quality": quality}
                if pil_format == "WEBP":
                    save_kwargs["method"] = 6
                img.save(output_path, pil_format, **save_kwargs)
            
            original_size = os.path.getsize(input_path) / 1024
            new_size = os.path.getsize(output_path) / 1024
            reduction = ((original_size - new_size) / original_size) * 100
            
            total_original += original_size
            total_converted += new_size
            converted += 1
            
            dims_info = f"{original_dims[0]}x{original_dims[1]}"
            if original_dims != new_dims:
                dims_info += f" → {new_dims[0]}x{new_dims[1]}"
            
            #print(f"  ✔ {img_info['name']}")
            #print(f"    {original_size:.0f} KB → {new_size:.0f} KB ({reduction:.1f}% reducción)")
            #print(f"    Dimensiones: {dims_info}")
            
        except Exception as e:
            errors += 1
            print(f"  ✖ Error con {img_info['name']}: {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("✅ CONVERSIÓN COMPLETADA")
    print("=" * 60)
    print(f"  Convertidas: {converted}/{len(images)}")
    if errors > 0:
        print(f"  Errores: {errors}")
    print(f"\n  Tamaño original: {total_original / 1024:.2f} MB")
    print(f"  Tamaño final: {total_converted / 1024:.2f} MB")
    if total_original > 0:
        total_reduction = ((total_original - total_converted) / total_original) * 100
        print(f"  Reducción total: {total_reduction:.1f}%")
    print(f"\n  📁 Imágenes guardadas en: {output_dir}")


if __name__ == "__main__":
    # Obtener configuración del usuario
    input_dir, output_dir, quality, max_width, max_height, output_format = get_user_input()
    
    if not os.path.exists(input_dir):
        print(f"\n❌ El directorio '{input_dir}' no existe.")
        exit(1)
    
    images = scan_images(input_dir)
    
    if not images:
        print("\n⚠️ No se encontraron imágenes para convertir.")
        exit(0)
    
    print(f"\n¿Deseas convertir {len(images)} imágenes a WebP? (s/n): ", end="")
    response = input().strip().lower()
    
    if response in ("s", "si", "sí", "y", "yes"):
        convert_images(images, input_dir, output_dir, quality, max_width, max_height, output_format)
    else:
        print("\n❌ Conversión cancelada.")
