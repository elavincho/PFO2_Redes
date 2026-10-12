# PFO 2 - Sistema de Gestión de Tareas con API y Base de Datos

API REST desarrollada con **Flask** y **SQLite** para registrar usuarios, iniciar
sesión y consultar tareas. Incluye un **cliente de consola** en Python que
interactúa con la API.

---

## Instalación

```bash
git clone https://github.com/<tu-usuario>/pfo2-tareas.git
cd pfo2-tareas
python -m venv venv
Activar el entorno virtual:

Windows (PowerShell): .\venv\Scripts\Activate.ps1

Windows (CMD): venv\Scripts\activate.bat

macOS / Linux: source venv/bin/activate

## Instalar depencencias:

pip install flask requests


## Ejecución

1. Levantar el servidor:

python servidor.py

Se inicia en http://127.0.0.1:5000.

2. En otra terminal (con el venv activado), ejecutar el cliente:

python cliente.py

# Registro
curl -X POST http://127.0.0.1:5000/registro \
  -H "Content-Type: application/json" \
  -d '{"usuario":"ana","contraseña":"1234"}'

# Login
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"ana","contraseña":"1234"}'

# Página pública
curl http://127.0.0.1:5000/tareas


## Estructura del proyecto

pfo2-tareas/
├── servidor.py        # API Flask + SQLite
├── cliente.py         # Cliente de consola
├── tareas.db          # Base de datos (se genera automáticamente)
├── requirements.txt
└── README.md


## Respuestas conceptuales

❓ ¿Por qué hashear contraseñas?
Hashear las contraseñas es una práctica fundamental de seguridad al
construir cualquier sistema que gestione credenciales. Las razones principales
son:

Evita almacenar datos sensibles en texto plano.
Si la base de datos es robada, filtrada o mal compartida, un atacante no
obtiene las contraseñas reales de los usuarios. Solo ve cadenas de hash
ilegibles e irreversibles.

Protege a los usuarios que reutilizan contraseñas.
Muchas personas usan la misma contraseña para el correo, el banco o redes
sociales. Si un sistema la guarda en texto plano y se filtra, compromete
todos los demás servicios del usuario.

El hash es una función unidireccional.
A diferencia del cifrado (que se puede descifrar con una clave), un hash
no se puede revertir matemáticamente. No existe forma práctica de
obtener la contraseña original a partir del hash.

Uso automático de salt.
Librerías como Werkzeug (generate_password_hash) aplican un salt
aleatorio a cada contraseña antes de hashearla. Esto significa que dos
usuarios con la misma contraseña obtienen hashes completamente distintos,
lo que impide ataques de tablas precalculadas (rainbow tables).

Verificación sin conocer la contraseña.
El servidor nunca necesita "saber" la contraseña original. Solo compara el
hash recién calculado con el almacenado usando check_password_hash(). La
contraseña real nunca toca el disco ni la base de datos.

Cumplimiento normativo.
Regulaciones como GDPR (Europa) o Ley de Protección de Datos
Personales (Argentina) exigen medidas de seguridad razonables para datos
sensibles, y el hasheo de contraseñas es una de ellas.

🔐 Conclusión: hashear contraseñas no es opcional, es un requisito mínimo
de cualquier sistema que se tome en serio la seguridad de sus usuarios.

❓ Ventajas de usar SQLite en este proyecto
SQLite es una base de datos embebida, sin servidor, que se guarda en un
único archivo. Para un PFO como este, ofrece ventajas claras:

Cero configuración.
No hace falta instalar, administrar ni levantar un servidor de base de
datos (como MySQL o PostgreSQL). Simplemente se usa el módulo sqlite3 que
ya viene incluido en Python.

Portabilidad total.
Toda la base de datos es un solo archivo (tareas.db). Se puede
copiar, mover, respaldar o versionar fácilmente entre equipos.

Ideal para desarrollo, prototipado y proyectos pequeños.
Para un sistema de tareas con pocos usuarios concurrentes, SQLite es más
que suficiente y evita la sobrecarga de un motor cliente-servidor.

Sin dependencias externas.
No requiere instalar controladores, ni configurar usuarios, puertos o
permisos del motor. Todo funciona "out of the box".

Soporta SQL estándar.
Permite JOIN, claves foráneas, UNIQUE, transacciones, AUTOINCREMENT,
etc. Lo que aprendes con SQLite es directamente aplicable a otros motores.

Rápida para lecturas.
Al ser un archivo local, las lecturas son muy veloces y sin latencia de red.

Integración nativa con Python.
El módulo sqlite3 viene en la biblioteca estándar, así que el código es
simple, limpio y sin capas extra.

⚠️ Limitación a tener en cuenta: SQLite no está pensado para alta
concurrencia de escritura. Si el proyecto creciera a cientos de usuarios
simultáneos escribiendo, convendría migrar a PostgreSQL o MySQL. Para un PFO
académico, es la elección ideal.

##  Capturas de pantalla

captura 1
captura 2