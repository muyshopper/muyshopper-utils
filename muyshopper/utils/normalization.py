"""Normalization utils."""
import re
from unidecode import unidecode


def parse_contains_boolean(input_value, keyword):
    """Check if value is in string and returns a boolean."""
    input_value = unidecode(input_value.lower())
    return keyword in input_value


def parse_contains_string(input_value, mapping):
    """Check if value is in string and returns normalized value."""
    for key in mapping.keys():
        if key in unidecode(input_value.lower()):
            return mapping[key]


def find_integer_in_string(value, count=1, limit=None):
    """Find an integer in a string."""
    if value:
        value = str(value).lower()

        try:
            numbers = re.findall(r"\d+", value)[:count]

            numbers = [int(number) for number in numbers]

            if count > 1:
                if type(numbers) is int:
                    return None
                else:
                    return numbers
            else:
                return numbers[0]
        except IndexError:
            return None


def find_float_in_string(value, limit=None, keep_right_zeros=True):
    """Find float number in a string."""
    if value:
        value = str(value).lower()

        try:
            value = value.replace(',', '.')
            number = re.findall(r"[-+]?\d*\.\d+|\d+", value)[0]
            # number = re.findall(r"\d+\.\d+", value)[0] # ONLY FLOAT, NO INT

            number = float(number)

            if not keep_right_zeros:
                if float(number) % 1 == 0:
                    number = int(number)

            if limit and number > limit:
                return None

            return number
        except IndexError:
            return None


def find_boolean_in_string(value, limit=None):
    """Find boolean in a string."""
    if value:
        value = unidecode(str(value).lower())

        positive_values = ['si', 'true']
        negative_values = ['no', 'false']

        for word in value.split():
            if word in positive_values:
                return True
            elif word in negative_values:
                return False

        return None


def find_join_integer_in_string(value, count=2, join_char='x'):
    """
    Find `count` integers in a string and returns a string
    with all of them joined by `join_char` char
    """
    integers = find_integer_in_string(value, count=count)

    if integers:
        string_value = ''

        if len(integers) == count:
            for index in range(count - 1):
                string_value += str(integers[index])
                string_value += join_char
                string_value += str(integers[index + 1])

            return string_value


def normalize_field_value(field_name, field_value):
    """Normalized field value according to the mapping."""
    try:
        func, args = field_to_normalize_function[field_name]
    except KeyError:
        return None

    if func and field_value:
        normalized_value = func(field_value, *args)
        return normalized_value
    else:
        return None


