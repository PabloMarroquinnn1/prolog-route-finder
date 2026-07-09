# RutaGT — Prolog Route Finder

Sistema híbrido de búsqueda de rutas entre ciudades guatemaltecas. Utiliza SWI-Prolog como motor de inferencia lógica para representar el conocimiento geográfico y calcular rutas óptimas, con FastAPI como backend y una interfaz web interactiva.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Motor de inferencia | SWI-Prolog |
| Backend / API | Python + FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Integración Prolog | pyswip |

## Arquitectura (MVC)

```
┌─────────────────────────────────────┐
│            Vista (View)             │
│         views/index.html            │
│  Selectores de ciudades, mapa de    │
│  rutas, panel de administración     │
└──────────────┬──────────────────────┘
               │ HTTP (fetch)
┌──────────────▼──────────────────────┐
│        Controlador (Controller)     │
│    controllers/rutas_controller.py  │
│  Endpoints REST: /api/rutas,        │
│  /api/ciudades, /api/ruta-optima    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│          Modelo (Model)             │
│      models/prolog_model.py         │
│  Comunicación con SWI-Prolog        │
│  via pyswip                         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│          SWI-Prolog                 │
│     prolog/ciudades_combined.pl     │
│  Hechos geográficos + reglas de     │
│  búsqueda de rutas                  │
└─────────────────────────────────────┘
```

## Características

- **Ruta óptima:** Calcula la ruta más corta entre dos ciudades usando inferencia lógica en Prolog
- **Todas las rutas:** Muestra todas las rutas posibles entre dos puntos con sus distancias
- **Panel de administración:** Agregar/eliminar ciudades y conexiones desde la interfaz web
- **Visualización interactiva:** Interfaz con selectores, estadísticas y resultados en tiempo real
- **Base de conocimiento Prolog:** Representación declarativa de ciudades y carreteras de Guatemala

## Instalación

### Requisitos

- Python 3.10+
- SWI-Prolog instalado y en el PATH

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar

```bash
uvicorn main:app --reload
```

La interfaz estará disponible en `http://localhost:8000`.

## Estructura del proyecto

```
├── main.py                        # Entry point FastAPI
├── requirements.txt               # Dependencias Python
├── controllers/
│   └── rutas_controller.py        # Endpoints REST
├── models/
│   └── prolog_model.py            # Integración con SWI-Prolog
├── prolog/
│   ├── ciudades.pl                # Hechos base de ciudades
│   ├── ciudades_aux.pl            # Ciudades agregadas dinámicamente
│   └── ciudades_combined.pl       # Unificador (base + dinámico)
├── views/
│   └── index.html                 # Interfaz web interactiva
└── docs/
    ├── ManualTecnico.md           # Documentación técnica
    └── ManualUsuario              # Guía de uso
```

## Documentación

- [Manual Técnico](docs/ManualTecnico.md) — Arquitectura MVC, modelo Prolog, endpoints
- [Manual de Usuario](docs/ManualUsuario) — Instalación y guía paso a paso

## Autor

**Pablo Alejandro Marroquin Cutz**
