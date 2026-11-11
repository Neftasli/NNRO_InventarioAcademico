from seguridad import crear_hash
import json
from pathlib import Path


RAIZ = Path(__file__).resolve().parent
USUARIOS = RAIZ / "usuarios.json"

def main():
    usuarios = json.load(open(USUARIOS, encoding="utf-8"))
    #en el loop va por cada instancia de clave y la cambia por hash, mientras que esta hasheando la clave
    for usuario in usuarios:
        usuario["hash"] = crear_hash(usuario.pop("clave"))   
    USUARIOS.write_text(json.dumps(usuarios, indent=2), encoding="utf-8")
    print("clave migrada")

if __name__ == "__main__":
    main()
