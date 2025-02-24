# Importamos las bibliotecas necesarias
import streamlit as st # Streamlit para crear la interfaz web
import os # Módulo para manejar archivos en el sistema
from Crypto.Cipher import AES # Para cryptodome
from Crypto.Random import get_random_bytes # Para crear la clave aleatoria

# Título de la aplicación en Streamlit
st.title("Cifrado Pycryptodome - Codificación y Decodificación")

# Generamos clave e inicializamos
if "clave" not in st.session_state:
    st.session_state.clave = get_random_bytes(16)  # Generar clave aleatoria de 16 bytes

if "texto_cifrado" not in st.session_state:
    st.session_state.texto_cifrado = None

if "nonce" not in st.session_state:
    st.session_state.nonce = None

if "tag" not in st.session_state:
    st.session_state.tag = None

# Sección para subir un archivo de texto
archivo = st.file_uploader("Sube un archivo TXT", type=["txt"], key="file_uploader_1")

# Verificamos si el usuario ha subido un archivo
if archivo:
    texto = archivo.read().decode("utf-8")  # Leer y decodificar el archivo
    st.text_area("Contenido del archivo:", texto, height=200)

    # Botón para cifrar el texto
    if st.button("Cifrar"):
        cipher = AES.new(st.session_state.clave, AES.MODE_EAX)  # Crear nuevo cifrador AES EAX
        texto_bytes = texto.encode("utf-8")  # Convertir a bytes
        cifrado, tag = cipher.encrypt_and_digest(texto_bytes)  # Cifrar y obtener el tag
        
        # Guardamos en la sesión
        st.session_state.texto_cifrado = cifrado
        st.session_state.nonce = cipher.nonce
        st.session_state.tag = tag
        
        # Mostramos texto cifrado
        st.markdown(f"**Texto cifrado:** `{cifrado.hex()}`") # Si lo dejamos como str no funciona
        
        # Creamos carpeta "archivos" si no existe
        if not os.path.exists("archivos"):
            os.makedirs("archivos")
            
            # Guardamos el texto cifrado en un archivo dentro de la carpeta "archivos"
        with open("archivos/cifrado.txt", "wb") as f:
            f.write(cifrado)
        
        # Confirmamos que funciona
        st.success("Texto cifrado guardado en 'archivos/cifrado.txt'")
    
    # Botón para descifrar el texto
    if st.button("Descifrar"):
        if st.session_state.texto_cifrado:
            try:
                cipher_dec = AES.new(st.session_state.clave, AES.MODE_EAX, nonce=st.session_state.nonce)
                mensaje_descifrado = cipher_dec.decrypt_and_verify(st.session_state.texto_cifrado, st.session_state.tag).decode("utf-8")
                
                # Guardamos el texto descifrado en un archivo dentro de la carpeta "archivos"
                with open("archivos/descifrado.txt", "w", encoding="utf-8") as f:
                    f.write(mensaje_descifrado)
                
                st.success("Texto descifrado correctamente y guardado en 'archivos/descifrado.txt'")
                st.text_area("Texto Descifrado:", mensaje_descifrado, height=200)
            except ValueError:
                st.error("Error. El texto cifrado no es valido o la clave es erronea")
        else:
            st.warning("No hay texto cifrado para descifrar. Cifra un texto primero.")
