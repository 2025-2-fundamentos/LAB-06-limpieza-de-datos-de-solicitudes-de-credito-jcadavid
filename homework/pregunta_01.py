"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    import pandas as pd
    import os
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    input_path = 'files/input/solicitudes_de_credito.csv'
    df = pd.read_csv(input_path, sep=';')

    df = df.drop(columns=['Unnamed: 0'], errors='ignore') \
           .dropna() \
           .drop_duplicates()

    fecha = df['fecha_de_beneficio'].str.split('/', expand=True)
    fecha.columns = ['dia', 'mes', 'anio']

    mask = fecha['anio'].str.len() < 4
    fecha.loc[mask, ['dia', 'anio']] = fecha.loc[mask, ['anio', 'dia']].values

    df['fecha_de_beneficio'] = (
        fecha['anio'] + '-' + fecha['mes'] + '-' + fecha['dia']
    )

    text_columns = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito']
    df[text_columns] = (
        df[text_columns]
        .apply(lambda col: col.str.lower().str.replace(r'[-_]', ' ', regex=True).str.strip())
    )

    df['barrio'] = df['barrio'].str.lower().str.replace(r'[-_]', ' ', regex=True)

    df['monto_del_credito'] = (
        df['monto_del_credito']
        .str.replace(r'[$,\s]', '', regex=True)
        .astype(float)
        .fillna(0)
        .astype(int)
        .astype(str)
    )

    df = df.drop_duplicates()

    output_path = 'files/output'
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(os.path.join(output_path, 'solicitudes_de_credito.csv'), sep=';', index=False)

    return df.head()