# 🏢 Consulta de Contribuyentes AFIP

Una aplicación web desarrollada con Streamlit que permite consultar datos de contribuyentes de la AFIP (Administración Federal de Ingresos Públicos) de Argentina mediante su CUIT.

## 🚀 Características

- **Búsqueda por CUIT**: Consulta de contribuyentes ingresando su CUIT
- **Validación de entrada**: Verifica que el CUIT tenga el formato correcto
- **Interfaz intuitiva**: Diseño moderno y fácil de usar
- **Datos en tiempo real**: Consulta directa a los servicios web de AFIP
- **Visualización clara**: Presentación organizada de la información del contribuyente
- **Funciona con Enter**: Búsqueda rápida con tecla Enter

## 📋 Requisitos

- Python 3.7 o superior
- Conexión a internet
- Credenciales válidas de AFIP (certificado, clave privada y token de acceso)

## 🛠️ Instalación Local

1. **Clonar o descargar el proyecto**

2. **Instalar las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar las credenciales AFIP**:

   - Crear archivo `.env` en la raíz del proyecto
   - Agregar las siguientes variables:

   ```
   cuit=tu_cuit
   cert=tu_certificado
   key=tu_clave_privada
   access_token=tu_token
   ```

4. **Ejecutar la aplicación**:
   ```bash
   streamlit run app.py
   ```

## 🚀 Deploy en Streamlit Cloud

### 1. Preparar el repositorio

- Asegúrate de que todos los archivos estén en tu repositorio Git
- El archivo `.gitignore` ya está configurado para excluir archivos sensibles

### 2. Configurar variables de entorno en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu repositorio de GitHub
3. En la configuración del deploy, agrega las siguientes variables de entorno:
   - `cuit`: Tu CUIT de AFIP
   - `cert`: Tu certificado completo (incluye BEGIN y END)
   - `key`: Tu clave privada completa (incluye BEGIN y END)
   - `access_token`: Tu token de acceso de AFIP

### 3. Deploy

- Streamlit Cloud detectará automáticamente el archivo `app.py`
- El deploy se realizará automáticamente

## 📱 Uso

1. **Ingresar CUIT**: Escribe el CUIT del contribuyente que deseas consultar

   - Puedes usar formato con guiones: `20-12345678-9`
   - O sin guiones: `20123456789`

2. **Buscar**: Haz clic en "🔍 Buscar" o presiona Enter

3. **Ver resultados**: Los datos del contribuyente se mostrarán organizados en secciones:
   - **📋 Información General**: Contribuyente, CUIT, tipo, estado
   - **🏢 Información de Actividad**: Actividad principal y detalles
   - **📍 Información de Domicilio**: Dirección y ubicación

## 📊 Datos mostrados

La aplicación muestra los siguientes datos del contribuyente:

- **Contribuyente**: Nombre y apellido
- **CUIT**: Clave Única de Identificación Tributaria
- **Tipo de Persona**: Clasificación del contribuyente
- **Estado**: Estado actual del contribuyente
- **Forma Jurídica**: Forma jurídica de la entidad
- **Actividad Principal**: Descripción completa de la actividad económica
- **Domicilio**: Dirección fiscal completa

## ⚠️ Notas importantes

- **Credenciales**: Asegúrate de tener credenciales válidas y actualizadas de AFIP
- **Producción**: La aplicación está configurada para usar el entorno de producción de AFIP
- **Límites**: Respeta los límites de consulta establecidos por AFIP
- **Privacidad**: Los datos obtenidos son públicos y están disponibles en el padrón de AFIP

## 🛡️ Seguridad

- Las credenciales se manejan a través de variables de entorno
- El archivo `.env` está excluido del control de versiones
- Para producción, usa las variables de entorno de Streamlit Cloud

## 📝 Licencia

Este proyecto es de uso educativo y personal. Asegúrate de cumplir con los términos de uso de la API de AFIP.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

---

_Desarrollado con ❤️ usando Streamlit y la API de AFIP_
