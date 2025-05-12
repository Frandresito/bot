import os
import json
import random
import requests
import time
from moviepy.editor import *
from google.auth.transport.requests import Request
from PIL import Image, ImageDraw, ImageFont
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from flask import Flask, request

# Configuración de APIs
PEXELS_API_KEY = "GAtP1pyOdYnrAhwfI6RLUlhwEyclik3i8Wf9VpWDD41TU564vUFYLBy0"  # Regístrate en pexels.com
YOUTUBE_CLIENT_SECRETS_FILE = "client_secret.json"  # Descarga de Google Cloud Console
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
"https://www.googleapis.com/auth/youtube.force-ssl"]

# Temas populares (puedes modificarlos según tus intereses)


def crear_guion(tema=None):
        """Crea un guión para el video usando la API de Gemini"""
        import google.generativeai as genai

        # Temas populares (puedes modificarlos según tus intereses)
        TEMAS = [
            "enigmas de la historia",
            "civilizaciones perdidas",
            "teorías conspirativas famosas",
            "eventos paranormales documentados",
            "lugares abandonados con historias oscuras",
            "experimentos científicos secretos",
            "misterios del universo",
            "casos sin resolver de la policía",
            "avistamientos de ovnis y extraterrestres",
            "viajes en el tiempo y paradojas",
            "tecnología secreta del gobierno",
            "mensajes ocultos en obras de arte",
            "personajes históricos con vidas enigmáticas",
            "fenómenos sobrenaturales",
            "desapariciones inexplicables",
            "mitos y leyendas urbanas",
            "tecnologías antiguas adelantadas a su tiempo",
            "criaturas misteriosas y criptozoología",
            "simbología oculta en religiones",
            "lugares malditos en el mundo",
            "secretos del Vaticano",
            "cultos y sociedades secretas",
            "experiencias cercanas a la muerte",
            "programas de control mental",
            "mensajes en sueños y premoniciones",
            "la simulación de la realidad",
            "artefactos arqueológicos imposibles",
            "el lado oscuro de internet (deep web)",
            "proyectos espaciales ocultos",
            "viajeros del tiempo reales",
            "curiosidades científicas",
            "tecnología del futuro",
            "avances tecnológicos",
            "innovaciones recientes",
            "descubrimientos arqueológicos inesperados",
            "secretos enterrados bajo el mar",
            "islas prohibidas",
            "experimentos médicos inhumanos del pasado",
            "el código secreto de Da Vinci",
            "teorías sobre el fin del mundo",
            "la vida después de la muerte según distintas culturas",
            "animales con comportamientos inexplicables",
            "inteligencia artificial que se salió de control",
            "robots que desarrollaron conciencia",
            "lugares donde el tiempo no fluye igual",
            "realidades paralelas",
            "muertes misteriosas de celebridades",
            "mensajes del espacio",
            "conspiraciones en la industria farmacéutica",
            "infidelidades que terminaron en tragedia",
            "hermanos enfrentados por una herencia",
            "una madre que ocultaba un gran secreto",
            "un esposo con doble vida",
            "la suegra que destruyó un matrimonio",
            "compañeros de trabajo que sabotearon un ascenso",
            "una amistad traicionada por dinero",
            "secretos familiares revelados en un funeral",
            "celos que llevaron al desastre",
            "mentiras que arruinaron una familia",
            "un jefe manipulador que arruinó varias vidas",
            "un romance secreto en la oficina",
            "un hijo ilegítimo aparece tras décadas",
            "vecinos en guerra durante años",
            "una boda interrumpida por una confesión",
            "un ex que nunca dejó de manipular",
            "amores imposibles por diferencias culturales",
            "la historia de una doble vida descubierta",
            "la esposa que contrató un detective privado",
            "el mejor amigo que resultó ser un traidor",
            "la niñera que destruyó una familia",
            "un padre ausente que regresa con un secreto",
            "una pelea entre primos que terminó en tragedia",
            "una historia de amor que escondía violencia",
            "el compañero de cuarto con intenciones oscuras",
            "una relación virtual que terminó mal",
            "una madre que fingió toda su vida",
            "el secreto detrás de una adopción",
            "la amante que se volvió peligrosa",
            "familias que se odian por generaciones",
            "la empresa que arruinó la vida de sus empleados",
            "un crimen encubierto por amor",
            "un profesor con una obsesión peligrosa",
            "una venganza planeada durante años",
            "una herencia que dividió una familia",
            "la esposa que desapareció sin dejar rastro",
            "una amistad que terminó en juicio",
            "un matrimonio perfecto con un oscuro secreto",
            "una mentira que duró toda una vida",
            "el amante que nadie sospechaba",
            "una pareja rota por una red social",
            "el reencuentro con el amor del pasado",
            "una cita que terminó en pesadilla",
            "un influencer que ocultaba su verdadera identidad",
            "la boda con un final inesperado",
            "una relación basada en una mentira",
            "la historia de una estafa emocional",
            "el diario que reveló la verdad",
            "una pareja destruida por los celos",
            "un hermano que traicionó por envidia",
            "un caso de acoso laboral encubierto",
            "una familia que fingía una vida perfecta"
        ]


        if not tema:
            tema = random.choice(TEMAS)

        print(f"Generando guion sobre: {tema}")

        # Configurar API de Gemini - Necesitas obtener tu API key en https://makersuite.google.com/
        GEMINI_API_KEY = "AIzaSyAy3nsin-Exvdgq71zxX2OjGPW2gHpo7a8"  # Sustituye con tu clave API real
        genai.configure(api_key=GEMINI_API_KEY)

        # Crear un modelo de generación
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        # Usar el modelo Gemini-1.0-Pro
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config
        )

        # Crear el prompt para Gemini
        prompt = f"""
        Genera un guion para un video en español sobre {tema}.
        El guion debe ser para un video de 3 minutos.
        El guion debe incluir:

        1. Un título atractivo
        2. Una introducción que enganche al espectador (2-3 frases)
        3. El desarrollo jugoso del tema
        4. Una frase recordando al espectador dar like y suscribirse
        5. Una conclusión (2-3 frases)

        También genera una descripción para YouTube (3-5 líneas) y 5-10 palabras clave relacionadas para buscar imágenes.

        FORMATO DE RESPUESTA (respeta este formato exacto):
        {{
            "titulo": "El título aquí",
            "guion": "El guion completo aquí, con varios párrafos NO DES DESCRIPCCIONES DE LAS IMAGENES NI DE MUSICA, EN ESTE ESPACIO VA SOLO LO QUE DEBO LEER",
            "descripcion": "La descripción para YouTube aquí",
            "palabras_clave": ["palabra1", "palabra2", "etc"]
        }}
        """

        try:
            # Generar el contenido con Gemini
            response = model.generate_content(prompt)

            # Intentar extraer el JSON de la respuesta
            respuesta_texto = response.text

            # Buscar contenido JSON en la respuesta
            import json
            import re

            # Intentar encontrar contenido JSON en la respuesta
            json_match = re.search(r'\{[\s\S]*\}', respuesta_texto)

            if json_match:
                try:
                    resultado = json.loads(json_match.group(0))

                    # Verificar que todos los campos necesarios estén presentes
                    campos_requeridos = ["titulo", "guion", "descripcion", "palabras_clave"]
                    for campo in campos_requeridos:
                        if campo not in resultado:
                            raise KeyError(f"Falta el campo '{campo}' en la respuesta")

                    return resultado
                except json.JSONDecodeError as e:
                    print(f"Error al parsear JSON: {e}")
            else:
                print("No se encontró formato JSON en la respuesta")

            # Si llegamos aquí, hubo un problema con el formato. Intentamos extraer manualmente
            print("Intentando extraer contenido manualmente...")

            # Buscar título
            titulo_match = re.search(r'"titulo":\s*"([^"]+)"', respuesta_texto)
            titulo = titulo_match.group(1) if titulo_match else f"10 datos fascinantes sobre {tema}"

            # Buscar guion
            guion_match = re.search(r'"guion":\s*"([^"]*)"', respuesta_texto, re.DOTALL)
            guion = guion_match.group(1) if guion_match else respuesta_texto

            # Buscar descripción
            descripcion_match = re.search(r'"descripcion":\s*"([^"]*)"', respuesta_texto, re.DOTALL)
            descripcion = descripcion_match.group(1) if descripcion_match else f"Video sobre {tema}"

            # Para palabras clave
            palabras_clave = [tema] + tema.split()
            if len(palabras_clave) < 5:
                palabras_clave += ["educación", "aprendizaje", "conocimiento", "ciencia", "descubrimiento"]

            palabras_clave = palabras_clave[:10]  # Limitar a 10 palabras clave

            return {
                "titulo": titulo,
                "guion": guion,
                "descripcion": descripcion,
                "palabras_clave": palabras_clave
            }

        except Exception as e:
            print(f"Error al generar contenido con Gemini: {e}")

            # Respuesta de emergencia por si falla la API
            titulo = f"10 datos fascinantes sobre {tema} que no conocías"

            guion = f"""Hola a todos, bienvenidos a un nuevo video. Hoy hablaremos sobre {tema}, un tema fascinante que seguro te sorprenderá.

    Primero, es importante destacar que {tema} ha evolucionado mucho en los últimos años. Los expertos sugieren que cada vez hay más interés en este campo.

    Un dato interesante es que {tema} tiene conexiones con otros campos que quizás no esperabas.

    ¿Sabías que muchas personas desconocen la verdadera importancia de {tema} en nuestra vida diaria?

    Los estudios han demostrado que {tema} puede tener un impacto significativo en cómo vemos el mundo.

    Un aspecto poco conocido de {tema} es su influencia en el desarrollo de nuevas tecnologías.

    Investigadores de universidades prestigiosas han dedicado años al estudio de {tema}, descubriendo patrones sorprendentes.

    Si estás disfrutando de este contenido, no olvides dar like y suscribirte a nuestro canal.

    Para concluir, {tema} es un campo en constante evolución que seguirá sorprendiéndonos. Si te ha gustado este contenido, no olvides dar like y suscribirte para más videos como este.
    """

            descripcion = f"""
    {titulo}

    En este video exploramos los aspectos más interesantes sobre {tema}.

    ¡No olvides suscribirte y dar like si te ha gustado!

    #datos #curiosidades #{tema.replace(' ', '')} #educacion #aprendizaje
    """

            palabras_clave = [tema] + tema.split()
            if len(palabras_clave) < 5:
                palabras_clave += ["educación", "aprendizaje", "conocimiento", "ciencia", "descubrimiento"]

            palabras_clave = palabras_clave[:10]  # Limitar a 10 palabras clave

            return {
                "titulo": titulo,
                "guion": guion,
                "descripcion": descripcion,
                "palabras_clave": palabras_clave
            }

