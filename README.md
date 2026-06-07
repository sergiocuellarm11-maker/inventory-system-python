# 🛒 Sistema de Control de Inventario Web con SQL (Flask)

Una aplicación web moderna, ligera y robusta desarrollada en **Python** utilizando el microframework **Flask** y **SQLite3** como motor de base de datos. Esta versión migra la lógica de consola anterior a una interfaz gráfica de usuario (GUI) basada en navegador, incorporando un sistema dinámico de alertas y un módulo avanzado de exportación de reportes.

---

## 🚀 Características y Funcionalidades

* **Diseño Web Responsivo (Flexbox):** Interfaz limpia y estilizada con tarjetas independientes para la gestión de productos y tablas organizadas mediante CSS nativo.
* **Operaciones CRUD Completas con SQL:**
  * **Agregar:** Inserción segura de productos controlando duplicados (`UNIQUE constraint`).
  * **Actualizar:** Modificación en tiempo real de precios y existencias con recalculado automático de totales del inventario.
  * **Eliminar:** Remoción de registros del sistema mediante parámetros dinámicos con ventanas nativas de confirmación en el navegador.
* **Control de Errores y Seguridad (Try/Except/Finally):** Gestión segura de conexiones SQL para prevenir la corrupción de datos y blindaje de rutas mediante el método seguro **POST**.
* **Sistema de Notificaciones Flash:** Alertas de color dinámico (verde para éxito / rojo para peligro) inyectadas directamente en el flujo HTML con Jinja2.
* **Módulo de Exportación Multiformato (RAM-on-the-fly):** Generación de reportes inmediatos en la memoria RAM del servidor sin generar almacenamiento basura:
  * 📄 **TXT:** Reporte estructurado en texto plano alineado con tabuladores tipográficos.
  * 📊 **CSV:** Archivo nativo de Excel delimitado por comas, listo para análisis financiero.
  * ⚙️ **JSON:** Estructura jerárquica de diccionarios, ideal para integraciones o futuras API REST.

---

## 🛠️ Arquitectura del Proyecto

El proyecto sigue la estructura jerárquica oficial recomendada por la comunidad de Flask:

```text
PROYECTOS/
│
├── inventario.py        # Servidor backend de Flask, rutas y lógica SQL
├── .gitignore           # Archivo de exclusión para evitar subir datos locales
├── README.md            # Documentación oficial del repositorio (este archivo)
└── templates/           # Carpeta contenedora de vistas HTML
    └── inventario.html  # Plantilla web del frontend armada con Jinja2

👨‍💻 Autor

Sergio Cuellar Mendoza

