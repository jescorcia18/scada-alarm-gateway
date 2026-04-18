# SCADA Alarm Gateway & Migrator

Prueba técnica – Procesamiento de datos SCADA y exposición vía API

## Descripción

Este proyecto implementa una solución para la ingesta, limpieza, normalización y exposición de datos de alarmas provenientes de sistemas SCADA en formatos legacy (CSV/JSON).

El sistema permite:

* Procesar datos inconsistentes (fechas, nulos, tipos incorrectos)
* Normalizar y almacenar la información en una base de datos relacional
* Exponer una API REST para consulta y análisis de alarmas

---
## Arquitectura de la solución

```text
[Dataset sucio CSV]
        ↓
[ETL - Python (Pandas)]
        ↓
[Base de Datos (PostgreSQL / SQLite)]
        ↓
[API REST (FastAPI)]
```

---
## Tecnologías utilizadas

* Python 3.11+
* FastAPI
* SQLAlchemy (ORM)
* Pandas (procesamiento de datos)
* PostgreSQL (o SQLite como alternativa)
* Docker (opcional)

---
## Estructura del proyecto

```text
scada-project/
│
├── app/
│   ├── main.py
│   ├── db/
│   ├── models/
│   
│
├── etl/
│   ├── generator.py
│   ├── cleaner.py
│   └── loader.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── requirements.txt
└── docker-compose.yml
```

---
## Ejecución del proyecto

### 1. Clonar repositorio

```bash
git clone <repo_url>
cd scada-project
```
---

### 2. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Configuración de base de datos

### Opción A — PostgreSQL con Docker

```bash
docker-compose up -d
```

---

## Pipeline ETL

### 1. Generar dataset (datos sucios)

```bash
python etl/generator.py
```

Genera:

```text
data/raw/alarms_dirty.csv
```

Incluye:

* fechas inconsistentes
* valores nulos
* tipos incorrectos

---

### 2. Limpiar datos

```bash
python etl/cleaner.py
```

Aplica:

* normalización de fechas
* validación de severidad
* eliminación de registros inválidos

Salida:

```text
data/processed/clean.csv
```

---

### 3. Cargar a base de datos

```bash
python etl/loader.py
```

---

## Ejecución de la API

```bash
uvicorn app.main:app --reload
```

Acceder a documentación interactiva:

```text
http://localhost:8000/docs
```

---

## Endpoints

### Obtener alarmas con filtros

```http
GET /alarms
```

#### Parámetros:

* `start_date` (ISO datetime)
* `end_date` (ISO datetime)
* `severity`
* `tag`
* `limit`
* `offset`

#### Ejemplo:

```http
/alarms?severity=HIGH&tag=PUMP_01
```

---

### Top tags (agregación)

```http
GET /alarms/top-tags
```

Ejemplo:

```http
/alarms/top-tags?limit=5
```

---

### Conteo por severidad

```http
GET /alarms/by-severity
```

---

## Decisiones técnicas

### Uso de Pandas para ETL

Permite procesamiento vectorizado eficiente y manejo robusto de datos inconsistentes.

### FastAPI

Se eligió por:

* alto rendimiento
* validación automática
* documentación integrada (Swagger)

### SQLAlchemy

Permite abstracción del acceso a datos y portabilidad entre motores.

### Modelo relacional

Optimizado para consultas por:

* tiempo (timestamp)
* criticidad (severity)
* tag

---

## Supuestos realizados

* Registros sin `timestamp` o `tag` son descartados
* Valores inválidos en `severity` se normalizan a `LOW`
* Valores no numéricos en `value` se convierten a `NULL`

---

## Consideraciones de escalabilidad

* Uso de paginación en endpoints
* Posibilidad de agregar índices en:

  * `timestamp`
  * `severity`
  * `tag`
* Carga de datos en batch (evitando inserts fila a fila)

---

## Pruebas

Se validaron:

* datos con fechas inválidas
* valores nulos
* filtros combinados en API
* agregaciones

---

## Seguridad (básico)

* Validación de parámetros de entrada
* Manejo de errores con HTTPException

---

## Mejoras futuras

* Implementación de migraciones (Alembic)
* Autenticación (JWT)
* Frontend para visualización
* Procesamiento en tiempo real (streaming)

---

## Autor

Desarrollado como prueba técnica para evaluación de capacidades en procesamiento de datos, backend y diseño de APIs.

Juan Escorcia Rudas
18/04/2026
