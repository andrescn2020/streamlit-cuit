import streamlit as st
import pandas as pd
from afip import Afip
import re
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Consulta de Contribuyentes AFIP", page_icon="🏢", layout="wide"
)


# Inicializar la conexión AFIP
@st.cache_resource
def init_afip():
    # Obtener credenciales desde variables de entorno
    cuit = os.getenv("cuit")
    cert = os.getenv("cert")
    key = os.getenv("key")
    access_token = os.getenv("access_token")
    production = True

    # Verificar que todas las credenciales estén disponibles
    if not all([cuit, cert, key, access_token]):
        st.error("❌ Error: Faltan credenciales de AFIP en las variables de entorno.")
        st.info("💡 Asegúrate de tener configurado el archivo .env con:")
        st.code(
            """
AFIP_CUIT=tu_cuit
AFIP_CERT=tu_certificado
AFIP_KEY=tu_clave_privada
AFIP_ACCESS_TOKEN=tu_token
AFIP_PRODUCTION=True
        """
        )
        return None

    try:
        return Afip(
            {
                "CUIT": int(cuit),
                "cert": cert,
                "key": key,
                "access_token": access_token,
                "production": production,
            }
        )
    except Exception as e:
        st.error(f"❌ Error al inicializar AFIP: {str(e)}")
        return None


def validate_cuit(cuit):
    """Validar formato de CUIT"""
    if not cuit:
        return False
    # Remover guiones y espacios
    cuit_clean = re.sub(r"[-\s]", "", str(cuit))
    # Verificar que tenga 11 dígitos
    if not cuit_clean.isdigit() or len(cuit_clean) != 11:
        return False
    return int(cuit_clean)


def get_taxpayer_details(afip_instance, cuit):
    """Obtener detalles del contribuyente"""
    try:
        return afip_instance.RegisterScopeThirteen.getTaxpayerDetails(cuit)
    except Exception as e:
        error_str = str(e)
        # Si el error indica que no existe la persona, no mostrar el error técnico
        if "No existe persona con ese Id" in error_str or "500" in error_str:
            return None
        else:
            st.error(f"Error al consultar el contribuyente: {error_str}")
            return None


def format_taxpayer_data(data):
    """Formatear los datos del contribuyente para mostrar"""
    if not data:
        return None

    # Crear un diccionario con los datos formateados
    formatted_data = {}

    # Si data es una lista, tomar el primer elemento
    if isinstance(data, list) and len(data) > 0:
        data = data[0]

    # Si data es un diccionario, procesar directamente
    if isinstance(data, dict):
        # Extraer datos de la estructura real de AFIP
        persona_data = data.get("persona", {})

        if persona_data:
            # Mapear los campos de la estructura real de AFIP
            field_mapping = {
                "idPersona": "CUIT",
                "razonSocial": "Razón Social",
                "tipoPersona": "Tipo de Persona",
                "estadoClave": "Estado",
                "formaJuridica": "Forma Jurídica",
                "descripcionActividadPrincipal": "Actividad Principal",
                "idActividadPrincipal": "ID Actividad Principal",
                "periodoActividadPrincipal": "Período Actividad Principal",
                "mesCierre": "Mes de Cierre",
                "tipoClave": "Tipo de Clave",
            }

            # Procesar campos básicos
            for key, display_name in field_mapping.items():
                if key in persona_data and persona_data[key] is not None:
                    formatted_data[display_name] = persona_data[key]

            # Unir apellido y nombre si existen
            apellido = persona_data.get("apellido", "")
            nombre = persona_data.get("nombre", "")
            if apellido or nombre:
                nombre_completo = f"{apellido} {nombre}".strip()
                if nombre_completo:
                    formatted_data["Contribuyente"] = nombre_completo

            # Procesar domicilios
            domicilios = persona_data.get("domicilio", [])
            if domicilios:
                # Tomar el primer domicilio (fiscal)
                domicilio = domicilios[0]
                domicilio_mapping = {
                    "direccion": "Dirección",
                    "calle": "Calle",
                    "numero": "Número",
                    "localidad": "Localidad",
                    "descripcionProvincia": "Provincia",
                    "codigoPostal": "Código Postal",
                    "tipoDomicilio": "Tipo de Domicilio",
                    "estadoDomicilio": "Estado del Domicilio",
                }

                for key, display_name in domicilio_mapping.items():
                    if key in domicilio and domicilio[key] is not None:
                        formatted_data[f"Domicilio - {display_name}"] = domicilio[key]

                # Si hay más de un domicilio, mostrar información
                if len(domicilios) > 1:
                    formatted_data["Cantidad de Domicilios"] = len(domicilios)

        # Si no encontramos datos en 'persona', intentar con la estructura completa
        if not formatted_data:
            # Mapear campos alternativos
            alt_field_mapping = {
                "taxpayerId": "CUIT",
                "taxpayerName": "Razón Social",
                "taxpayerType": "Tipo de Contribuyente",
                "taxpayerStatus": "Estado",
                "inscriptionDate": "Fecha de Inscripción",
                "address": "Domicilio",
                "city": "Ciudad",
                "province": "Provincia",
                "postalCode": "Código Postal",
                "country": "País",
                "email": "Email",
                "phone": "Teléfono",
                "activityStartDate": "Fecha de Inicio de Actividad",
                "activityEndDate": "Fecha de Fin de Actividad",
                "activityDescription": "Descripción de Actividad",
                "taxCategory": "Categoría Fiscal",
                "taxRegime": "Régimen Fiscal",
                # Campos adicionales que podrían estar presentes
                "cuit": "CUIT",
                "razonSocial": "Razón Social",
                "tipoPersona": "Tipo de Persona",
                "estado": "Estado",
                "fechaInscripcion": "Fecha de Inscripción",
                "domicilio": "Domicilio",
                "ciudad": "Ciudad",
                "provincia": "Provincia",
                "codigoPostal": "Código Postal",
                "pais": "País",
                "email": "Email",
                "telefono": "Teléfono",
                "fechaInicioActividad": "Fecha de Inicio de Actividad",
                "fechaFinActividad": "Fecha de Fin de Actividad",
                "descripcionActividad": "Descripción de Actividad",
                "categoriaFiscal": "Categoría Fiscal",
                "regimenFiscal": "Régimen Fiscal",
            }

            # Procesar todos los campos disponibles
            for key, display_name in alt_field_mapping.items():
                if key in data and data[key] is not None:
                    formatted_data[display_name] = data[key]

            # Si no encontramos datos mapeados, mostrar todos los campos disponibles
            if not formatted_data:
                st.warning(
                    "⚠️ No se encontraron campos mapeados. Mostrando todos los datos disponibles:"
                )
                for key, value in data.items():
                    if value is not None:
                        formatted_data[key] = value

    return formatted_data


