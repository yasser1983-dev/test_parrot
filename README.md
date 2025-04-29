# Test Parrot - Proyecto Django REST API

Este es un proyecto backend que implementa una API RESTful utilizando Django y Django REST Framework. El proyecto maneja la creación de órdenes, platos y usuarios, con funcionalidades para registrar usuarios con correo electrónico y generar datos falsos para platos y usuarios.

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

### Estructura del Proyecto
```bash
test_parrot/
│
├── parrot_api/                      # Configuración general del proyecto Django
│   ├── __init__.py                   # Inicialización del proyecto
│   ├── asgi.py                       # Configuración para ASGI (servidor asíncrono)
│   ├── settings.py                   # Configuración principal del proyecto (bases de datos, apps, etc.)
│   ├── urls.py                       # Rutas globales del proyecto
│   ├── wsgi.py                       # Configuración para WSGI (servidor tradicional)
│   ├── core/                         # Lógica común para el proyecto
│   │   ├── __init__.py               # Inicialización del módulo
│   │   ├── models.py                 # Modelos generales, si es necesario
│   │   ├── serializers.py            # Serializadores comunes (autenticación, usuarios, etc.)
│   │   ├── permissions.py            # Permisos y lógica compartida
│   │   └── utils.py                  # Funciones auxiliares comunes
│
├── sales/                            # Aplicación encargada de gestionar ventas (platos, órdenes, etc.)
│   ├── migrations/                   # Migraciones automáticas de base de datos para ventas
│   ├── __init__.py                   # Inicialización del módulo
│   ├── models.py                     # Modelos de base de datos para ventas
│   ├── serializers.py                # Serializadores para los modelos de ventas
│   ├── views.py                      # Vistas de la API para ventas
│   ├── urls.py                       # Rutas específicas para el módulo de ventas
│   ├── admin.py                      # Configuración de admin para ventas
│   └── tests/                        # Pruebas unitarias del módulo de ventas
│       ├── __init__.py               # Inicialización de pruebas
│       ├── test_views.py             # Pruebas para vistas
│       └── test_serializers.py       # Pruebas para serializadores
│
├── users/                            # Aplicación encargada de la gestión de usuarios
│   ├── migrations/                   # Migraciones automáticas de base de datos para usuarios
│   ├── __init__.py                   # Inicialización del módulo
│   ├── models.py                     # Modelos de base de datos para usuarios
│   ├── serializers.py                # Serializadores para el modelo de usuarios
│   ├── views.py                      # Vistas de la API para usuarios
│   ├── urls.py                       # Rutas específicas para el módulo de usuarios
│   ├── admin.py                      # Configuración de admin para usuarios
│   └── tests/                        # Pruebas unitarias del módulo de usuarios
│       ├── __init__.py               # Inicialización de pruebas
│       ├── test_views.py             # Pruebas para vistas de usuarios
│       └── test_serializers.py       # Pruebas para serializadores de usuarios
│
├── sales_reports/                    # Aplicación encargada de los reportes de ventas
│   ├── migrations/                   # Migraciones automáticas para los reportes
│   ├── __init__.py                   # Inicialización del módulo
│   ├── models.py                     # Modelos específicos para los reportes
│   ├── serializers.py                # Serializadores para los reportes
│   ├── views.py                      # Vistas para generar reportes
│   ├── urls.py                       # Rutas específicas para el módulo de reportes
│   └── tests/                        # Pruebas unitarias del módulo de reportes
│       ├── __init__.py               # Inicialización de pruebas
│       ├── test_views.py             # Pruebas para vistas de reportes
│       └── test_serializers.py       # Pruebas para serializadores de reportes
│
├── manage.py                         # Script para administrar el proyecto (migraciones, servidor, etc.)
├── requirements.txt                  # Listado de dependencias Python del proyecto
├── .env                               # Variables de entorno para configuración segura
└── README.md                         # Documentación principal del proyecto

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
Para facilitar el llenado de la base de datos con datos de prueba, puedes utilizar un comando personalizado que crea platos y usuarios falsos.

Ejecuta el siguiente comando para generar datos falsos:

```bash
  python manage.py populate_data
```

### Patrones de Diseño Utilizados

- **Modelo-Vista-Controlador (MVT)**: 
    Estructura básica de Django que separa la lógica de negocio, la presentación y el acceso a datos.

- **Repository Pattern (Patrón Repositorio)**
 Se utiliza una capa de servicio o repositorio para encapsular la lógica de acceso a datos, separando las consultas complejas del controlador: 
 OrderService**: Maneja la lógica de negocio relacionada con las órdenes.

- **Serializer Pattern (DRF)**: 
    El uso de serializers en Django REST Framework es un claro ejemplo de este patrón, ya que permite transformar objetos complejos 
    (modelos) en formatos legibles (JSON) y viceversa. Con el uso de los serializadores, se pueden validar y deserializar datos de entrada de manera eficiente.

- **Factory Pattern (Patrón Fábrica)**:
    Se utiliza para crear instancias de ordenes, Order.objects.create() y OrderItem.objects.create() y uso de la clase OrderFactory

- **Dependency Injection (Inyección de Dependencias)**:
    Se utiliza en la clase OrderSerializer, donde se inyecta el OrderFactory para la creación de órdenes y en la clase, tambièn en UserService y DailySalesReportService
