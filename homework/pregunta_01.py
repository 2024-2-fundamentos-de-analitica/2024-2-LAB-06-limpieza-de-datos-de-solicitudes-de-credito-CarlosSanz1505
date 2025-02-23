"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import os
    import re
    import pandas as pd
    
    data = pd.read_csv('./files/input/solicitudes_de_credito.csv', sep=';', index_col=0, encoding='utf-8')

    """RESULTADO: Sin problemas en `estrato` y `comuna_ciudadano`."""

    # Verificación de data textual
    # for col in data.dtypes[data.dtypes == 'object'].index:
    #     print('VALUE_COUNTS()\n', data.value_counts(col), '\n')
    """RESULTADO:
    - `sexo`: uso inconsistente de mayúsculas
    - `tipo_de_emprendimiento`: uso inconsistente de mayúsculas
    - `idea_negocio`: valores incompletos(?) (e.g. 'fabrica de '),
        espaciado inconsistente, uso inconsistente de mayúsculas
    - `barrio`: uso inconsistente de mayúsculas, espaciado inconsistente, ...
    - `fecha_de_beneficio`: formato de fecha inconsistente
    - `monto_del_credito`: formato de cantidad inconsistente (xxxxx y 
        $ x,xxx,xxx.xx)
    - `línea_credito`: uso inconsistente de mayúsculas, 
        espaciado inconsistente (' ', '-', '_'), 
        palabras mal escritas (?) (e.g. 'solidaria' y 'soli-diaria')
    """
    
    # Corrección de uso inconsistente de mayúsculas
    caps_vars = [
        'sexo', 'tipo_de_emprendimiento', 'idea_negocio', 
        'barrio', 'línea_credito'
    ]
    for var in caps_vars:
        data[var] = data[var].str.lower()

    # Corrección de espaciado inconsistente y tildes
    spcs_vars = ['idea_negocio', 'barrio', 'línea_credito']
    for var in spcs_vars:
        data[var] = data[var].apply(lambda d: re.sub(r'[-_]', ' ', str(d)))
        special_chars = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': '¿', 'bel¿n': 'belen'}
        for vowel, repl in special_chars.items():
            data[var] = data[var].apply(lambda d: re.sub(vowel, repl, str(d)))
        data[var] = data[var].str.strip()
    
    # Corrección de formato de moneda
    data['monto_del_credito'] = data['monto_del_credito'].apply(lambda x: float(re.sub(r'[($ ),]', '', x)))
    
    # Corrección de formato de fecha
    data['fecha_de_beneficio'] = data['fecha_de_beneficio'].apply(lambda d: re.sub(r'(\d{4})\/(\d{2})\/(\d+)', r'\3/\2/\1', d))

    # Borrar registros con NA's y duplicados
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)

    # Generar archivo de salida
    if not os.path.exists('./files/output'):
        os.makedirs('./files/output')
    data.to_csv('./files/output/solicitudes_de_credito.csv', sep=';')
pregunta_01()