field_to_normalize_function = {
    'tipo_disco': (
        parse_contains_string, [
            {
                'rigido': 'hdd',
                'hdd': 'hdd',
                'solido': 'ssd',
                'ssd': 'ssd',
            }
        ]
    ),
    'motor_reversible': (find_boolean_in_string, []),
    'resolucion': (find_join_integer_in_string, []),
    'diametro': (find_float_in_string, []),
    'micro_SD': (find_boolean_in_string, []),
    'wifi': (find_boolean_in_string, []),
    'conveccion': (find_boolean_in_string, []),
    'ventilacion': (
        parse_contains_string, [
            {
                'derecha': 'derecha',
                'izquierda': 'izquierda',
                'natural': 'natural',
                'superior': 'superior',
                'posterior': 'posterior',
            }
        ]
    ),
    'peso': (find_float_in_string, []),
    'enfriamiento': (
      parse_contains_string, [
            {
              'no frost': 'no frost',
              'neo frost': 'neo frost',
              'ciclica': 'ciclico',
              'ciclico': 'ciclico',
              'cycle': 'ciclico',
            }
        ]
    ),
    'tipo_PC': (
        parse_contains_string, [
            {
                'all in one': 'all in one',
                'aio': 'all in one',
                'cpu': 'escritorio',
                'escritorio': 'escritorio',
                'desktop': 'escritorio',
            }
        ]
    ),
    'puertos_usb3': (find_integer_in_string, []),
    'velocidad_procesador': (find_float_in_string, []),
    'tipo_de_ventilador': (
        parse_contains_string, [
            {
                'pared': 'de pared',
                'turbo': 'turbo',
                'piso': 'de piso',
                'techo': 'de techo',
                'climatizador': 'climatizador',
            }
        ]
    ),
    'velocidades': (find_integer_in_string, []),
    'tipo_de_producto': (
        parse_contains_string, [
            {
                'natural': 'tiro natural',
                'balanceado': 'tiro balanceado',
                'gas': 'a gas',
                'electrico': 'electrico',
                'automatico': 'automatico'
            }
        ]
    ),
    'sensor': (find_boolean_in_string, []),
    'camara_delantera': (find_float_in_string, []),
    'material_de_aspas': (
        parse_contains_string, [
            {
                'plastico': 'plastico',
                'plastica': 'plastico',
                'metal': 'metal',
                'metalica': 'metal',
                'metalico': 'metal',
                'chapa': 'chapa',
                'acero': 'acero',
                'madera': 'madera',
                'pvc': 'pvc',
                'abs': 'abs',
                'aluminio': 'aluminio',
            }
        ]
    ),
    'control_remoto': (find_boolean_in_string, []),
    'puertos_usb': (find_integer_in_string, []),
    'RPM_centrifugado': (find_integer_in_string, []),
    'capacidad': (find_integer_in_string, []),
    'display': (find_boolean_in_string, []),
    'tamano_disco': (find_integer_in_string, []),
    'flash_trasera': (find_boolean_in_string, []),
    'tamano': (find_float_in_string, []),
    'color': (
        parse_contains_string, [
            {
                'blanca': 'blanco',
                'blanco': 'blanco',
                'acero': 'gris',
                'inoxidable': 'gris',
                'gris': 'gris',
                'plata': 'gris',
                'negro': 'negro',
                'negra': 'negro',
            }
        ]
    ),
    'tipo': (None, None),
    'tarjeta_SD': (find_boolean_in_string, []),
    'red': (
        parse_contains_string, [
            {
                '4g': '4g',
                'lte': '4g',
                '3g': '3g',
                'edge': 'edge',
                'gprs': 'gprs',
            }
        ]
    ),
    'genero': (
        parse_contains_string, [
            {
                'nena': 'nena',
                'nene': 'nene',
                'mujer': 'mujer',
                'hombre': 'hombre',
            }
        ]
    ),
    'eficiencia': (
        parse_contains_string, [
            {
                'a+++': 'a+++',
                'a++': 'a++',
                'a+': 'a+',
                'a': 'a',
                'b': 'b',
                'c': 'c',
                'd': 'd'
            }
        ]
    ),
    'comando': (
        parse_contains_string, [
            {
                'manual': 'analogico',
                'digital': 'digital',
                'perilla': 'analogico',
                'mecanico': 'analogico',
                'analogico': 'analogico',
            }
        ]
    ),
    'numero_Sim': (find_integer_in_string, []),
    'recuperacion_por_hora': (find_float_in_string, []),
    'dispenser_liquidos': (
        parse_contains_string, [
            {
                'hielo': 'hielo y agua',
                'agua': 'agua',
                'si': 'agua',
                'no': 'no'
            }
        ]
    ),
    'tipo_de_montaje': (
        parse_contains_string, [
            {
                'colgar': 'de colgar',
                'apoyar': 'de apoyar',
                'dual': 'dual',
                'pie': 'de pie',
            }
        ]
    ),
    'encendido_electrico': (find_boolean_in_string, []),
    'forma_de_calentamiento': (
        parse_contains_string, [
            {
                'multigas': 'multigas',
                'envasado': 'gas envasado',
                'natural': 'gas natural',
                'gas': 'gas natural',
                'electrico': 'electrico',
            }
        ]
    ),
    'alta_recuperacion': (find_boolean_in_string, []),
    'clase_energia': (
        parse_contains_string, [
            {
                'a+++': 'a+++',
                'a++': 'a++',
                'a+': 'a+',
                'a': 'a',
                'b': 'b',
                'c': 'c',
                'd': 'd',
            }
        ]
    ),
    'pantalla': (find_float_in_string, []),
    'valvula_de_seguridad': (None, None),
    'sistema_operativo': (
        parse_contains_string, [
            {
                'ubuntu': 'ubuntu',
                'w10': 'windows 10',
                'windows 10': 'windows 10',
                'windows 8.1': 'windows 8.1',
                'windows 8': 'windows 8',
                'windows 7': 'windows 7',
                'android': 'android',
                'ios': 'ios',
            }
        ]
    ),
    'camara_trasera': (find_float_in_string, []),
    'memoria_ram': (find_float_in_string, []),
    'tipo_equipo': (
        parse_contains_string, [
            {
                'ventana': 'ventana',
                'split': 'split',
                'techo': 'techo',
                'portatil': 'portatil',
            }
        ]
    ),
    'cantidad_programas': (find_integer_in_string, []),
    'tipo_de_coccion': (None, None),
    'tiraje': (
        parse_contains_string, [
            {
                'balanceado': 'tiro balanceado',
                'superior': 'superior',
                'posterior': 'posterior',
                'natural': 'tiro natural',
            }
        ]
    ),
    'autolimpiante': (find_boolean_in_string, []),
    'alto': (find_float_in_string, []),
    'pantalla_touch': (find_boolean_in_string, []),
    'profundo': (find_float_in_string, []),
    'bateria': (find_integer_in_string, []),
    'potencia': (find_integer_in_string, []),
    'procesador': (None, None),
    'tresd': (find_boolean_in_string, []),
    'conexion': (
        parse_contains_string, [
            {
                'dual': 'superior e inferior',
                'superior e inferior': 'superior e inferior',
                'superior - inferior': 'superior e inferior',
                'superior (e inferior)': 'superior e inferior',
                'superior': 'superior', 'inferior': 'inferior',
            }
        ]
    ),
    'placa_grafica': (None, None),
    'frigorias': (find_integer_in_string, []),
    'operador': (
        parse_contains_string, [
            {
                'libre': 'libre',
                'movistar': 'movistar',
                'claro': 'claro',
                'personal': 'personal',
                'nextel': 'nextel',
                'tuenti': 'tuenti',
            }
        ]
    ),
    'timer': (find_boolean_in_string, []),
    'luz_interna': (find_boolean_in_string, []),
    'ancho': (find_float_in_string, []),
    'puertos_hdmi': (find_integer_in_string, []),
    'control': (None, None),
    'grill': (find_boolean_in_string, []),
    'smart': (find_boolean_in_string, []),
    'tipo_de_conexion': (None, None),
    'almacenamiento': (find_integer_in_string, []),
    'tambor': (None, None),
    'spiedo': (find_boolean_in_string, []),
    'termostato': (find_boolean_in_string, []),
    'tipo_carga': (
        parse_contains_string, [
            {
                'frontal': 'frontal',
                'superior': 'superior',
            }
        ]
    ),
}