def texto_a_audio(texto, nombre_archivo="audio.mp3"):
            """Convierte texto a audio usando exclusivamente ElevenLabs con voz en español"""
            import requests
            import time

            try:
                # Configuración de ElevenLabs
                ELEVENLABS_API_KEY = "sk_0a1dc8a370bd7e4b5e2fa71f2f2ec8aa297701500184bb31"  # Tu API key

                # Voice ID para voz en español (Antonio)
                VOICE_ID = "ErXwobaYiN019PkySvjV"  # Antonio (voz masculina en español)

                print("Generando audio con ElevenLabs...")

                url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": ELEVENLABS_API_KEY
                }

                # Configuración optimizada para voz en español
                data = {
                    "text": texto,
                    "model_id": "eleven_multilingual_v2",  # Mejor modelo para español
                    "voice_settings": {
                        "stability": 0.6,        # Aumentado para mayor consistencia
                        "similarity_boost": 0.7, # Aumentado para mejor calidad
                        "style": 0.5,            # Estilo balanceado
                        "use_speaker_boost": True # Mejora la calidad del altavoz
                    }
                }

                # Intenta la solicitud hasta 3 veces en caso de fallos
                max_intentos = 3
                for intento in range(1, max_intentos + 1):
                    try:
                        response = requests.post(url, json=data, headers=headers)

                        if response.status_code == 200:
                            with open(nombre_archivo, 'wb') as f:
                                f.write(response.content)
                            print(f"Audio generado exitosamente y guardado como {nombre_archivo}")
                            return nombre_archivo
                        elif response.status_code == 429:  # Rate limit
                            wait_time = 10 if intento == 1 else 20
                            print(f"Límite de velocidad alcanzado. Esperando {wait_time} segundos...")
                            time.sleep(wait_time)
                            continue
                        else:
                            # Imprimir detalles del error
                            print(f"Error en ElevenLabs (Intento {intento}/{max_intentos}):")
                            print(f"Estado: {response.status_code}")
                            try:
                                error_detail = response.json()
                                print(f"Detalle: {error_detail}")
                            except:
                                print(f"Respuesta: {response.text[:200]}...")

                            if intento < max_intentos:
                                wait_time = 5 * intento
                                print(f"Reintentando en {wait_time} segundos...")
                                time.sleep(wait_time)
                            else:
                                print("Todos los intentos fallidos.")
                                return None
                    except requests.exceptions.RequestException as req_err:
                        print(f"Error de conexión (Intento {intento}/{max_intentos}): {req_err}")
                        if intento < max_intentos:
                            time.sleep(5)
                        else:
                            print("Error persistente de conexión.")
                            return None

                print("No se pudo generar el audio después de múltiples intentos.")
                return None

            except Exception as e:
                print(f"Error inesperado al convertir texto a audio: {e}")
                import traceback
                traceback.print_exc()
                return None

