# BufetePDFReader-backend

Backend del proyecto de servicio social para el Bufete Estudiantil.

## Descripción

Este proyecto proporciona servicios backend para la aplicación de lectura, extracción de datos y colocación de información extraída desde archivos PDF. Forma parte del proyecto de servicio social en el Bufete Estudiantil de la Facultad de Ingeniería de la Universidad Autónoma de Sinaloa, Unidad Regional Norte.

## Configuración del Entorno

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- virtualenv (opcional, pero recomendado)

### Pasos de Instalación

1. **Crear Entorno Virtual** Crea un entorno virtual para aislar las dependencias del proyecto.

   ```bash
   python -m venv env
   ```

2. **Activar Entorno Virtual**

   - En Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source env/bin/activate
     ```

3. **Instalar Dependencias** Instala las dependencias necesarias para el proyecto.

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del Proyecto

Para iniciar el servidor backend, utiliza el siguiente comando:

```bash
uvicorn app.main:app --reload
```

Esto iniciará el servidor en modo desarrollo y estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Estructura del Proyecto

El backend está desarrollado con FastAPI y sigue una estructura modular para mantener el código organizado y fácil de mantener.

- `app/`: Contiene el código fuente principal.
  - `main.py`: Punto de entrada de la aplicación.
  - `routes/`: Contiene los endpoints de la API.
  - `services/`: Lógica de negocio y servicios de extracción de datos.
  - `models/`: Definición de los modelos de datos utilizados por la aplicación, generalmente para interactuar con la base de datos.
  - `schemas/`: Esquemas de datos definidos mediante Pydantic para validar las solicitudes y respuestas de la API.
  - `middlewares/`: Contiene lógica que se ejecuta entre las solicitudes y las respuestas, como la gestión de errores o autenticación.
  - `utils/`: Funciones auxiliares y utilidades reutilizables en todo el proyecto.
  - `config/`: Configuraciones globales del proyecto, como variables de entorno y configuraciones de la base de datos.

## Contribuciones

Este proyecto está abierto a contribuciones. Si deseas colaborar, sigue estos pasos:

1. Realiza un fork del repositorio.
2. Crea una rama para tu funcionalidad o corrección de errores.
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza los cambios y haz commit.
   ```bash
   git commit -m "Descripción de los cambios"
   ```
4. Sube los cambios a tu repositorio.
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Crea un Pull Request hacia el repositorio principal.

## Licencia

Este proyecto está licenciado bajo los términos de la [GNU General Public License v3.0](LICENSE).

## Contacto

Para preguntas o comentarios sobre el proyecto, puedes contactar al equipo del Bufete Estudiantil de la Facultad de Ingeniería de la Universidad Autónoma de Sinaloa, Unidad Regional Norte.



