# Manual Tecnico — RutaGT

**Universidad San Carlos de Guatemala**
**Facultad de Ingenieria — Escuela de Ciencias y Sistemas**
**Inteligencia Artificial 1 — Seccion A**

**Nombre:** Pablo Alejandro Marroquin Cutz

**Carne:** 202200214

**Practica:** 1 — Vacaciones del primer semestre 2026

---

## Descripcion General

RutaGT es un sistema hibrido de busqueda de rutas entre ciudades guatemaltecas. Utiliza Prolog (SWI-Prolog) como motor de inferencia logica para representar el conocimiento geografico y calcular rutas optimas, mientras que Python con FastAPI actua como capa de integracion entre la logica de Prolog y la interfaz web del usuario.

El sistema implementa el patron de arquitectura MVC (Model-View-Controller), separando claramente las responsabilidades de presentacion, logica de negocio y acceso a datos.

---

## Patron de Arquitectura: MVC

### Por que MVC?

MVC fue elegido porque permite separar tres responsabilidades claramente distintas dentro del sistema:

- Model: maneja la comunicacion con Prolog y el acceso a los datos geograficos
- View: presenta la informacion al usuario de forma visual e interactiva
- Controller: recibe las peticiones HTTP, las valida, las delega al Model y retorna las respuestas

Esta separacion facilita el mantenimiento, la escalabilidad y la comprension del codigo, ya que cada capa puede modificarse de forma independiente sin afectar a las demas. A diferencia de una arquitectura monolitica donde toda la logica esta en un solo lugar, MVC permite identificar rapidamente donde ocurre cada operacion del sistema.

### Diagrama de Arquitectura

```
+------------------------------------------------------------------+
|                          CLIENTE                                  |
|                     (Navegador Web)                               |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   |                       VIEW                                |   |
|   |                 views/index.html                          |   |
|   |            HTML + CSS + JavaScript puro                  |   |
|   |                                                           |   |
|   |   - Selectores de ciudades origen y destino              |   |
|   |   - Visualizacion de ruta optima y todas las rutas       |   |
|   |   - Panel de administracion con tabs                     |   |
|   |   - Barra de estadisticas                                |   |
|   |   - Mensajes de error y confirmacion                     |   |
|   +----------------------------+------------------------------+   |
+--------------------------------|----------------------------------+
                                 | fetch() HTTP REST
                                 |
                                 v
+------------------------------------------------------------------+
|                         SERVIDOR                                  |
|                    main.py  (FastAPI)                             |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   |                    CONTROLLER                             |   |
|   |           controllers/rutas_controller.py                 |   |
|   |                                                           |   |
|   |   GET  /api/ciudades                                      |   |
|   |   GET  /api/ruta-corta/{origen}/{destino}                 |   |
|   |   GET  /api/todas-rutas/{origen}/{destino}                |   |
|   |   POST /api/agregar-ciudad?nombre=X                       |   |
|   |   POST /api/agregar-conexion?origen=X&destino=Y&dist=Z    |   |
|   |                                                           |   |
|   |   Validaciones en controller:                             |   |
|   |   - strip(), lower(), replace() en entradas              |   |
|   |   - isalpha() para nombres de ciudades                    |   |
|   |   - Verificacion de duplicados                            |   |
|   |   - Verificacion de ciudades existentes                   |   |
|   |   - try/except en todos los endpoints                     |   |
|   +----------------------------+------------------------------+   |
|                                | llama a                          |
|                                v                                  |
|   +-----------------------------------------------------------+   |
|   |                      MODEL                                |   |
|   |              models/prolog_model.py                       |   |
|   |                                                           |   |
|   |   - Combina ciudades.pl + ciudades_aux.pl                 |   |
|   |   - Lanza subproceso swipl con el goal como argumento     |   |
|   |   - Captura stdout y parsea con expresiones regulares     |   |
|   |   - Escribe nuevas ciudades/conexiones en aux             |   |
|   |   - Verifica existencia de conexiones antes de agregar    |   |
|   +----------------------------+------------------------------+   |
+--------------------------------|----------------------------------+
                                 | subprocess swipl --quiet
                                 |
                                 v
+------------------------------------------------------------------+
|                        SWI-PROLOG                                 |
|                                                                   |
|   +------------------------+   +-----------------------------+   |
|   |   prolog/ciudades.pl   |   |   prolog/ciudades_aux.pl    |   |
|   |   Base de conocimiento |   |   Datos agregados           |   |
|   |   principal (fija)     |   |   dinamicamente             |   |
|   +------------------------+   +-----------------------------+   |
|                   |                          |                    |
|                   +------------+-------------+                    |
|                                |                                  |
|                                v                                  |
|                  prolog/ciudades_combined.pl                      |
|                  (generado en runtime antes de cada consulta)     |
|                                                                   |
|   Hechos:    ciudad/1, conexion/3                                 |
|   Reglas:    carretera/3, ruta/4, ruta_aux/5, ruta_mas_corta/4   |
+------------------------------------------------------------------+
```

