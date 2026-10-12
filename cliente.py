# import requests
# import webbrowser
# import tempfile
# import os

# BASE_URL = "http://127.0.0.1:5000"

# # Estado global de la sesión
# sesion = {
#     "usuario": None,
#     "usuario_id": None
# }


# # ---------- Menús ----------
# def menu_invitado():
#     print("\n=== GESTOR DE TAREAS (sin sesión) ===")
#     print("1. Registrarse")
#     print("2. Iniciar sesión")
#     print("3. Ver página pública /tareas")
#     print("4. Salir")
#     return input("Opción: ").strip()


# def menu_usuario():
#     print(f"\n=== GESTOR DE TAREAS — {sesion['usuario']} ===")
#     print("1. Ver mis tareas (página HTML)")
#     print("2. Cerrar sesión")
#     print("3. Salir")
#     return input("Opción: ").strip()


# # ---------- Acciones invitado ----------
# def registrar():
#     usuario = input("Usuario: ").strip()
#     contrasena = input("Contraseña: ").strip()
#     r = requests.post(f"{BASE_URL}/registro",
#                       json={"usuario": usuario, "contraseña": contrasena})
#     print(f"[{r.status_code}] {r.json()}")


# def login():
#     usuario = input("Usuario: ").strip()
#     contrasena = input("Contraseña: ").strip()
#     r = requests.post(f"{BASE_URL}/login",
#                       json={"usuario": usuario, "contraseña": contrasena})

#     if r.status_code == 200:
#         data = r.json()
#         sesion["usuario"] = usuario
#         sesion["usuario_id"] = data["usuario_id"]
#         print(f"\n✅ {data['mensaje']}")
#         # Mostrar la página HTML de bienvenida con las tareas
#         abrir_html_en_navegador(data["html"])
#     else:
#         print(f"[{r.status_code}] {r.json()}")


# def ver_tareas_publicas():
#     r = requests.get(f"{BASE_URL}/tareas")
#     print(f"[{r.status_code}] HTML recibido:")
#     print(r.text[:200])


# # ---------- Acciones usuario logueado ----------
# def ver_mis_tareas():
#     # Volvemos a pedir el HTML al servidor pidiendo login de nuevo (simple)
#     # En un caso real usaríamos un token. Aquí lo regeneramos pidiendo credenciales.
#     usuario = sesion["usuario"]
#     contrasena = input(f"Confirma la contraseña de '{usuario}': ").strip()
#     r = requests.post(f"{BASE_URL}/login",
#                       json={"usuario": usuario, "contraseña": contrasena})
#     if r.status_code == 200:
#         abrir_html_en_navegador(r.json()["html"])
#     else:
#         print(f"[{r.status_code}] {r.json()}")


# def cerrar_sesion():
#     r = requests.post(f"{BASE_URL}/logout")
#     print(f"[{r.status_code}] {r.json()}")
#     sesion["usuario"] = None
#     sesion["usuario_id"] = None


# # ---------- Utilidad: abrir HTML en el navegador ----------
# def abrir_html_en_navegador(html: str):
#     """Guarda el HTML en un archivo temporal y lo abre en el navegador."""
#     fd, path = tempfile.mkstemp(suffix=".html")
#     with os.fdopen(fd, "w", encoding="utf-8") as f:
#         f.write(html)
#     webbrowser.open(f"file://{path}")
#     print("🌐 Página abierta en el navegador.")


# # ---------- Bucle principal ----------
# def main():
#     while True:
#         if sesion["usuario"] is None:
#             op = menu_invitado()
#             if op == "1":
#                 registrar()
#             elif op == "2":
#                 login()
#             elif op == "3":
#                 ver_tareas_publicas()
#             elif op == "4":
#                 print("¡Hasta luego!")
#                 break
#             else:
#                 print("Opción inválida")
#         else:
#             op = menu_usuario()
#             if op == "1":
#                 ver_mis_tareas()
#             elif op == "2":
#                 cerrar_sesion()
#             elif op == "3":
#                 print("¡Hasta luego!")
#                 break
#             else:
#                 print("Opción inválida")


# if __name__ == "__main__":
#     main()



# cliente.py
import requests
import webbrowser

BASE_URL = "http://127.0.0.1:5000"

# Estado global de la sesión
sesion = {
    "usuario": None,
    "usuario_id": None
}


# ---------- Menús ----------
def menu_invitado():
    print("\n=== GESTOR DE TAREAS (sin sesión) ===")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Ver página pública /tareas")
    print("4. Salir")
    return input("Opción: ").strip()


def menu_usuario():
    print(f"\n=== GESTOR DE TAREAS — {sesion['usuario']} ===")
    print("1. Ver mis tareas (página HTML)")
    print("2. Cerrar sesión")
    print("3. Salir")
    return input("Opción: ").strip()


# ---------- Acciones invitado ----------
def registrar():
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    r = requests.post(f"{BASE_URL}/registro",
                      json={"usuario": usuario, "contraseña": contrasena})
    print(f"[{r.status_code}] {r.json()}")


def login():
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    r = requests.post(f"{BASE_URL}/login",
                      json={"usuario": usuario, "contraseña": contrasena})

    if r.status_code == 200:
        data = r.json()
        sesion["usuario"] = usuario
        sesion["usuario_id"] = data["usuario_id"]
        print(f"\n✅ {data['mensaje']}")
        # Abrimos directamente la ruta /tareas en el navegador
        webbrowser.open(f"{BASE_URL}/tareas")
    else:
        print(f"[{r.status_code}] {r.json()}")


def ver_tareas_publicas():
    webbrowser.open(f"{BASE_URL}/tareas")
    print("🌐 Página /tareas abierta en el navegador.")


# ---------- Acciones usuario logueado ----------
def ver_mis_tareas():
    # Abre directamente la ruta /tareas del servidor en el navegador
    webbrowser.open(f"{BASE_URL}/tareas")
    print("🌐 Página /tareas abierta en el navegador.")


def cerrar_sesion():
    r = requests.post(f"{BASE_URL}/logout")
    print(f"[{r.status_code}] {r.json()}")
    sesion["usuario"] = None
    sesion["usuario_id"] = None


# ---------- Bucle principal ----------
def main():
    while True:
        if sesion["usuario"] is None:
            op = menu_invitado()
            if op == "1":
                registrar()
            elif op == "2":
                login()
            elif op == "3":
                ver_tareas_publicas()
            elif op == "4":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida")
        else:
            op = menu_usuario()
            if op == "1":
                ver_mis_tareas()
            elif op == "2":
                cerrar_sesion()
            elif op == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida")


if __name__ == "__main__":
    main()