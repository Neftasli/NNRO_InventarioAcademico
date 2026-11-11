"""BASE EDUCATIVA INSEGURA. Corregir los TODO antes de la entrega."""
import json
from pathlib import Path
from datetime import datetime

import seguridad

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"


def cargar_inventario():
    # TODO: controlar archivo ausente y JSON inválido. No sobrescribirlos.
    try:
        return json.loads(DATOS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("No se encontro archivo de json")
        return
    except json.JSONDecodeError:
        print("JSON tiene formato incorrecto")


def guardar_inventario(productos):
    DATOS.write_text(json.dumps(productos, indent=2), encoding="utf-8")


def registrar_evento(usuario, accion, resultado, **detalles):
    # TODO: guardar un objeto JSON por línea; fecha/hora, usuario, acción,
    # resultado y detalles no sensibles. Nunca guardar contraseña ni hash.
    data = [{"date": str(datetime.now()), "usuario": usuario, "accion": accion, "resultado": resultado, "detalles": detalles} ]

   #Utiliza "a" que significa append que lo que hace es añadir despues de una entrada sin sobreescribirla
    with open(LOG, "a", encoding="utf-8") as auditoria: 
        auditoria.write(json.dumps(data, indent=2))
    pass




def autenticar(nombre, clave):
    usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))
    
    # TODO: integrar seguridad.py y migrar usuarios.json sin claves legibles.
    for usuario in usuarios:
        #Verifica la clave escrita con la proveida hecha hash
        if usuario["usuario"] == nombre and seguridad.verificar_clave(usuario["hash"], clave):
           
            registrar_evento(nombre, "login", "exitoso")
            return {"usuario": nombre, "rol": usuario["rol"]}
    # TODO: registrar también el intento fallido.
    registrar_evento(nombre, "login", "fallido")
    print("Credenciales incorrectas.")
    return None


def consultar_inventario(sesion):
    # TODO: rechazar si no existe sesión válida. DONE
    if sesion is None:
            print("No hay sesion")
            return False
    
    productos = cargar_inventario()
    #En caso de que no exista un JSON file o tenge un error no ocurre nada
    if productos is None:
        return
    for producto in productos:
        print(producto["id"], producto["nombre"], producto["cantidad"])


#Se asegura que solo sea el admin quien trata de modificar el 
def verificar_rol(sesion):
    if sesion is None or sesion["rol"] != "admin":
        print("No hay sesion O rol equivocado.")
        return False
    else:
        return True

def modificar_cantidad(sesion, identificador, entrada):
    # TODO: verificar sesión y rol AQUÍ, antes de modificar. DONE
    
    if verificar_rol(sesion):
    
        # TODO: validar entero entre 0 y 1000, sin interrumpir el programa. DONE
        try:
            #Verifica si esta en rango apropiado
            cantidad = int(entrada)
            if (cantidad < 0 or cantidad > 1000):
                print("Cantidad no es posible porque se pasa del limite o esta en negativo")
                cantidad = None
                bCantidadCambio = False
                razonCntNoCambio = "Fuera del margen permitido"
                
        except:
            #Si no es un numero marca la cantidad como none para queno cause error
            print("Cantidad no es posible debido a que es una entrada invalida.")
            cantidad = None
            bCantidadCambio = False
            razonCntNoCambio = "Entrada invalidad"
        productos = cargar_inventario()
        for producto in productos:
            if producto["id"] == identificador:
                anterior = producto["cantidad"]

               #Si es Numero entonces cambia la cantidad
                if cantidad is not None:
                    producto["cantidad"] = cantidad
                    bCantidadCambio = True
                
                
                guardar_inventario(productos)
                
                if bCantidadCambio:
                    registrar_evento(
                        sesion["usuario"], "modificar", "exitoso",
                        producto=identificador, anterior=anterior, nueva=cantidad
                    )
                    print("Cantidad actualizada.")
                    return True
                else:
                    registrar_evento(
                        sesion["usuario"], "modificar", "fallido",
                        producto=identificador, anterior=anterior, razon=razonCntNoCambio
                    )
                    print("Cantidad se quedo igual")
                    return False
            else:
                print("identificador inexistente")
                return False
        # TODO: informar identificador inexistente, sin crear productos. DONE
        return False
    else:
        return False


def main():
    print("Inventario académico — BASE CON DEBILIDADES")
    print("Estudiante:", input("Escriba su nombre: "))
    sesion = None
    while True:
        if sesion is None:
            nombre = input("Usuario (o salir): ")
            if nombre == "salir":
                break
            sesion = autenticar(nombre, input("Contraseña de prueba: "))
            continue
        print("1. Consultar | 2. Modificar | 3. Cerrar sesión | 0. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            consultar_inventario(sesion)
        elif opcion == "2":             
            identificador = input("ID del producto: ")
            entrada = input("Nueva cantidad: ")
            modificar_cantidad(sesion, identificador, entrada)
        elif opcion == "3":
            sesion = None
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