### Flujo de una peticion completa

```
1. Usuario selecciona Guatemala y Jutiapa, presiona Calcular rutas
2. View ejecuta fetch("GET /api/todas-rutas/guatemala/jutiapa")
3. Controller recibe la peticion, aplica strip() y lower() a los parametros
4. Controller verifica que origen != destino
5. Controller llama a model.obtener_todas_rutas("guatemala", "jutiapa")
6. Model ejecuta _combinar(): une ciudades.pl y ciudades_aux.pl en ciudades_combined.pl
7. Model lanza: swipl --quiet -g "consult('ciudades_combined.pl')" -g "forall(ruta(...),...)" -g halt
8. SWI-Prolog carga el conocimiento, ejecuta las reglas y escribe en stdout
9. Model captura stdout, parsea con regex y ordena por distancia
10. Controller retorna JSON: {"codigo": 200, "rutas": [...]}
11. View renderiza las rutas con animaciones escalonadas
12. Si no hay rutas, View muestra mensaje "No existe ruta entre estas ciudades"
```

---

## Estructura del Proyecto

```
[IA1]_VACASJUN2026_PabloMarroquin_202200214/
|
+-- controllers/
|   +-- rutas_controller.py        # Endpoints HTTP y validaciones — capa Controller
|
+-- models/
|   +-- prolog_model.py            # Comunicacion con Prolog — capa Model
|
+-- views/
|   +-- index.html                 # Interfaz web — capa View
|
+-- prolog/
|   +-- ciudades.pl                # Base de conocimiento principal
|   +-- ciudades_aux.pl            # Hechos agregados dinamicamente
|   +-- ciudades_combined.pl       # Archivo unificado generado en runtime
|
+-- docs/
|   +-- MANUAL_USUARIO.md
|   +-- MANUAL_TECNICO.md
|
+-- .venv/                         # Entorno virtual Python
+-- main.py                        # Punto de entrada FastAPI
+-- README.md
```

---

## Descripcion de Componentes

### 1. Base de Conocimiento Prolog

#### prolog/ciudades.pl

Contiene los hechos y reglas permanentes del sistema. Las directivas discontiguous evitan warnings cuando hechos del mismo tipo aparecen separados en el archivo:

```prolog
:- discontiguous ciudad/1.
:- discontiguous conexion/3.

ciudad(guatemala).
ciudad(escuintla).

conexion(guatemala, escuintla, 58).

carretera(X, Y, D) :- conexion(X, Y, D).
carretera(X, Y, D) :- conexion(Y, X, D).

ruta(Origen, Destino, Ruta, Distancia) :-
    ruta_aux(Origen, Destino, [Origen], Ruta, Distancia).

ruta_aux(Destino, Destino, Visitados, Visitados, 0).

ruta_aux(Actual, Destino, Visitados, Ruta, Distancia) :-
    carretera(Actual, Siguiente, D1),
    \+ member(Siguiente, Visitados),
    ruta_aux(Siguiente, Destino, [Siguiente|Visitados], RestoRuta, D2),
    Distancia is D1 + D2,
    Ruta = RestoRuta.

ruta_mas_corta(Origen, Destino, MejorRuta, MejorDist) :-
    findall(D-R, ruta(Origen, Destino, R, D), Rutas),
    Rutas \= [],
    min_member(MejorDist-MejorRuta, Rutas).
```

