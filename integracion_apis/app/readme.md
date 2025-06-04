/app/
├── main.py            ← Ejecutas todo con: `python -m app.main`
├── api_adjuntos/      ← Primera API (la de `/documentos`)
│   ├── routes.py
│   └── __init__.py
├── api_efirma/        ← Segunda API (con e.firma y jBPM)
│   ├── routes.py
│   ├── ocsp_proxy.py
│   ├── __init__.py
│   └── templates/
├── api_tablas/        ← Tercera API (generación de tablas)
│   ├── __init__.py    ← ya tienes esto hecho ✅
│   ├── main.py        ← ya no se usa, será absorbido por el global
│   ├── conexion.py
│   ├── tablas_busqueda.py (o routes.py)
│   └── templates/


find . -print | sed -e 's;[^/]*\/;|____;g;s;____|; |;g'

"C:\Users\francisco.contreras\AppData\Local\Programs\Python\Python311\python.exe" --version

"C:\Users\francisco.contreras\AppData\Local\Programs\Python\Python311\python.exe" -m venv venv311

source venv311/Scripts/activate


------------------------------------

$ flask routes
Endpoint                         Methods  Rule
-------------------------------  -------  -------------------------------
api_adjuntos.descargar_archivo   GET      /files/<document_id>/<filename>
api_adjuntos.mostrar_archivos    GET      /archivos
api_adjuntos.recibir_documentos  POST     /documentos
efirma_bp.descargar_documento    GET      /documentos/<filename>
efirma_bp.login                  POST     /login
efirma_bp.login_page             GET      /login
efirma_bp.mostrar_index          GET      /
efirma_bp.recibir_documento      POST     /documentos
static                           GET      /static/<path:filename>
tablas_bp.buscar_tabla           GET      /buscar_tabla
tablas_bp.descargar_archivo      GET      /descargar/<path:filename>
tablas_bp.generar_tabla          GET      /generar_tabla
tablas_bp.index                  GET      /
(venv311)
