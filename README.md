# Test Parrot - Proyecto Django REST API

Este es un proyecto backend que implementa una API RESTful utilizando Django y Django REST Framework. El proyecto maneja
la creación de órdenes, platos y usuarios, con funcionalidades para registrar usuarios con correo electrónico y generar
datos falsos para platos y usuarios.

## Instalación

### Requisitos previos

Asegúrate de tener instalados los siguientes programas:

- Python 3.10 o superior
- Django 4.x o superior
- Docker y Docker Compose (opcional, si deseas usar contenedores)

### Pasos para instalar

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/yasser1983-dev/test_parrot.git
   cd test_parrot
    ```
2. ** Configura un entorno virtual (opcional) **
    ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```
3. **Instala las dependencias**

   ```bash
   pip install -r requirements.txt
   ```
    4. **Configura las variables de entorno**
       Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables:

       DEBUG=True
       SECRET_KEY=tu_clave_secreta
       DB_NAME=nombre_base_datos
       DB_USER=usuario
       DB_PASSWORD=contraseña
       DB_HOST=localhost
       DB_PORT=5432
5. **Crea las migraciones y aplica las migraciones**

6. **Background Worker (django-rq)**

Este proyecto utiliza django-rq para ejecutar tareas en segundo plano mediante Redis.
Para que las tareas asincrónicas funcionen correctamente (impresión en consola del registro de órdenes),
es necesario ejecutar un worker.

```bash
  python manage.py rqworker
```

### Estructura del Proyecto

```bash
test_parrot/
│
├── manage.py                         # Script principal para tareas administrativas de Django
├── pytest.ini                        # Configuración para pytest
├── requirements.txt                  # Lista de dependencias del proyecto
├── .env                              # Variables de entorno para configuración local
├── README.md                         # Documentación principal del proyecto
│
├── dishes/                            # Aplicación encargada de la gestión de platillos
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py                     # Modelo de platillos
│   ├── serializers.py                # Serializadores para los platillos
│   ├── views.py                      # Vistas de la API de platillos
│   ├── urls.py                       # Rutas de platillos
│   ├── migrations/                   # Migraciones de platillos
│   └── user_services.py              # Lógica de negocio de platillos
│
├── parrot_api/                       # Configuración principal del proyecto Django
│   ├── __init__.py
│   ├── asgi.py                       # Configuración para servidores ASGI (asincrónicos)
│   ├── settings.py                   # Configuración global (apps instaladas, bases de datos, etc.)
│   ├── urls.py                       # Enrutamiento raíz del proyecto
│   └── wsgi.py                       # Configuración para servidores WSGI (sincrónicos)
│
├── sales/                            # Aplicación encargada de la gestión de ventas
│   ├── __init__.py
│   ├── admin.py                      # Configuración del panel admin para ventas
│   ├── models.py                     # Modelos de órdenes, etc.
│   ├── serializers.py                # Serializadores de ventas
│   ├── views.py                      # Vistas de la API de ventas
│   ├── urls.py                       # Rutas de ventas
│   ├── tasks.py                      # Tareas asincrónicas relacionadas con ventas
│   ├── migrations/                   # Archivos de migración
│   ├── order_factory.py              # Fábricas de entidades de ventas
│   └── sales_services.py             # Lógica de negocio de ventas
│
├── users/                            # Aplicación encargada de la gestión de usuarios
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py                     # Modelo de usuarios personalizado
│   ├── serializers.py                # Serializadores de usuario
│   ├── views.py                      # Vistas de usuario (login)
│   ├── urls.py                       # Rutas de usuarios
│   ├── migrations/                   # Migraciones de usuarios
│   └── user_services.py              # Lógica de negocio de usuarios
│
├── reports/                          # Aplicación para generar reportes
│   ├── __init__.py
│   ├── admin.py
│   ├── filters.py                    # Filtros para búsquedas avanzadas
│   ├── models.py                     # Modelos específicos de reportes
│   ├── serializers.py                # Serializadores para reportes
│   ├── views.py                      # Vistas para generación de reportes
│   ├── urls.py                       # Rutas para reportes
│   ├── migrations/                   # Migraciones de reportes
│   └── report_services.py            # Lógica de negocio para reportes

```

### Endpoints de la API

**Autenticación por Correo Electrónico (Token)**
Endpoint: POST /api/user/email-login/
Descripción: Inicia sesión utilizando un correo electrónico y contraseña.
Cuerpo de la solicitud:

```json
{
  "email": "usuario@example.com"
}
```

Respuesta exitosa:

```json
{
  "token": "token_de,_acceso",
 }
``` 

**Crear una orden**
Endpoint: POST /api/orders/

Descripción: Crea una nueva orden.

Cuerpo de la solicitud:

