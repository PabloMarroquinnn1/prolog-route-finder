import subprocess
import re
from pathlib import Path

class PrologModel:
    def __init__(self):
        self.archivo_pl = Path("prolog/ciudades.pl").resolve()
        self.archivo_aux = Path("prolog/ciudades_aux.pl").resolve()
        self.archivo_combinado = Path("prolog/ciudades_combined.pl").resolve()
        self._combinar()

    def _combinar(self):
        contenido_principal = self.archivo_pl.read_text(encoding="utf-8")
        contenido_aux = ""
        if self.archivo_aux.exists() and self.archivo_aux.stat().st_size > 0:
            contenido_aux = self.archivo_aux.read_text(encoding="utf-8")
            # Quitar las directivas duplicadas del auxiliar
            contenido_aux = "\n".join([
                l for l in contenido_aux.split("\n")
                if not l.startswith(":- discontiguous")
            ])
        with open(self.archivo_combinado, "w", encoding="utf-8") as f:
            f.write(contenido_principal)
            f.write("\n")
            f.write(contenido_aux)

    def _consultar(self, goal: str) -> str:
        self._combinar()
        archivo = self.archivo_combinado.as_posix()
        cmd = [
            "swipl",
            "--quiet",
            "-g", f"consult('{archivo}')",
            "-g", goal,
            "-g", "halt"
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return resultado.stdout

    def obtener_ciudades(self):
        goal = "findall(X,ciudad(X),Xs),maplist(writeln,Xs)"
        salida = self._consultar(goal)
        return [c.strip() for c in salida.strip().split("\n") if c.strip()]

    def obtener_ruta_mas_corta(self, origen: str, destino: str):
        goal = f"ruta_mas_corta({origen},{destino},Ruta,Dist),writeln(dist:Dist),writeln(ruta:Ruta)"
        salida = self._consultar(goal)
        try:
            dist = int(re.search(r"dist:(\d+)", salida).group(1))
            ruta_str = re.search(r"ruta:\[(.+)\]", salida).group(1)
            ruta = [c.strip() for c in ruta_str.split(",")]
            ruta.reverse()
            return {"ruta": ruta, "distancia": dist}
        except:
            return None

    def obtener_todas_rutas(self, origen: str, destino: str):
        goal = f"forall(ruta({origen},{destino},R,D),(writeln(dist:D),writeln(ruta:R)))"
        salida = self._consultar(goal)
        rutas = []
        lineas = salida.strip().split("\n")
        i = 0
        while i < len(lineas) - 1:
            try:
                dist = int(re.search(r"dist:(\d+)", lineas[i]).group(1))
                ruta_str = re.search(r"ruta:\[(.+)\]", lineas[i+1]).group(1)
                ruta = [c.strip() for c in ruta_str.split(",")]
                ruta.reverse()
                rutas.append({"ruta": ruta, "distancia": dist})
                i += 2
            except:
                i += 1
        return sorted(rutas, key=lambda x: x["distancia"])

    def _inicializar_aux(self):
        if not self.archivo_aux.exists() or self.archivo_aux.stat().st_size == 0:
            with open(self.archivo_aux, "w", encoding="utf-8") as f:
                f.write(":- discontiguous ciudad/1.\n")
                f.write(":- discontiguous conexion/3.\n")

    def agregar_ciudad(self, ciudad: str):
        self._inicializar_aux()
        with open(self.archivo_aux, "a", encoding="utf-8") as f:
            f.write(f"\nciudad({ciudad}).")

    def agregar_conexion(self, origen: str, destino: str, distancia: int):
        self._inicializar_aux()
        with open(self.archivo_aux, "a", encoding="utf-8") as f:
            f.write(f"\nconexion({origen}, {destino}, {distancia}).")

    def existe_conexion(self, origen: str, destino: str) -> bool:
        goal = f"(conexion({origen},{destino},_) ; conexion({destino},{origen},_)), write(si)"
        salida = self._consultar(goal)
        return "si" in salida