#### prolog/ciudades_aux.pl

Archivo de escritura dinamica donde se persisten las ciudades y conexiones que el usuario agrega en tiempo de ejecucion. Se inicializa con directivas discontiguous para evitar warnings de Prolog cuando los hechos del mismo tipo no estan agrupados.

#### prolog/ciudades_combined.pl

Generado automaticamente por el Model antes de cada consulta. Une el contenido de ciudades.pl y ciudades_aux.pl eliminando directivas discontiguous duplicadas, garantizando que Prolog vea todos los hechos en un solo modulo coherente.

---

### 2. Model — models/prolog_model.py

Es el componente central del sistema. Actua como puente entre Python y SWI-Prolog.

#### Estrategia de integracion: subprocess

La comunicacion con Prolog se realiza a traves de subprocesos del sistema operativo en lugar de la libreria PySwip. Esta decision fue tomada porque PySwip presenta un bug conocido (NestedQueryError) cuando opera dentro del entorno de threads de FastAPI, causando que las peticiones se bloqueen indefinidamente.

Con subprocess, cada consulta es completamente independiente y no comparte estado con otras:

```python
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
```

#### Verificacion de conexiones duplicadas

Antes de agregar una conexion nueva, el Model consulta a Prolog si ya existe en cualquier direccion:

```python
def existe_conexion(self, origen: str, destino: str) -> bool:
    goal = f"(conexion({origen},{destino},_) ; conexion({destino},{origen},_)), write(si)"
    salida = self._consultar(goal)
    return "si" in salida
```

---

### 3. Controller — controllers/rutas_controller.py

Define los endpoints de la API REST e implementa tres niveles de validacion antes de llamar al Model:

**Normalizacion de entrada:**
```python
nombre = nombre.strip().lower().replace(" ", "")
```
- strip() elimina espacios al inicio y al final
- lower() convierte todo a minusculas
- replace() elimina espacios internos

**Validacion de formato:**
```python
if not nombre.isalpha():
    return {"codigo": 400, "error": "Solo letras sin espacios ni tildes"}
```
isalpha() retorna False si el texto contiene espacios, numeros, tildes o cualquier caracter especial.

**Validacion de negocio:**
- Verificacion de que las ciudades existen antes de agregar conexiones
- Verificacion de conexiones duplicadas en ambas direcciones
- Verificacion de que origen y destino sean distintos

#### Tabla de endpoints

| Metodo | Endpoint | Descripcion | Respuesta exitosa |
|--------|----------|-------------|-------------------|
| GET | /api/ciudades | Lista todas las ciudades | {"ciudades": [...]} |
| GET | /api/ruta-corta/{origen}/{destino} | Ruta mas corta | {"codigo": 200, "resultado": {"ruta": [...], "distancia": N}} |
| GET | /api/todas-rutas/{origen}/{destino} | Todas las rutas ordenadas | {"codigo": 200, "rutas": [...]} |
| POST | /api/agregar-ciudad?nombre=X | Agrega ciudad nueva | {"codigo": 200, "mensaje": "..."} |
| POST | /api/agregar-conexion?origen=X&destino=Y&distancia=Z | Agrega conexion | {"codigo": 200, "mensaje": "..."} |

---

### 4. View — views/index.html

Interfaz web en HTML, CSS y JavaScript puro sin frameworks externos. Se comunica con el backend mediante fetch() a la API REST.

Caracteristicas tecnicas:
- Tipografia: Playfair Display para titulos, DM Sans para cuerpo, via Google Fonts
- Diseno: estetica editorial con paleta tinta, papel y dorado
- Animaciones: CSS keyframes con animation-delay escalonado para la entrada de resultados
- Estado: mantenido en variables JavaScript en memoria durante la sesion
- Carga inicial: cargarCiudades() puebla los selectores dinamicamente al abrir la pagina
- Manejo de errores: mensajes visuales rojos para errores, verdes para confirmaciones

