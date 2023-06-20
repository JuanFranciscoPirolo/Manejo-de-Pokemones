import re
import os
import json
from unidecode import unidecode
import csv

def validar_datos(path:str):
    """
    Valido datos en caso de un incorrecto uso del usuario.
    Parametros:
    path: el archivo scv a validar.
    Returns:
    Esta funcion no devuelve nada
    """
    
    if type(path) != str or len(path) == 0:
            print("""\nError, no haz ingresado texto o el casillero esta vacio.
            ¡Intenta de nuevo!\n""")
            return
    if not os.path.isfile(path):
        print(f"\nError: el archivo '{path}' no existe.\n")
        return 

def separar_habilidades(habilidades:list) -> list:
            habilidad_sin_separador = habilidades.replace("|*|", ",")
            habilidad_sin_ninguna = re.sub(r'\bNinguna\b', '', habilidad_sin_separador)
            habilidad = re.sub(r'\n', '', habilidad_sin_ninguna)
            habilidad_final = habilidad.rstrip(',')
            habilidades = re.split(r',\s*', habilidad_final)
            return habilidades

def traer_datos_archivos(path:str) -> list:
    """
    Brief: Lee los datos de un archivo csv en la ruta especificada 
    y los convierte en una lista de diccionarios que representan
    cada uno de los pokemones encontrados en el archivo.

    Parametros:
        path(str): Ruta del archivo csv que contiene los datos de los pokemones.

    Returns:
        list: Lista de diccionarios que representan cada uno de los pokemones encontrados en el archivo.
    """
    validar_datos(path)
    pokemones = []
    with open(path, "r" , encoding="UTF-8") as file:
        next(file)
        for linea in file:
            lista = re.split(",", linea)
            habilidades = separar_habilidades(lista[5])
            tipo = lista[2].replace("/", ",")
            tipos_separados = re.split(r',\s*', tipo)
            diccionario_pokemon = {}
            diccionario_pokemon['N° Pokedex'] = lista[0]
            diccionario_pokemon['Nombre'] = lista[1].strip()
            diccionario_pokemon['Tipo'] = tipos_separados
            diccionario_pokemon['Poder de Ataque'] = int(lista[3])
            diccionario_pokemon['Poder de Defensa'] = int(lista[4])
            diccionario_pokemon['Habilidades'] = habilidades
            pokemones.append(diccionario_pokemon)
    
    return pokemones

def contar_caracteristica(path:str) -> list:
    '''Brief: Cuenta la cantidad de pokemones que tienen 
    cada tipo de pokemon

    Parámetros:
    
    path: Un string que representa la ruta del archivo que contiene la información de los pokemones.
    Return:
    
    tipos_pokemones: Una lista con la cantidad de pokemones que tienen cada tipo.
    Además, la función imprime por pantalla la cantidad de pokemones que tienen cada tipo.
    '''
    validar_datos(path)
    nueva_lista = {}
    pokemones = traer_datos_archivos(path)

    for pokemon in pokemones:
        tipos = pokemon['Tipo']
        
        for tipo in tipos:
            if tipo == "":
                tipo = "No Tiene"

            if tipo not in nueva_lista:
                nueva_lista[tipo] = 1
            else:
                nueva_lista[tipo] += 1

    for tipo, cantidad in nueva_lista.items():
        tipos_pokemones = print(f"""
{tipo}
------
{cantidad}
                                    """)
    return tipos_pokemones


def listar_pokemones_por_tipo(path:str):
    """
    Brief: Lista los pokemones agrupados por tipo de pokemon, 
    mostrando para cada uno su nombre, la cantidad de pokemones que tienen ese tipo y
    su poder de ataque.

    Parámetros:
    path: cadena de caracteres que indica la ruta del archivo csv a procesar.
    Return: Esta función no devuelve nada, 
    imprime en consola la lista de pokemones agrupados por tipo de pokemon.
    """
    validar_datos(path)
    
    pokemones = traer_datos_archivos(path)
    
    tipos_pokemones = {}
    
    for pokemon in pokemones:
        
        for tipo in pokemon['Tipo']:
            
            if tipo not in tipos_pokemones:
                tipos_pokemones[tipo] = [pokemon]
            else:
                tipos_pokemones[tipo].append(pokemon)
                
    for tipo, lista_pokemones in tipos_pokemones.items():
        print(f"\nPokemones de tipo {tipo}:")
        for pokemon in lista_pokemones:
            print(f"Nombre: {pokemon['Nombre']} | Poder de Ataque: {pokemon['Poder de Ataque']}")