```json
{
  "customer_name": "Juan Pérez",
  "waiter": 1,
  "items": [
    {
      "dish": 1,
      "quantity": 2
    }
  ]
}
```

**Listar órdenes (Order)**

Endpoint: GET /api/orders/

    Descripción:  Obtiene una lista de todas las órdenes.
    
    Respuesta: 

```json
[
  {
    "id": 1,
    "customer_name": "Juan Pérez",
    "total_price": 31.00,
    "created_at": "2025-04-28T12:00:00",
    "items": [
      {
        "id": 1,
        "dish": {
          "id": 1,
          "name": "Plato de Ejemplo",
          "price": 15.50
        },
        "quantity": 2
      }
    ]
  }
]
```

**Generar reporte diarios (Order)**

Endpoint: GET /api/reports

Descripción:  Obtiene una lista de las órdenes por fechas de forma descendete.

Parámetros de consulta:

- `start_date`: Fecha de inicio (formato: YYYY-MM-DD)
- `end_date`: Fecha de fin (formato: YYYY-MM-DD)

Respuesta:

```json
[
    {
        "name": "Way",
        "total_quantity": 10,
        "total_price": "98.20"
    },
    {
        "name": "Level",
        "total_quantity": 2,
        "total_price": "12.76"
    }
]
``` 

### Generación de datos falsos

Para facilitar el llenado de la base de datos con datos de prueba, puedes utilizar un comando personalizado que crea
platos y usuarios falsos.

Ejecuta el siguiente comando para generar datos falsos:

```bash
  python manage.py generate_waiters_dishes
```

### Pruebas
Para ejecutar las pruebas, asegúrate de tener pytest instalado y ejecuta el siguiente comando:

```bash
  pytest
```

### Patrones de Diseño Utilizados

- **Modelo-Vista-Controlador (MVT)**:
  Estructura básica de Django que separa la lógica de negocio, la presentación y el acceso a datos.

- **Repository Pattern (Patrón Repositorio)**
  Se utiliza una capa de servicio o repositorio para encapsular la lógica de acceso a datos, separando las consultas
  complejas del controlador:
  OrderService**: Maneja la lógica de negocio relacionada con las órdenes.

- **Serializer Pattern (DRF)**:
  El uso de serializers en Django REST Framework es un claro ejemplo de este patrón, ya que permite transformar objetos
  complejos
  (modelos) en formatos legibles (JSON) y viceversa. Con el uso de los serializadores, se pueden validar y deserializar
  datos de entrada de manera eficiente.

- **Factory Pattern (Patrón Fábrica)**:
  Se utiliza para crear instancias de ordenes, Order.objects.create() y OrderItem.objects.create() y uso de la clase
  OrderFactory

- **Dependency Injection (Inyección de Dependencias)**:
  Se utiliza en la clase OrderSerializer, donde se inyecta el OrderFactory para la creación de órdenes y en la clase,
  tambièn en UserService y DailySalesReportService

- **Patrón de Asynchronous Processing (Procesamiento Asincrónico)**:

  Se utiliza django-rq para manejar tareas en segundo plano, como la impresión de registros de órdenes.
  Esto permite que el servidor maneje múltiples tareas sin bloquear el hilo principal.
  Este patrón se enfoca en procesar tareas largas o bloqueantes fuera del ciclo principal de la aplicación.

- **Patrón de Message Queue (Cola de Mensajes)**
  Utiliza Redis como backend para manejar tareas asincrónicas.
  Esto permite que las tareas se procesen en segundo plano y se manejen de manera eficiente.
  Este patrón es útil para desacoplar componentes y mejorar la escalabilidad de la aplicación.
-
- **Patrón de Decorador**:
  Se utiliza para agregar funcionalidad adicional para crear la tarea asíncron con @django_rq.job.

- **Patrón de Decoupling (Desacoplamiento)**
  Se utiliza para separar la lógica de negocio de la lógica de presentación.
  Esto se logra mediante el uso de servicios y serializadores, lo que permite una mejor mantenibilidad y escalabilidad
  del código.
  Usar Redis y tareas asincrónicas desacopla el procesamiento pesado o de larga duración de las vistas o controladores
  de Django.

- **Patrón de Task Queue Worker (Trabajador de Cola de Tareas)**
  Se utiliza django-rq para manejar tareas en segundo plano, como la impresión de registros de órdenes.

- **Patrón de Event-Driven Architecture (Arquitectura Basada en Eventos)**
  Se utiliza para manejar eventos como la creación de órdenes y la generación de reportes.
  Esto permite que la aplicación responda a eventos de manera eficiente y escalable.

- **Patrón de Filtros**:
  Se utiliza para filtrar las órdenes por fecha de creación y nombre del cliente en la vista de reportes.
  Esto permite una búsqueda más eficiente y específica de los datos.



