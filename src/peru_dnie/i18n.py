# Standard Library
import locale
import os


def get_current_language():
    default_locale = locale.getdefaultlocale()
    if len(default_locale) > 0 and default_locale[0] is not None:
        current_lang = default_locale[0].split("_")[0]
        if current_lang not in ["en", "es"]:
            current_lang = "en"
    else:
        current_lang = "en"

    force_lang = os.getenv("PERUDNIE_LANG", None)
    if force_lang is not None:
        current_lang = force_lang

    return current_lang


LANG = {
    "en": {
        "cli": {
            "sign": {
                "sign_help": "Sign with the DNIe",
                "input_file_help": "File to sign",
                "output_file_help": "Output signature file",
                "hash_algorithm_help": "Hash algorithm for the signature",
            },
            "extract": {
                "extract_help": "Extract certificates from the DNIe",
                "certificate_type_help": "Type of certificate to extract",
                "output_file_help": "Output public certificate file",
            },
            "program_description": "Utilities for the Peruvian DNIe Smart Card cryptographic functions",
            "available_tasks": "Available DNIe tasks",
        },
        "init": {
            "choose_reader": "Choose reader",
            "readers": "[bold underline]Readers:",
            "waiting_dnie": "Waiting for DNIe...",
            "found_dnie": "[green]Found DNIe V2",
        },
        "certificates": {
            "reading_cert": "Reading signature certificate...",
            "success": "[green]Certificate successfully loaded",
            "failed": "[red]Could not read certificate",
            "wrote_cert": "[green]Wrote certificate to '{}'",
        },
        "general": {
            "enter_pin": "Please enter your PIN",
        },
        "errors": {
            "lc_must_none": "'lc' must be None if 'data' is None",
            "lc_must_length": "'lc' must be the length of 'data'",
            "dnie_not_init": "DNIe card is not initialized",
            "dnie_not_found": "Could not find DNIe",
            "could_not_select_pki": "Could not select PKI app: '{}'",
            "could_not_select_cert": "Could not select signature certificate file: '{}'",
            "could_not_read_cert": "Could not read certificate: '{}'",
            "wrong_while_reading": "Something went wrong while reading the certificate: '{}'",
            "certificate_not_supported": "Certificate type extraction not supported",
            "failed_pin": "Failed to verify PIN: '{}'",
            "could_not_set_env": "Could not set security environment: '{}'",
            "could_not_sign": "Could not sign payload: '{}'",
        },
    },
    "es": {
        "cli": {
            "sign": {
                "sign_help": "Firmar con el DNIe",
                "input_file_help": "Archivo a firmar",
                "output_file_help": "Archivo de firma resultante",
                "hash_algorithm_help": "Algoritmo de hash para la firma",
            },
            "extract": {
                "extract_help": "Extraer certificados del DNIe",
                "certificate_type_help": "Tipo de certificado a extraer",
                "output_file_help": "Archivo de certificado público resultante",
            },
            "program_description": "Utilidades para las funciones criptográficas de la Tarjeta Inteligente DNIe peruana",
            "available_tasks": "Tareas DNIe disponibles",
        },
        "init": {
            "choose_reader": "Elegir lector",
            "readers": "[bold underline]Lectores:",
            "waiting_dnie": "Esperando el DNIe...",
            "found_dnie": "[green]DNIe V2 encontrado",
        },
        "certificates": {
            "reading_cert": "Leyendo certificado de firma...",
            "success": "[green]Certificado cargado con éxito",
            "failed": "[red]No se pudo leer el certificado",
            "wrote_cert": "[green]Certificado escrito en '{}'",
        },
        "general": {
            "enter_pin": "Por favor, introduce tu PIN",
        },
        "errors": {
            "lc_must_none": "'lc' debe ser None si 'data' es None",
            "lc_must_length": "'lc' debe ser la longitud de 'data'",
            "dnie_not_init": "La tarjeta DNIe no está inicializada",
            "dnie_not_found": "No se pudo encontrar el DNIe",
            "could_not_select_pki": "No se pudo seleccionar la aplicación PKI: '{:!r}'",
            "could_not_select_cert": "No se pudo seleccionar el archivo de certificado de firma: '{:!r}'",
            "could_not_read_cert": "No se pudo leer el certificado: '{:!r}'",
            "wrong_while_reading": "Algo salió mal al leer el certificado: '{:!r}'",
            "certificate_not_supported": "Extracción de tipo de certificado no soportada",
            "failed_pin": "Fallo al verificar el PIN: '{:!r}'",
            "could_not_set_env": "No se pudo configurar el entorno de seguridad: '{:!r}'",
            "could_not_sign": "No se pudo firmar el payload: '{:!r}'",
        },
    },
}

current_lang = get_current_language()
t = LANG[current_lang]