def generar_subtitulos(guion, audio_path, nombre_archivo="subtitulos.srt"):
    """
    Genera subtítulos sincronizados para el video basado en el guión
    y el audio generado.

    Args:
        guion (str): El texto del guión del video
        audio_path (str): Ruta al archivo de audio generado
        nombre_archivo (str): Nombre del archivo de subtítulos (predeterminado: "subtitulos.srt")

    Returns:
        str: Ruta al archivo de subtítulos generado o None si ocurre un error
    """
    try:
        import os
        import re
        from pydub import AudioSegment

        print("Generando subtítulos basados en el guión...")

        # Verificar que el archivo de audio exista
        if not os.path.exists(audio_path):
            print(f"Error: El archivo de audio no existe en {audio_path}")
            return None

        # Cargar el audio para obtener su duración
        audio = AudioSegment.from_file(audio_path)
        duracion_total_ms = len(audio)
        duracion_total_seg = duracion_total_ms / 1000

        print(f"Duración del audio: {duracion_total_seg:.2f} segundos")

        # Preparar el texto: separar en oraciones o párrafos
        # Primero, normalizar saltos de línea
        texto_normalizado = guion.replace('\r\n', '\n').replace('\r', '\n')

        # Dividir el texto en párrafos significativos
        parrafos = []
        parrafo_actual = ""

        for linea in texto_normalizado.split('\n'):
            linea = linea.strip()
            if not linea:  # Línea vacía indica cambio de párrafo
                if parrafo_actual:
                    parrafos.append(parrafo_actual)
                    parrafo_actual = ""
            else:
                if parrafo_actual:
                    parrafo_actual += " " + linea
                else:
                    parrafo_actual = linea

        # Añadir el último párrafo si existe
        if parrafo_actual:
            parrafos.append(parrafo_actual)

        # Si no hay suficientes párrafos, dividir en oraciones
        if len(parrafos) < 100:
            # Patrón para dividir en oraciones
            patron_oraciones = re.compile(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])')
            oraciones = []

            for parrafo in parrafos:
                # Dividir el párrafo en oraciones
                for oracion in re.split(patron_oraciones, parrafo):
                    if oracion.strip():
                        oraciones.append(oracion.strip())

            segmentos = oraciones
        else:
            segmentos = parrafos

        # Si hay muy pocas oraciones, dividir por puntos
        if len(segmentos) < 5:
            nuevos_segmentos = []
            for segmento in segmentos:
                partes = segmento.split('.')
                for parte in partes:
                    if parte.strip():
                        nuevos_segmentos.append(parte.strip() + '.')
            segmentos = nuevos_segmentos

        # Calcular la duración aproximada de cada segmento
        # Asumimos una distribución uniforme del tiempo para cada segmento
        duracion_por_segmento = duracion_total_seg / len(segmentos)

        print(f"Generando {len(segmentos)} segmentos de subtítulos...")

        # Función para convertir segundos a formato SRT (HH:MM:SS,mmm)
        def formato_tiempo_srt(segundos):
            horas = int(segundos / 3600)
            minutos = int((segundos % 3600) / 60)
            segundos_restantes = int(segundos % 60)
            milisegundos = int((segundos - int(segundos)) * 1000)
            return f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d},{milisegundos:03d}"

        # Generar el archivo SRT
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            tiempo_actual = 0

            for i, segmento in enumerate(segmentos, 1):
                # Calcular tiempos de inicio y fin
                tiempo_inicio = tiempo_actual

                # Ajustar la duración según la longitud del texto
                # (aproximadamente 15 caracteres por segundo)
                caracteres = len(segmento)
                duracion_estimada = max(1.5, min(caracteres / 15, duracion_por_segmento * 1.5))

                # Asegurarse de que no exceda la duración total
                tiempo_fin = min(tiempo_actual + duracion_estimada, duracion_total_seg)

                # Para los segmentos más largos, dividirlos en líneas más cortas
                if len(segmento) > 42:  # Máximo recomendado de caracteres por línea
                    palabras = segmento.split()
                    mitad = len(palabras) // 2
                    primera_linea = ' '.join(palabras[:mitad])
                    segunda_linea = ' '.join(palabras[mitad:])
                    texto_subtitulo = f"{primera_linea}\n{segunda_linea}"
                else:
                    texto_subtitulo = segmento

                # Escribir subtítulo en formato SRT
                f.write(f"{i}\n")
                f.write(f"{formato_tiempo_srt(tiempo_inicio)} --> {formato_tiempo_srt(tiempo_fin)}\n")
                f.write(f"{texto_subtitulo}\n\n")

                tiempo_actual = tiempo_fin

        print(f"Subtítulos generados exitosamente en '{nombre_archivo}'")

        # Devolver la ruta al archivo de subtítulos
        return nombre_archivo

    except Exception as e:
        print(f"Error al generar subtítulos: {e}")
        import traceback
        traceback.print_exc()
        return None

