from funciones import listar_pokemon_por_habilidad
from funciones import traer_datos_archivos
from funciones import contar_caracteristica
from funciones import listar_pokemones_por_tipo
from funciones import guardar_pokemon_por_tipo
from funciones import leer_pokemon
from funciones import listar_pokemones_ordenados
from funciones import generar_codigo_pokemon
from funciones import eliminar_pokemon_por_valor
from funciones import agregar_codigos_pokemon

def imprimir_menu():
        print("""
            DESAFIO-POKEMON || DESAFIO-POKEMON
        _________________________________________
        ########### ELIJA UNA OPCION ############
        
        1. Traer datos desde archivo:
        2. Listar cantidad por tipo:
        3. Listar pokemones por tipo:
        4. Listar pokemones por habilidad:
        5. Listar pokemones ordenados:
        6. Guardar Json:
        7. Leer Json:
        9. Eliminar pokemon por campo indicando el valor.
        10. Generar el codigo del Pokemon.
        11. Agregar el codigo al archivo
        12 Salir
        _________________________________________
        """)


def mostrar_menu_principal():
    while True:
        imprimir_menu()
        opcion = int(input("Ingrese la opcion a elegir"))
        match opcion:
                case 1:
                    path = input("Ingrese el nombre del archivo .csv")
                    print(traer_datos_archivos(path))                    
                case 2:
                    path = input("Ingrese el nombre del archivo .csv")
                    contar_caracteristica(path)
                
                case 3:
                    path = input("Ingrese el nombre del archivo .csv")
                    listar_pokemones_por_tipo(path)
                    
                case 4:
                    path = input("Ingrese el nombre del archivo .csv")
                    habilidad = input("Ingrese la habilidad a listar.").capitalize()
                    listar_pokemon_por_habilidad(path, habilidad)
                
                case 5:
                    path = input("Ingrese el nombre del archivo .csv")
                    listar_pokemones_ordenados(path)
                
                case 6:
                    path = input("Ingrese el nombre del archivo .csv ")
                    tipo = input("Ingrese el tipo de pokemon a guardar en JSON.").capitalize()
                    guardar_pokemon_por_tipo(path, tipo)
                case 7:
                    tipo = input("Ingrese el tipo de pokemon a leer").capitalize()
                    archivo = input("Ingrese como se llama el archivo sin el JSON")
                    leer_pokemon(tipo, archivo)
                
                case 9:
                    path = input("Ingrese el nombre del archivo CSV")
                    campo = input("Ingrese el campo del pokemon a eliminar")
                    valor = input("Ingrese el valor del campo")
                    if valor.isnumeric():
                        valor = int(valor)
                    eliminar_pokemon_por_valor(path, campo, valor)
                case 10:
                    pokemon_nombre = input("Ingrese el nombre del pokemon para generar el codigo").capitalize()
                    path = input("Ingrese el nombre del archivo SCV")
                    print(generar_codigo_pokemon(pokemon_nombre, path))
                case 11:
                    path = input("Ingrese el nombre del archivo SCV")
                    agregar_codigos_pokemon(path)
                case 12:
                    print("Haz salido!")
                    break