---

### 5. Main — main.py

Punto de entrada de la aplicacion FastAPI. Instancia el Model, registra el Controller bajo el prefijo /api y sirve el frontend estatico:

```python
app = FastAPI(title="Rutas entre Ciudades - Guatemala")
model = PrologModel()
router = build_router(model)
app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory="views"), name="static")

@app.get("/")
def index():
    return FileResponse("views/index.html")
```

---

## Logica de Prolog Explicada

### Prevencion de ciclos

La regla ruta_aux mantiene una lista Visitados que acumula las ciudades ya recorridas. El operador `\+ member` garantiza que Prolog no vuelva a visitar una ciudad que ya esta en el camino actual:

```prolog
ruta_aux(Actual, Destino, Visitados, Ruta, Distancia) :-
    carretera(Actual, Siguiente, D1),
    \+ member(Siguiente, Visitados),
    ruta_aux(Siguiente, Destino, [Siguiente|Visitados], RestoRuta, D2),
    Distancia is D1 + D2,
    Ruta = RestoRuta.
```

### Busqueda de ruta mas corta

findall/3 recolecta todas las rutas posibles con sus distancias, y min_member/2 selecciona el par de menor valor:

```prolog
ruta_mas_corta(Origen, Destino, MejorRuta, MejorDist) :-
    findall(D-R, ruta(Origen, Destino, R, D), Rutas),
    Rutas \= [],
    min_member(MejorDist-MejorRuta, Rutas).
```

### Bidireccionalidad

Las conexiones se definen en una sola direccion pero la regla carretera/3 las hace transitables en ambas:

```prolog
carretera(X, Y, D) :- conexion(X, Y, D).
carretera(X, Y, D) :- conexion(Y, X, D).
```

---

## Manejo de Errores

El sistema implementa tres capas de manejo de errores:

**Capa View — validacion en cliente:**
- Validacion de formularios antes de enviar la peticion al servidor
- try/catch en todas las llamadas fetch()
- Mensajes visuales de error en rojo y confirmacion en verde
- Mensaje claro cuando no existe ruta entre dos ciudades

**Capa Controller — validacion de entrada:**
- Normalizacion automatica con strip(), lower() y replace()
- isalpha() rechaza tildes, espacios, numeros y caracteres especiales
- Verificacion de existencia de ciudades antes de agregar conexiones
- Verificacion de conexiones duplicadas en ambas direcciones
- try/except en todos los endpoints retorna codigo 500 con mensaje descriptivo

**Capa Model — errores de Prolog:**
- timeout=15 en subprocess.run evita que consultas largas bloqueen el servidor
- Retorno de None cuando Prolog no encuentra resultados, manejado en el Controller

---


## Dependencias

| Libreria   | Version  | Uso |
|------------|----------|-----|
| fastapi    | 0.136.x  | Framework web y definicion de la API REST |
| uvicorn    | 0.49.x   | Servidor ASGI para correr FastAPI |
| pyswip     | 0.3.x    | Instalada como dependencia, no usada en produccion |
| SWI-Prolog | 10.0.2   | Motor de inferencia logica, invocado via subprocess |

---

## Decisiones de Diseno

| Decision | Alternativa considerada | Razon de la eleccion |
|---|---|---|
| subprocess para Prolog | PySwip directo | PySwip causa NestedQueryError con threads de FastAPI |
| Archivo combinado en runtime | Dos consult() separados | Prolog trata predicados de archivos distintos como modulos separados |
| HTML/JS puro en el frontend | React o Vue | Menor complejidad, sin build tools, mas facil de servir con FastAPI |
| FastAPI | Flask o Django | Documentacion automatica, tipado con Pydantic, mejor rendimiento |
| ciudades_aux.pl separado | Escribir en ciudades.pl | Mantiene la base de conocimiento original intacta |
| Patron MVC | Monolitico | Separacion clara de responsabilidades, facilita mantenimiento |