#Added start

def buscar_musica_fondo(tema=None):
    """
    Busca y descarga música de fondo libre de derechos desde una fuente gratuita

    Args:
        tema (str, opcional): Tipo de música a buscar (energética, relajada, etc.)

    Returns:
        str: Ruta al archivo de música descargado o None si hubo un error
    """
    try:
        import os
        import random
        import requests

        print("Buscando música de fondo...")

        # Lista de URLs de música libre de derechos de FreeSound o similar
        # En una implementación real, deberías usar una API como FreeSound o similar
        MUSICAS_LIBRES = [
            "https://cdn.pixabay.com/download/audio/2022/03/10/audio_45d7c86310.mp3",  # Inspiradora
            "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0c6ffed6e.mp3",  # Tecnología
            "https://cdn.pixabay.com/download/audio/2022/08/02/audio_884fe5f776.mp3",  # Científica
            "https://cdn.pixabay.com/download/audio/2021/11/25/audio_d255ea7a42.mp3",  # Relajada
            "https://cdn.pixabay.com/download/audio/2021/07/24/audio_c668b3fb42.mp3"   # Curiosidades
        ]

        # Seleccionar una música según el tema o al azar si no se especifica
        if tema:
            tema = tema.lower()
            if "tecno" in tema or "futuro" in tema:
                musica_url = MUSICAS_LIBRES[1]
            elif "ciencia" in tema or "científic" in tema:
                musica_url = MUSICAS_LIBRES[2]
            elif "relaj" in tema or "salud" in tema:
                musica_url = MUSICAS_LIBRES[3]
            elif "curios" in tema or "dato" in tema:
                musica_url = MUSICAS_LIBRES[4]
            else:
                musica_url = MUSICAS_LIBRES[0]
        else:
            musica_url = random.choice(MUSICAS_LIBRES)

        # Descargar el archivo de música
        musica_path = "musica_fondo.mp3"
        response = requests.get(musica_url)

        if response.status_code == 200:
            with open(musica_path, "wb") as f:
                f.write(response.content)
            print(f"Música de fondo descargada correctamente: {musica_path}")
            return musica_path
        else:
            print(f"Error al descargar música: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error al buscar música de fondo: {e}")
        import traceback
        traceback.print_exc()
        return None

