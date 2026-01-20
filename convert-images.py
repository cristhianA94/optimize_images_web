import os
from PIL import Image
import pillow_heif

# CONFIGURACIÓN
MAX_WIDTH = 1200          # ancho máximo para web
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
    
    print("\n" + "-" * 60)
    print(f"   Origen:  {input_dir}")
    print(f"   Salida:  {output_dir}")
    print(f"   Calidad: {quality}")
    print("-" * 60)
    
    return input_dir, output_dir, quality


def resize_image(img, max_width):
    width, height = img.size
    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)
        return img.resize((max_width, new_height), Image.LANCZOS)
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


def convert_images(images, input_dir, output_dir, quality):
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
        
        output_name = os.path.splitext(img_info["name"])[0] + ".webp"
        output_path = os.path.join(output_subdir, output_name)
        
        try:
            with Image.open(input_path) as img:
                img = img.convert("RGB")
                original_dims = img.size
                img = resize_image(img, MAX_WIDTH)
                new_dims = img.size
                
                img.save(
                    output_path,
                    "WEBP",
                    quality=quality,
                    method=6
                )
            
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
    input_dir, output_dir, quality = get_user_input()
    
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
        convert_images(images, input_dir, output_dir, quality)
    else:
        print("\n❌ Conversión cancelada.")
