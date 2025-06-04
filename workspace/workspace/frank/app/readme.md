MAYA/
├── app/
│   ├── __init__.py              # Crea y configura la app Flask
│   ├── main.py                  # Punto de entrada
│   ├── config.py                # Configuración global (rutas, jBPM, claves)
│   ├── api_documentos/          # (API 1)
│   │   └── routes.py
│   ├── api_efirma/              # (API 2)
│   │   ├── routes.py
│   │   ├── ocsp_proxy.py
│   │   └── templates/
│   │       ├── form7.html
│   │       └── index.html
│   ├── api_tablas/              # (API 3)
│   │   ├── routes.py
│   │   ├── conexion.py
│   │   ├── copiar_completo.sh
│   │   ├── limpiar_docs.sh
│   │   └── templates/
│   │       └── index.html
└── requirements.txt
