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