def subir_subtitulos_youtube(youtube, video_id, subtitulos_path, lenguaje="es"):
    """
    Sube subtítulos a un video de YouTube

    Args:
        youtube: Instancia autenticada de la API de YouTube
        video_id (str): ID del video de YouTube
        subtitulos_path (str): Ruta al archivo de subtítulos
        lenguaje (str): Código de lenguaje (defecto: "es" para español)

    Returns:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    try:
        import os
        from googleapiclient.http import MediaFileUpload

        if not os.path.exists(subtitulos_path):
            print(f"Error: El archivo de subtítulos no existe en {subtitulos_path}")
            return False

        # Leer el contenido del archivo de subtítulos para depuración
        with open(subtitulos_path, 'r', encoding='utf-8') as f:
            subtitulos_content = f.read()

        print(f"Subiendo subtítulos para el video ID: {video_id}")
        print(f"Tamaño del archivo de subtítulos: {os.path.getsize(subtitulos_path)} bytes")

        # Verificar el formato del ID del video
        if not video_id or len(video_id) != 11:
            print(f"Error: ID de video inválido: {video_id}")
            return False

        # Crear un objeto MediaFileUpload con el tipo MIME correcto
        media = MediaFileUpload(
            subtitulos_path,
            mimetype="application/vnd.ttml+xml",
            resumable=True
        )

        # Subir los subtítulos con manejo de errores mejorado
        try:
            request = youtube.captions().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": video_id,
                        "language": lenguaje,
                        "name": "Subtítulos en español oficiales.",
                        "isDraft": False
                    }
                },
                media_body=media
            )

            # Intentar la ejecución con manejo de errores detallado
            response = request.execute()
            print(f"Subtítulos subidos correctamente. Caption ID: {response.get('id')}")
            return True

        except googleapiclient.errors.HttpError as error:
            error_content = error.content.decode() if hasattr(error, 'content') else str(error)
            print(f"Error HTTP detallado: {error_content}")

            # Si el error es por permisos insuficientes
            if "insufficientPermissions" in error_content or "permission" in error_content.lower():
                print("Error de permisos: Asegúrate de que la aplicación tenga permisos para gestionar subtítulos.")
                print("Debes activar la API YouTube Caption en la consola de Google Cloud.")

            # Si el error es por formato
            elif "invalid" in error_content.lower() and "format" in error_content.lower():
                print("Error de formato: El archivo de subtítulos no está en un formato compatible.")
                # Intentar convertir y subir como SRT
                return subir_subtitulos_alternativo(youtube, video_id, subtitulos_path, lenguaje)

            return False

    except Exception as e:
        print(f"Error al subir subtítulos a YouTube: {e}")
        import traceback
        traceback.print_exc()
        return False


def subir_subtitulos_alternativo(youtube, video_id, subtitulos_path, lenguaje="es"):
    """
    Método alternativo para subir subtítulos
    """
    try:
        import os
        from googleapiclient.http import MediaFileUpload

        print("Intentando método alternativo para subir subtítulos...")

        # Leer el contenido del archivo SRT
        with open(subtitulos_path, 'r', encoding='utf-8') as f:
            subtitulos_content = f.read()

        # Crear archivo SRT temporal con BOM UTF-8 para mayor compatibilidad
        temp_srt_path = "temp_subtitles.srt"
        with open(temp_srt_path, 'w', encoding='utf-8-sig') as f:
            f.write(subtitulos_content)

        media = MediaFileUpload(
            temp_srt_path,
            mimetype="application/x-subrip",
            resumable=True
        )

        request = youtube.captions().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "language": lenguaje,
                    "name": "Subtítulos en español",
                    "isDraft": False
                }
            },
            media_body=media
        )

        response = request.execute()
        print(f"Subtítulos subidos correctamente con método alternativo. Caption ID: {response.get('id')}")

        # Eliminar archivo temporal
        if os.path.exists(temp_srt_path):
            os.remove(temp_srt_path)

        return True

    except Exception as e:
        print(f"Error en método alternativo para subir subtítulos: {e}")
        import traceback
        traceback.print_exc()
        return False
#added end

def buscar_imagenes(palabras_clave):
    """Busca imágenes en Pexels basado en palabras clave"""
    imagenes = []

    try:
        for palabra in palabras_clave:
            print(f"Buscando imágenes para: {palabra}")
            url = f"https://api.pexels.com/v1/search?query={palabra}&per_page=3"
            headers = {"Authorization": PEXELS_API_KEY}

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"Error al buscar imágenes para '{palabra}': {response.status_code}")
                continue

            data = response.json()

            if "photos" in data and data["photos"]:
                for photo in data["photos"]:
                    imagenes.append({
                        "url": photo["src"]["large"],
                        "palabra_clave": palabra
                    })
            else:
                print(f"No se encontraron imágenes para '{palabra}'")

        # Si no tenemos suficientes imágenes, busquemos algunas genéricas
        if len(imagenes) < 10:
            extra_keywords = ["background", "abstract", "nature", "technology"]
            for palabra in extra_keywords:
                url = f"https://api.pexels.com/v1/search?query={palabra}&per_page=2"
                headers = {"Authorization": PEXELS_API_KEY}

                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    continue

                data = response.json()

                if "photos" in data:
                    for photo in data["photos"]:
                        imagenes.append({
                            "url": photo["src"]["large"],
                            "palabra_clave": palabra
                        })

        # Descargar las imágenes
        print(f"Descargando {len(imagenes)} imágenes...")
        for i, img in enumerate(imagenes):
            try:
                img_response = requests.get(img["url"])
                if img_response.status_code == 200:
                    img_filename = f"img_{i}.jpg"
                    with open(img_filename, "wb") as file:
                        file.write(img_response.content)
                    img["archivo"] = img_filename
                else:
                    print(f"Error al descargar imagen {i}: {img_response.status_code}")
            except Exception as e:
                print(f"Error al procesar imagen {i}: {e}")

        # Filtrar imágenes que se descargaron correctamente
        imagenes = [img for img in imagenes if "archivo" in img]
        return imagenes

    except Exception as e:
        print(f"Error al buscar imágenes: {e}")
        return []

def crear_miniatura(titulo, imagen_fondo=None):
    """Crea una miniatura para el video"""
    try:
        # Si no tenemos imagen de fondo, crear una con colores llamativos
        if not imagen_fondo:
            width, height = 1280, 720
            img = Image.new('RGB', (width, height), color=(33, 150, 243))

            # Agregar gradiente
            draw = ImageDraw.Draw(img)
            for i in range(height):
                r = int(33 + (210 - 33) * i / height)
                g = int(150 + (59 - 150) * i / height)
                b = int(243 + (112 - 243) * i / height)
                draw.line([(0, i), (width, i)], fill=(r, g, b))
        else:
            img = Image.open(imagen_fondo)
            img = img.resize((1280, 720))

        # Agregar texto
        draw = ImageDraw.Draw(img)

        # Dividir el título en líneas de máximo 30 caracteres
        palabras = titulo.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            if len(linea_actual + " " + palabra) <= 30:
                linea_actual += " " + palabra if linea_actual else palabra
            else:
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        # Intentar cargar una fuente, o usar la fuente por defecto
        try:
            # Buscar fuentes disponibles en el sistema
            font_path = None
            common_fonts = [
                "DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "C:\\Windows\\Fonts\\Arial.ttf"
            ]

            for f in common_fonts:
                if os.path.exists(f):
                    font_path = f
                    break

            if font_path:
                font = ImageFont.truetype(font_path, 60)
            else:
                # Si no encontramos fuentes, usar la por defecto
                font = ImageFont.load_default()
        except Exception as font_error:
            print(f"Error al cargar fuente: {font_error}")
            # Usar fuente por defecto
            font = ImageFont.load_default()

        # Dibujar sombra para el texto
        y_pos = 200
        for linea in lineas:
            # Calcular ancho del texto (compatibilidad con diferentes versiones de PIL)
            try:
                text_width = draw.textlength(linea, font=font)
            except AttributeError:
                # Para versiones anteriores de PIL
                text_width, _ = draw.textsize(linea, font=font)

            position = ((1280 - text_width) // 2, y_pos)

            # Sombra
            draw.text((position[0] + 3, position[1] + 3), linea, font=font, fill=(0, 0, 0))
            # Texto principal
            draw.text(position, linea, font=font, fill=(255, 255, 255))
            y_pos += 70

        thumbnail_path = "miniatura.jpg"
        img.save(thumbnail_path)
        return thumbnail_path

    except Exception as e:
        print(f"Error al crear miniatura: {e}")
        # Crear una miniatura básica de emergencia
        width, height = 1280, 720
        img = Image.new('RGB', (width, height), color=(33, 150, 243))
        img.save("miniatura.jpg")
        return "miniatura.jpg"

def procesar_archivo_srt(srt_path):
    """
    Procesa un archivo SRT y devuelve una lista de subtítulos con sus tiempos.

    Args:
        srt_path (str): Ruta al archivo SRT de subtítulos

    Returns:
        list: Lista de diccionarios con tiempos de inicio, fin y texto
    """
    try:
        with open(srt_path, 'r', encoding='utf-8') as file:
            contenido = file.read()

        # Dividir el archivo por bloques de subtítulos
        bloques = contenido.strip().split('\n\n')
        subtitulos = []

        for bloque in bloques:
            lineas = bloque.split('\n')
            if len(lineas) < 3:
                continue

            # Extraer tiempos
            tiempos = lineas[1].split(' --> ')
            tiempo_inicio = convertir_tiempo_srt_a_segundos(tiempos[0])
            tiempo_fin = convertir_tiempo_srt_a_segundos(tiempos[1])

            # Extraer texto (puede haber más de una línea)
            texto = '\n'.join(lineas[2:])

            subtitulos.append({
                'inicio': tiempo_inicio,
                'fin': tiempo_fin,
                'texto': texto
            })

        return subtitulos
    except Exception as e:
        print(f"Error al procesar archivo SRT: {e}")
        return []

def convertir_tiempo_srt_a_segundos(tiempo_str):
    """
    Convierte el formato de tiempo SRT (HH:MM:SS,mmm) a segundos

    Args:
        tiempo_str (str): Tiempo en formato SRT

    Returns:
        float: Tiempo en segundos
    """
    partes = tiempo_str.replace(',', '.').split(':')
    horas = int(partes[0])
    minutos = int(partes[1])
    segundos = float(partes[2])

    return horas * 3600 + minutos * 60 + segundos

def crear_video_con_subtitulos(guion_info, audio_path, imagenes, subtitulos_path, musica_path=None):
    """
    Crea un video combinando audio, imágenes, música de fondo y subtítulos integrados

    Args:
        guion_info (dict): Información del guión
        audio_path (str): Ruta al archivo de audio
        imagenes (list): Lista de imágenes para el video
        subtitulos_path (str): Ruta al archivo SRT de subtítulos
        musica_path (str, opcional): Ruta al archivo de música de fondo

    Returns:
        str: Ruta al video final o None si hubo un error
    """
    try:
        if not os.path.exists(audio_path):
            print(f"Error: El archivo de audio no existe en {audio_path}")
            return None

        if not os.path.exists(subtitulos_path):
            print(f"Error: El archivo de subtítulos no existe en {subtitulos_path}")
            return None

        # Cargar el audio principal (voz)
        audio_clip = AudioFileClip(audio_path)
        duracion_total = audio_clip.duration

        # Cargar y procesar la música de fondo si existe
        if musica_path and os.path.exists(musica_path):
            try:
                print("Añadiendo música de fondo...")
                musica_clip = AudioFileClip(musica_path)

                # Repetir la música si es más corta que el audio principal
                if musica_clip.duration < duracion_total:
                    print("La música es más corta que el audio principal, extendiéndola...")
                    repeticiones = int(duracion_total / musica_clip.duration) + 1
                    musica_extendida = concatenate_audioclips([musica_clip] * repeticiones)
                    musica_clip = musica_extendida.subclip(0, duracion_total)
                else:
                    # Recortar la música si es más larga
                    musica_clip = musica_clip.subclip(0, duracion_total)

                # Bajar el volumen de la música (0.2 = 20% del volumen original)
                musica_clip = musica_clip.volumex(0.2)

                # Mezclar el audio principal con la música de fondo
                audio_final = CompositeAudioClip([audio_clip, musica_clip])
            except Exception as e:
                print(f"Error al procesar música de fondo: {e}")
                audio_final = audio_clip
        else:
            audio_final = audio_clip

        # Procesar el archivo SRT para obtener los subtítulos
        subtitulos = procesar_archivo_srt(subtitulos_path)
        if not subtitulos:
            print("No se pudieron cargar los subtítulos. Continuando sin ellos.")

        # Verificar si tenemos imágenes
        if not imagenes:
            print("No hay imágenes disponibles para el video, creando fondo genérico...")
            # Crear una imagen genérica
            width, height = 1280, 720
            img = Image.new('RGB', (width, height), color=(33, 150, 243))
            img_path = "fondo_generico.jpg"
            img.save(img_path)
            imagenes = [{"archivo": img_path, "palabra_clave": "fondo"}]

        # Calcular duración para cada imagen
        duracion_por_imagen = duracion_total / len(imagenes)
        print(f"Creando video de {duracion_total:.2f} segundos con {len(imagenes)} imágenes")

        # Crear los clips de video para cada imagen
        video_clips = []
        for i, img in enumerate(imagenes):
            inicio = i * duracion_por_imagen
            fin = (i + 1) * duracion_por_imagen

            if i == len(imagenes) - 1:
                # Asegurar que la última imagen cubra hasta el final
                fin = duracion_total

            try:
                if not os.path.exists(img["archivo"]):
                    print(f"Error: Archivo de imagen no encontrado: {img['archivo']}")
                    continue

                img_clip = ImageClip(img["archivo"]).set_duration(fin - inicio)

                # Hacer que la imagen llene la pantalla manteniendo proporción
                img_clip = img_clip.resize(height=720)
                img_clip = img_clip.resize(width=1280) if img_clip.w < 1280 else img_clip

                # Centrar la imagen
                img_clip = img_clip.set_position(("center", "center"))

                # Recortar a 1280x720 si es más grande
                if img_clip.w > 1280 or img_clip.h > 720:
                    img_clip = img_clip.crop(x_center=img_clip.w/2, y_center=img_clip.h/2,
                                           width=1280, height=720)

                video_clips.append(img_clip.set_start(inicio))
            except Exception as img_error:
                print(f"Error al procesar imagen {i}: {img_error}")

        if not video_clips:
            print("No se pudo crear ningún clip de video válido")
            return None

        # Crear el video base
        video = CompositeVideoClip(video_clips, size=(1280, 720))
        video = video.set_audio(audio_final)  # Usar el audio con música de fondo
        video = video.set_duration(duracion_total)

        # Función para generar los clips de subtítulos
        def crear_clips_subtitulos(subtitulos_lista):
            clips_subtitulos = []

            for sub in subtitulos_lista:
                # Crear un TextClip para cada subtítulo
                txt_clip = TextClip(
                    sub['texto'],
                    fontsize=36,
                    color='white',
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=2,
                    method='label',
                    align='center',
                    size=(1200, None)  # Ancho máximo y altura automática
                )

                # Posicionar el subtítulo en la parte inferior del video
                txt_clip = txt_clip.set_position(('center', 620))

                # Establecer duración y tiempos
                txt_clip = txt_clip.set_start(sub['inicio']).set_duration(sub['fin'] - sub['inicio'])

                clips_subtitulos.append(txt_clip)

            return clips_subtitulos

        # Añadir los subtítulos al video si existen
        if subtitulos:
            print(f"Añadiendo {len(subtitulos)} subtítulos al video...")
            clips_subtitulos = crear_clips_subtitulos(subtitulos)
            video_con_subs = CompositeVideoClip([video] + clips_subtitulos)
            video_final = video_con_subs
        else:
            video_final = video

        # Renderizar el video final
        video_path = "video_final.mp4"
        print(f"Generando archivo de video final con subtítulos y música: {video_path}")
        video_final.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')

        return video_path

    except Exception as e:
        print(f"Error al crear el video con subtítulos: {e}")
        import traceback
        traceback.print_exc()
        return None

def autenticar_youtube():
    """Sistema mejorado de autenticación para YouTube"""
    try:
        print("Iniciando el proceso de autenticación de YouTube...")

        # Verificar archivo de credenciales
        if not os.path.exists(YOUTUBE_CLIENT_SECRETS_FILE):
            print(f"Error: Archivo de credenciales no encontrado: {YOUTUBE_CLIENT_SECRETS_FILE}")
            return None

        # Cargar información del cliente OAuth desde el archivo JSON
        with open(YOUTUBE_CLIENT_SECRETS_FILE, 'r') as f:
            client_config = json.load(f)

        # Verificar si hay token guardado y si es válido
        creds = None
        if os.path.exists("youtube_token.json"):
            try:
                with open("youtube_token.json", 'r') as token:
                    creds = Credentials.from_authorized_user_info(json.load(token), YOUTUBE_SCOPES)

                # Si las credenciales existen pero expiraron y tienen refresh token
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open("youtube_token.json", 'w') as token:
                        token.write(creds.to_json())
                    print("Credenciales actualizadas correctamente")
                    return build_youtube_client(creds)
            except Exception as e:
                print(f"Error con credenciales existentes: {e}")
                creds = None

        # Si no hay credenciales válidas, iniciar el flujo de autorización
        if not creds or not creds.valid:
            # Configurar Flask para manejar la redirección
            app = Flask(__name__)
            auth_response = {"code": None}

            @app.route('/')
            def index():
                return "Servicio de autenticación de YouTube activo. Espera la redirección desde Google."

            @app.route('/oauth2callback')
            def oauth2callback():
                code = request.args.get('code')
                if code:
                    auth_response["code"] = code
                    return "<h1>Autorización exitosa</h1><p>Ya puedes cerrar esta ventana y volver a tu aplicación.</p>"
                return "<h1>Error de autorización</h1><p>No se recibió el código.</p>"

            # Ejecutar servidor en un hilo separado
            from threading import Thread
            server = Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=False))
            server.daemon = True
            server.start()

            # Crear flujo de OAuth
            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_config,
                scopes=YOUTUBE_SCOPES
            )

            # Establecer URI de redirección CORRECTAMENTE - IMPORTANTE:
            # Esta debe coincidir EXACTAMENTE con una URI autorizada en la consola de Google Cloud
            # Para aplicaciones de escritorio/pruebas locales, usa http://localhost:8080/oauth2callback
            flow.redirect_uri = "http://localhost:8080/oauth2callback"

            # Generar URL de autorización
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )

            print("\n===== INSTRUCCIONES DE AUTENTICACIÓN =====")
            print(f"1. Abre esta URL en tu navegador: {auth_url}")
            print("2. Inicia sesión con tu cuenta de Google y autoriza la aplicación")
            print("3. Espera a ser redirigido automáticamente\n")

            # Esperar a que se reciba el código de autorización
            timeout = 300  # 5 minutos para autenticar
            start_time = time.time()

            while not auth_response["code"] and time.time() - start_time < timeout:
                time.sleep(1)

            if not auth_response["code"]:
                print("Tiempo de espera agotado. No se recibió respuesta de autenticación.")
                return None

            # Intercambiar el código por credenciales
            flow.fetch_token(code=auth_response["code"])
            creds = flow.credentials

            # Guardar credenciales para futuras ejecuciones
            with open("youtube_token.json", 'w') as token:
                token.write(creds.to_json())
                print("Credenciales guardadas correctamente")

        return build_youtube_client(creds)

    except Exception as e:
        print(f"Error en la autenticación: {e}")
        import traceback
        traceback.print_exc()
        return None

def build_youtube_client(credentials):
    """Crea un cliente de la API de YouTube"""
    try:
        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    except Exception as e:
        print(f"Error al crear cliente de YouTube: {e}")
        return None

def subir_video_youtube(youtube, video_path, titulo, descripcion, tags, miniatura_path):
    """Sube el video a YouTube"""
    try:
        # Verificar que los archivos existan
        if not os.path.exists(video_path):
            print(f"Error: El archivo de video no existe: {video_path}")
            return None

        if not os.path.exists(miniatura_path):
            print(f"Error: La miniatura no existe: {miniatura_path}")
            miniatura_path = None  # YouTube usará un frame del video como miniatura

        # Definir metadata del video
        request_body = {
            "snippet": {
                "title": titulo,
                "description": descripcion,
                "tags": tags,
                "categoryId": "27"  # Categoría "Educación"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        # Iniciar la subida
        media_file = MediaFileUpload(video_path)

        print("Subiendo video a YouTube...")
        response_upload = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        ).execute()

        video_id = response_upload.get("id")

        # Subir miniatura
        if video_id and miniatura_path:
            print("Subiendo miniatura...")
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(miniatura_path)
            ).execute()

            print(f"Video subido correctamente: https://www.youtube.com/watch?v={video_id}")
            return video_id
        else:
            print("No se pudo obtener el ID del video subido.")
            return None

    except Exception as e:
        print(f"Error al subir el video a YouTube: {e}")
        return None

def main():
    """Función principal que ejecuta todo el proceso"""
    print("🚀 Iniciando la creación de un nuevo video para YouTube")

    # 1. Crear guion
    print("1️⃣ Creando guion...")
    guion_info = crear_guion()
    print(f"Título generado: {guion_info['titulo']}")

    # 2. Convertir guion a audio
    print("2️⃣ Convirtiendo guion a audio...")
    audio_path = texto_a_audio(guion_info["guion"])
    # audio_path = os.path.join(os.path.dirname(__file__), "audio.mp3")

    if not audio_path:
        print("❌ Error al generar el audio. Proceso terminado.")
        return

    # 3. Generar subtítulos
    print("3️⃣ Generando subtítulos...")
    subtitulos_path = generar_subtitulos(guion_info["guion"], audio_path)

    if not subtitulos_path:
        print("❌ Error al generar los subtítulos. Proceso terminado.")
        return

    # 4. Buscar imágenes relacionadas
    print("4️⃣ Buscando imágenes relacionadas...")
    imagenes = buscar_imagenes(guion_info["palabras_clave"])
    print(f"Se encontraron {len(imagenes)} imágenes.")

    # 5. Buscar música de fondo relacionada con el tema
    print("5️⃣ Buscando música de fondo...")
    # Extraer el tema principal para seleccionar la música adecuada
    tema_principal = guion_info["titulo"].split()[0] if guion_info["titulo"] else ""
    musica_path = buscar_musica_fondo(tema_principal)

    # 6. Crear miniatura
    print("6️⃣ Creando miniatura...")
    miniatura_path = crear_miniatura(guion_info["titulo"],
                                   imagenes[0]["archivo"] if imagenes else None)

    # 7. Crear video con subtítulos integrados y música de fondo
    print("7️⃣ Generando video con subtítulos y música...")
    video_path = crear_video_con_subtitulos(guion_info, audio_path, imagenes, subtitulos_path, musica_path)
    # video_path = os.path.join(os.path.dirname(__file__), "video_final.mp4")

    if not video_path:
        print("❌ Error al crear el video. Proceso terminado.")
        return

    # 8. Subir a YouTube
    print("8️⃣ Preparando para subir a YouTube...")
    youtube = autenticar_youtube()

    if youtube:
        print("🔄 Subiendo video a YouTube...")
        tags = guion_info["palabras_clave"] + ["datos interesantes", "curiosidades", "español"]

        video_id = subir_video_youtube(
            youtube,
            video_path,
            guion_info["titulo"],
            guion_info["descripcion"],
            tags,
            miniatura_path
        )

        if video_id:
            print("✅ Video subido correctamente!")
            print(f"🔗 URL: https://www.youtube.com/watch?v={video_id}")

            # Subir subtítulos si el video se subió correctamente
            if subtitulos_path:
                print("Subiendo subtítulos a YouTube...")
                try:
                    # Añadir un pequeño retraso para evitar límites de tasa
                    print("Esperando 5 segundos antes de subir subtítulos...")
                    time.sleep(5)

                    # Intentar subir los subtítulos
                    subtitulos_ok = subir_subtitulos_youtube(youtube, video_id, subtitulos_path)
                    if subtitulos_ok:
                        print("✅ Subtítulos subidos correctamente")
                    else:
                        print("❌ No se pudieron subir los subtítulos")
                except Exception as e:
                    print(f"❌ Error general al subir subtítulos: {e}")
        else:
            print("❌ Error al subir el video a YouTube.")
    else:
        print("❌ No se pudo autenticar con YouTube.")
        print("El video ha sido creado localmente en:", video_path)

if __name__ == "__main__":
    main()