def listar_pokemon_por_habilidad(path:str, habilidad:str):
    """
    Brief: Imprime una lista de pokemones que tienen esa habilidad pasada por parametro, con su promedio de poder.

    Parámetros:

    path : str - La ruta del archivo csv que contiene los datos de los pokemones.
    habilidad : str - La habilidad que se desea buscar en los pokemones.
    Return: No devuelve nada, solo imprime los pokemones.

    """
    validar_datos(path)
    pokemones = traer_datos_archivos(path)
    habilidad_encontrada = False
    habilidad_pokemones = {}

    for pokemon in pokemones:
        tipo = tuple(pokemon["Tipo"])

        for hab in pokemon["Habilidades"]:
            habilidad_normalizada = unidecode(hab).lower()
            if habilidad_normalizada == habilidad.lower():
                habilidad_encontrada = True

                poder_ataque = int(pokemon['Poder de Ataque'])
                poder_defensa = int(pokemon['Poder de Defensa'])
                promedio_poder = (poder_ataque + poder_defensa) / 2

                if tipo not in habilidad_pokemones:
                    habilidad_pokemones[tipo] = []
                
                habilidad_pokemones[tipo].append((pokemon["Nombre"], promedio_poder))
                habilidad_encontrada = True

    if not habilidad_encontrada:
        print("Error, habilidad no encontrada.")
    else:

    
        for tipo, lista_pokemones in habilidad_pokemones.items():
            print(f"\nPokemones de tipo {tipo} con la habilidad '{habilidad}':")

            if not lista_pokemones:
                print("No hay pokemones con esta habilidad.")
            else:
                for pokemon in lista_pokemones:
                    print(f"Nombre: {pokemon[0]} | Promedio de poder entre ataque y defensa: {pokemon[1]:.2f}")

def listar_pokemones_ordenados(path):
    """
    Brief: Imprime la lista de pokemones ordenados por su poder de ataque y, en caso de ser iguales, por orden alfabético.
    Ordenamiento burbuja.
    
    Parámetros:
    path : str - La ruta del archivo csv que contiene los datos de los pokemones.

    Return:
    No devuelve nada, solo imprime los pokemones.
    """
    validar_datos(path)
    pokemones = traer_datos_archivos(path)
    
    longitud_pokemon = len(pokemones)
    for i in range(longitud_pokemon-1):
        for j in range(i+1, longitud_pokemon):
            if pokemones[i]["Poder de Ataque"] < pokemones[j]["Poder de Ataque"] or \
            (pokemones[i]["Poder de Ataque"] == pokemones[j]["Poder de Ataque"] and \
            pokemones[i]["Nombre"] > pokemones[j]["Nombre"]):
                pokemones[i], pokemones[j] = pokemones[j], pokemones[i]
    
    for pokemon in pokemones:
        print(pokemon)

def guardar_pokemon_por_tipo(path:str, tipo:str):
    """
    Brief: Crea un archivo JSON con los datos de los pokemones 
    que tienen el tipo pasado por parametro.
    
    Parámetros:
    path : str - La ruta del archivo csv que contiene los datos de los pokemones.
    tipo : str - El tipo de pokemon que quiero buscar en los datos.

    Return:
    No devuelve nada, solo crea el archivo si hay pokemones con el tipo especificado, 
    de lo contrario imprime un mensaje indicando 
    que no hay pokemones con ese tipo.
    """
    validar_datos(path)
    pokemones = traer_datos_archivos(path)
    pokemon_tipo = []
    
    for pokemon in pokemones:
        for tipos in pokemon['Tipo']:
            tipo_normalizado = unidecode(tipos)
            if tipo == tipo_normalizado:
                nombre = pokemon["Nombre"]
                poder_ataque = int(pokemon['Poder de Ataque'])
                poder_defensa = int(pokemon['Poder de Defensa'])
                if poder_ataque > poder_defensa:
                    tipo_poder = "Ataque"
                    mayor_poder = poder_ataque
                else:
                    tipo_poder = "Defensa"
                    mayor_poder = poder_defensa
                pokemon_tipo.append({"Nombre": nombre, "Mayor Poder": mayor_poder, "Tipo de poder": tipo_poder})
        
    if pokemon_tipo:
        with open(f"{tipo}.json", "w") as file:
            json.dump(pokemon_tipo, file, indent=4)
        print(f"Archivo {tipo}.json creado exitosamente.")
    else:
        print(f"No hay pokemones de tipo {tipo}.")



def leer_pokemon(tipo: str, archivo: str) -> None:
    """
    Brief: 
    Muestra por pantalla la lista de pokemones de ese tipo presentes en el archivo, 
    junto con su mayor poder y si este es de ataque o defensa.

    Parámetros:
    tipo (str): el tipo de pokemon a buscar en el archivo.
    archivo (str): el nombre del archivo en formato JSON a leer.
    Return: No devuelve nada, solo imprime
    """
    nombre_archivo = f"{archivo}.json"
    
    if not os.path.isfile(nombre_archivo):
        print(f"\nError: el archivo '{nombre_archivo}' no existe.\n")
        return 
    
    with open(nombre_archivo, "r") as file:
        pokemones = json.load(file)
        
        if not pokemones:
            print(f"No hay pokemones de tipo {tipo} en el archivo.")
            return
        print(f"Lista de pokemones de tipo {tipo}:")
        
        for pokemon in pokemones:
            print(f"- {pokemon['Nombre']}: {pokemon['Tipo de poder']} ({pokemon['Mayor Poder']})")




