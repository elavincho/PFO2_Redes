from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "tareas.db"


# ---------- Utilidades de BD ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            completada INTEGER DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Helper: ¿la petición viene de un navegador? ----------
def es_navegador():
    accept = request.headers.get("Accept", "")
    return request.method == "GET" and "text/html" in accept


# ---------- Plantilla HTML base ----------
def pagina(titulo, contenido):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
                margin: 0;
                padding: 40px;
                color: #2c3e50;
            }}
            .card {{
                max-width: 720px;
                margin: auto;
                background: #fff;
                padding: 32px 40px;
                border-radius: 12px;
                box-shadow: 0 4px 18px rgba(0,0,0,0.08);
            }}
            h1 {{ margin-top: 0; }}
            code {{
                background: #eef1f5;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: Consolas, monospace;
            }}
            a {{ color: #2980b9; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            ul {{ line-height: 1.8; }}
        </style>
    </head>
    <body>
        <div class="card">
            {contenido}
        </div>
    </body>
    </html>
    """


# ---------- Página de bienvenida con tareas ----------
def render_bienvenida(usuario, tareas):
    items = "".join(
        f"<li>{'✅' if t['completada'] else '⬜'} {t['titulo']}</li>"
        for t in tareas
    )
    contenido = f"""
        <h1>👋 Bienvenido, {usuario}</h1>
        <h2>Tus tareas pendientes</h2>
        <ul>{items if items else '<li>No tienes tareas aún</li>'}</ul>
    """
    return pagina(f"Bienvenido {usuario}", contenido)


# ---------- Endpoints ----------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    # Si es un navegador, mostrar mensaje simple
    if es_navegador():
        return pagina(
            "Registro",
            "<h1>🔐 Endpoint /registro</h1>"
            "<p>Esta ruta requiere una petición <code>POST</code>. "
            "Usá el cliente de consola para registrarte.</p>"
            "<h2>Endpoints disponibles</h2>"
                    """<ul>
                        <li><a href="/tareas">/tareas</a> — información de las tareas</li>
                        <li><a href="/login">/login</a> — información del endpoint</li>
                        <li><a href="/registro">/registro</a> — información del endpoint</li>
                        <li><a href="/logout">/logout</a> — información del endpoint</li>
                    </ul>"""
        )

    datos = request.get_json() or {}
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña") or datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    hash_pw = generate_password_hash(contrasena)

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
            (usuario, hash_pw),
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado con éxito"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409


@app.route("/login", methods=["GET", "POST"])
def login():
    # Si es un navegador, mostrar mensaje simple
    if es_navegador():
        return pagina(
            "Login",
            "<h1>🔐 Endpoint /login</h1>"
            "<p>Esta ruta requiere una petición <code>POST</code>. "
            "Usá el cliente de consola para iniciar sesión.</p>"
                        "<h2>Endpoints disponibles</h2>"
                    """<ul>
                        <li><a href="/tareas">/tareas</a> — información de las tareas</li>
                        <li><a href="/login">/login</a> — información del endpoint</li>
                        <li><a href="/registro">/registro</a> — información del endpoint</li>
                        <li><a href="/logout">/logout</a> — información del endpoint</li>
                    </ul>"""
        )

    datos = request.get_json() or {}
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña") or datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    fila = cur.fetchone()

    if fila is None or not check_password_hash(fila["contrasena_hash"], contrasena):
        conn.close()
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Crear tareas ficticias si el usuario no tiene ninguna
    cur.execute("SELECT COUNT(*) AS c FROM tareas WHERE usuario_id = ?", (fila["id"],))
    if cur.fetchone()["c"] == 0:
        iniciales = [
            "Completar el PFO 2 de Programación sobre Redes",
            "Repasar autenticación con hash",
            "Probar la API con el cliente de consola",
        ]
        cur.executemany(
            "INSERT INTO tareas (usuario_id, titulo) VALUES (?, ?)",
            [(fila["id"], t) for t in iniciales],
        )
        conn.commit()

    cur.execute("SELECT * FROM tareas WHERE usuario_id = ?", (fila["id"],))
    tareas = [dict(row) for row in cur.fetchall()]
    conn.close()

    return jsonify({
        "mensaje": f"Bienvenido {usuario}",
        "usuario_id": fila["id"],
        "html": render_bienvenida(usuario, tareas)
    }), 200


@app.route("/tareas", methods=["GET"])
def tareas():
    contenido = """
        <h1>📋 Sistema de Gestión de Tareas</h1>
            <ul>
                <li>Completar el PFO 2 de Programación sobre Redes</li>
                <li>Repasar autenticación con hash</li>
                <li>Probar la API con el cliente de consola</li>
            </ul>
        <h2>Endpoints disponibles</h2>
        <ul>
            <li><a href="/tareas">/tareas</a> — información de las tareas</li>
            <li><a href="/login">/login</a> — información del endpoint</li>
            <li><a href="/registro">/registro</a> — información del endpoint</li>
            <li><a href="/logout">/logout</a> — información del endpoint</li>
        </ul>
    """
    return pagina("Sistema de Tareas", contenido), 200


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if es_navegador():
        return pagina(
            "Logout",
            "<h1>🔐 Endpoint /logout</h1>"
            "<p>Esta ruta requiere una petición <code>POST</code>.</p>"
                        "<h2>Endpoints disponibles</h2>"
                    """<ul>
                        <li><a href="/tareas">/tareas</a> — información de las tareas</li>
                        <li><a href="/login">/login</a> — información del endpoint</li>
                        <li><a href="/registro">/registro</a> — información del endpoint</li>
                        <li><a href="/logout">/logout</a> — información del endpoint</li>
                    </ul>"""
        )
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)