# Título principal
st.title("🏢 Consulta de Contribuyentes AFIP")
st.markdown("---")

# Inicializar AFIP
afip = init_afip()

# Verificar que AFIP se inicializó correctamente
if afip is None:
    st.error("❌ No se pudo inicializar la conexión con AFIP")
    st.stop()

# Formulario de búsqueda
st.subheader("🔍 Buscar Contribuyente")

# Crear un formulario para que funcione con Enter
with st.form("busqueda_form"):
    # Campo de entrada para CUIT
    cuit_input = st.text_input(
        "Ingrese el CUIT del contribuyente:",
        placeholder="Ej: 20-12345678-9 o 20123456789",
        help="Puede ingresar el CUIT con o sin guiones",
    )

    # Botón de búsqueda
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_button = st.form_submit_button(
            "🔍 Buscar", type="primary", use_container_width=True
        )

# Procesar búsqueda
if search_button and cuit_input:
    # Validar CUIT
    cuit = validate_cuit(cuit_input)

    if not cuit:
        st.error("❌ CUIT inválido. Debe tener 11 dígitos numéricos.")
    else:
        with st.spinner("🔍 Consultando datos del contribuyente..."):
            # Obtener datos del contribuyente
            taxpayer_data = get_taxpayer_details(afip, cuit)

            if taxpayer_data:
                st.success(f"✅ Datos encontrados para CUIT: {cuit}")

                # Formatear y mostrar datos
                formatted_data = format_taxpayer_data(taxpayer_data)

                if formatted_data and len(formatted_data) > 0:
                    # Separar datos por categorías
                    datos_generales = {}
                    datos_actividad = {}
                    datos_domicilio = {}

                    # Primero agregar el contribuyente si existe
                    if "Contribuyente" in formatted_data:
                        datos_generales["Contribuyente"] = formatted_data[
                            "Contribuyente"
                        ]

                    for key, value in formatted_data.items():
                        if key == "Contribuyente":
                            continue  # Ya lo agregamos arriba
                        elif "Domicilio" in key:
                            datos_domicilio[key] = value
                        elif "Actividad" in key or "Período" in key or "Mes" in key:
                            datos_actividad[key] = value
                        elif key in [
                            "CUIT",
                            "Razón Social",
                            "Tipo de Persona",
                            "Estado",
                            "Forma Jurídica",
                        ]:
                            datos_generales[key] = value
                        else:
                            # Todos los demás datos van a información general
                            datos_generales[key] = value

                    # 1. INFORMACIÓN GENERAL
                    if datos_generales:
                        st.subheader("📋 Información General")
                        for key, value in datos_generales.items():
                            if value:
                                st.metric(key, str(value))

                    # 2. INFORMACIÓN DE ACTIVIDAD
                    if datos_actividad:
                        st.subheader("🏢 Información de Actividad")
                        for key, value in datos_actividad.items():
                            if value:
                                if key == "Actividad Principal":
                                    # Para la actividad principal, usar un contenedor más amplio
                                    st.markdown(f"**{key}:**")
                                    st.info(f"{value}")
                                else:
                                    st.metric(key, str(value))

                    # 3. INFORMACIÓN DE DOMICILIO
                    if datos_domicilio:
                        st.subheader("📍 Información de Domicilio")
                        for key, value in datos_domicilio.items():
                            if value:
                                st.metric(key, str(value))

                    # Si no hay datos categorizados, mostrar en formato simple
                    if not any([datos_generales, datos_actividad, datos_domicilio]):
                        st.subheader("📋 Datos del Contribuyente")
                        for key, value in formatted_data.items():
                            if value:
                                if key == "Actividad Principal":
                                    st.markdown(f"**{key}:**")
                                    st.info(f"{value}")
                                else:
                                    st.metric(key, str(value))
                else:
                    st.warning("⚠️ No se pudieron formatear los datos del contribuyente")
                    st.info("💡 Mostrando datos sin formatear:")
            else:
                st.error("❌ No se encontraron datos para el CUIT ingresado")

    # Información adicional
    # st.markdown("---")
    # st.markdown(
    """
### 📝 Información
- **CUIT**: Clave Única de Identificación Tributaria
- Los datos se obtienen directamente desde los servicios web de AFIP
- La consulta es en tiempo real
"""
# )

# Footer
# st.markdown("---")
# st.markdown("*Desarrollado con Streamlit y AFIP API*")