def validar_campo_primera_linea(path: str, campo: str) -> bool:
    """
    Valida si un campo está presente en la primera línea de un archivo CSV.

    Args:
        path (str): Ruta del archivo CSV.
        campo (str): Campo a validar.

    Returns:
        bool: True si el campo está presente en la primera línea, False en caso contrario.
    """
    with open(path, 'r', encoding='utf-8') as file:
        primera_linea = file.readline().strip()
        campos = primera_linea.split(',')
        resultado = campo in campos
        return resultado


def eliminar_pokemon_por_valor(path: str, campo: str, valor: str):
    """
    Elimina un Pokémon del archivo CSV por un valor específico en un campo determinado.

    Args:
        path (str): Ruta del archivo CSV.
        campo (str): Campo en el que se buscará el valor a eliminar.
        valor (str): Valor a buscar y eliminar en el campo especificado.

    Returns:
        None
    """
    pokemones = traer_datos_archivos(path)
    bandera_pokemon = False

    if not validar_campo_primera_linea(path, campo):
        print("El campo especificado es incorrecto")
        return

    datos_pokemones = pokemones[:]
    for pokemon in pokemones[:]:
        if type(valor) == int:
            if str(pokemon[campo]) == str(valor):
                datos_pokemones.remove(pokemon)
                bandera_pokemon = True
        elif valor in pokemon[campo]:
            datos_pokemones.remove(pokemon)
            bandera_pokemon = True

    if not bandera_pokemon:
        print("No se encontró ningún Pokémon con el valor especificado.")
        return

    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(path, 'w', encoding='utf-8') as file:
        file.write(lines[0])
        for line in lines[1:]:
            if str(valor) not in line:
                file.write(line)
    print("Pokemon eliminado correctamente")

def generar_codigo_pokemon(pokemon_nombre:str, path:str):
    """
    Genera el código del Pokémon utilizando su nombre y datos del archivo CSV.

    Args:
        pokemon_nombre (str): Nombre del Pokémon.
        path (str): Ruta del archivo CSV.

    Returns:
        str: Código del Pokémon generado.
    """

    validar_datos(path)
    pokemones = traer_datos_archivos(path)
    pokemon_encontrado = False
    codigo = None
    
    for pokemon in pokemones:
        if pokemon['Nombre'] == pokemon_nombre:
            primera_letra = pokemon['Nombre'][0]
            numero_pokedex = str(pokemon['N° Pokedex'])
            
            if pokemon['Poder de Ataque'] > pokemon['Poder de Defensa']:
                mayor_ataque = pokemon['Poder de Ataque']
                codigo = f"{primera_letra}-A-{mayor_ataque}-{numero_pokedex}"
                
            elif pokemon['Poder de Ataque'] == pokemon['Poder de Defensa']:
                igual_ataque_defensa = pokemon['Poder de Ataque']
                codigo = f"{primera_letra}-AD-{igual_ataque_defensa}-{numero_pokedex}"
                
            else:
                mayor_defensa = pokemon['Poder de Defensa']
                codigo = f"{primera_letra}-D-{mayor_defensa}-{numero_pokedex}"
            
            if len(numero_pokedex) == 1:
                codigo = codigo[:-1] + codigo[-1].zfill(13 - len(codigo))
            elif len(numero_pokedex) == 2:
                codigo = codigo[:-2] + codigo[-2:].zfill(14 - len(codigo))
            elif len(numero_pokedex) == 3:
                codigo = codigo[:-3] + codigo[-3:].zfill(15 - len(codigo))
            
            pokemon_encontrado = True
            break
    
    if not pokemon_encontrado:
        print("El Pokémon no se encuentra en la lista.")
    
    return codigo


def agregar_codigos_pokemon(path:str):
    """
    Agrega los códigos de Pokémon faltantes al archivo CSV especificado.

    Args:
        path (str): Ruta del archivo CSV.
    """
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        pokemones = list(reader)
        numero_principio = 1

    def generar_codigo(i, pokemon):
        if 'Codigo de Pokemon' in pokemon:
            print(f"El Pokémon '{pokemon['Nombre']}' ya tiene un código de Pokémon: {pokemon['Codigo de Pokemon']}")
        else:
            codigo = generar_codigo_pokemon(pokemon['Nombre'], path)
            pokemon['Codigo de Pokemon'] = codigo
        return pokemon

    pokemones_actualizados = list(map(lambda x: generar_codigo(*x), enumerate(pokemones, start=numero_principio)))

    with open(path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Nombre', 'N° Pokedex', 'Poder de Ataque', 'Poder de Defensa', 'Tipo', 'Habilidades', 'Codigo de Pokemon']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pokemones_actualizados)





















