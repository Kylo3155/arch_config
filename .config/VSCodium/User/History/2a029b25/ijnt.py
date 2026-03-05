import subprocess
import random
import requests
import re
import time
import os

# CONFIGURACIÓN DE NAVEGADOR (Para evitar bloqueos)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

def enviar_notificacion(titulo, mensaje, urgencia="normal"):
    """
    Envía una notificación usando notify-send.
    Niveles de urgencia: low, normal, critical
    """
    try:
        subprocess.run([
            "notify-send",
            titulo,
            mensaje,
            f"--urgency={urgencia}",
            "--app-name=MiScriptPython", # Aparecerá en el panel de SwayNC
            "--icon=dialog-information"  # Puedes poner la ruta a un .png
        ], check=True)
        print("Notificación enviada.")
    except Exception as e:
        print(f"Error al enviar la notificación: {e}")

def iniciar_descargador():
    print("--- 🎬 XNXX Random Downloader Interactivo ---")
    
    # 1. Entrada de datos por el usuario
    keyword = input("👉 ¿Qué quieres buscar? (ej. latina, vlogs, etc.): ").strip()
    if not keyword:
        print("❌ Debes ingresar una palabra clave.")
        return

    category = input("👉 ¿Qué categoria? (hetero, gay, shemale): ").strip()
    if not category:
        print("❌ Debes ingresar una palabra clave.")
        return

    try:
        num_pag = int(input("👉 ¿Que pagina debo buscar?: "))
    except ValueError:
        print("❌ Error: Por favor, ingresa un número válido.")
        return

    try:
        num_videos = int(input("👉 ¿Cuántos videos aleatorios quieres descargar?: "))
    except ValueError:
        print("❌ Error: Por favor, ingresa un número válido.")
        return

    print(f"\n🔍 Buscando en el catálogo para: '{keyword}'...")
    if category = "hetero":
        url_busqueda = f"https://www.xnxx.com/search/{keyword}"
    else:
        url_busqueda = f"https://www.xnxx.com/search/{category}/{keyword}"

    try:
        # 2. Obtener la página de resultados
        response = requests.get(url_busqueda, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Error de conexión con el sitio (Código: {response.status_code})")
            return

        # 3. Extraer URLs COMPLETAS con Regex
        enlaces_encontrados = re.findall(r'/video-[a-z0-9]+/[^"\'\s>]+', response.text)
        urls_completas = list(set([f"https://www.xnxx.com{enlace}" for enlace in enlaces_encontrados]))

        if not urls_completas:
            print("⚠️ No se encontraron videos. Prueba con otro término.")
            return

        total_disponibles = len(urls_completas)
        print(f"✅ Se detectaron {total_disponibles} videos en la primera página.")
        
        # Ajustar si el usuario pide más de los que hay
        if num_videos > total_disponibles:
            print(f"ℹ️ Solo hay {total_disponibles} disponibles, descargando todos.")
            num_videos = total_disponibles

        # 4. Bucle de descarga
        descargados = 0
        while descargados < num_videos and urls_completas:
            url_final = random.choice(urls_completas)
            urls_completas.remove(url_final)
            
            print(f"\n🚀 [{descargados + 1}/{num_videos}] Preparando: {url_final}")
            
            # Comando yt-dlp
            comando = [
                'yt-dlp',
                '--user-agent', HEADERS['User-Agent'],
                '--no-check-certificate',
                '-o', f'/home/kylo/videosPorno/{keyword}/%(title)s.%(ext)s', # Organizado por carpetas
                url_final
            ]
            
            resultado = subprocess.run(comando)
            
            if resultado.returncode == 0:
                descargados += 1
                print(f"✅ Video {descargados} guardado en la carpeta 'descargas/{keyword}/'")
            else:
                print(f"❌ Error en la descarga de este video.")

            # Pausa de seguridad
            if descargados < num_videos:
                print("⏳ Pausa de 3 segundos para evitar bloqueos...")
                time.sleep(3)

        print(f"\n✨ Proceso finalizado. Total descargado: {descargados} videos.")
        enviar_notificacion(f"✨ Proceso finalizado.", f"Total descargado: {descargados} videos.")

    except Exception as e:
        print(f"💥 Error inesperado: {e}")

if __name__ == "__main__":
    iniciar_descargador()
