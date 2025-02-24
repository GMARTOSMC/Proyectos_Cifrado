## Importamos las bibliotecas necesarias
import streamlit as st # Streamlit para crear la interfaz web
import os # Módulo para manejar archivos en el sistema
from cryptography.fernet import Fernet # Para cryptography

# Título de la aplicación en Streamlit
st.title("Cifrado Fernet-Cryptography - Codificación y Decodificación")

# Generar clave e inicializar variables
if "clave" not in st.session_state:
   st.session_state.clave = Fernet.generate_key()  # Generar la clave
   st.session_state.cipher = Fernet(st.session_state.clave)  # Crear el cifrador
if "texto_cifrado" not in st.session_state:
    st.session_state.texto_cifrado = "" #Inicializamos una variable para guardar el texto cifrado

# Sección para subir un archivo de texto
archivo = st.file_uploader("Sube un archivo TXT", type=["txt"], key="file_uploader_1")

# Verificamos si el usuario ha subido un archivo
if archivo:
    texto = archivo.read().decode("utf-8")  # Leer y decodificar el archivo
    st.text_area("Contenido del archivo:", texto, height=200)

    # Botón para cifrar el texto
    if st.button("Cifrar"):
        # Ciframos el texto leído del archivo
        mensaje_cifrado = st.session_state.cipher.encrypt(texto.encode())

        # Guardamos el mensaje cifrado en el estado de la sesión
        st.session_state.texto_cifrado = mensaje_cifrado
        
        # Mostramos texto cifrado
        st.markdown(f"Texto cifrado: `{mensaje_cifrado}`")  
              
        # Creamos la carpeta si no existe
        if not os.path.exists("archivos"):
            os.makedirs("archivos")
            
        # Guardamos el texto cifrado en un archivo dentro de la carpeta "archivos"
        with open("archivos/cifrado.txt", "wb") as f:
            f.write(mensaje_cifrado)
        
        # Confirmamos que funciona
        st.success("Texto cifrado guardado en 'archivos/cifrado.txt'")
    
    # Botón para descifrar el texto
    if st.button("Descifrar"):
        if os.path.exists("archivos/cifrado.txt"):
            with open("archivos/cifrado.txt", "rb") as f:
                mensaje_cifrado = f.read()                          
            mensaje_descifrado = st.session_state.cipher.decrypt(mensaje_cifrado).decode()            
            st.markdown(f"Texto descifrado: `{mensaje_descifrado}`")
            
            # Guardamos el texto descifrado en un archivo dentro de la carpeta "archivos"
            with open("archivos/descifrado.txt", "w", encoding="utf-8") as f:
                f.write(mensaje_descifrado)
            
            st.success("Texto descifrado guardado en 'archivos/descifrado.txt'")
