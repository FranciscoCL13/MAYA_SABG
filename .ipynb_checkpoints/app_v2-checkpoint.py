from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, text
import pandas as pd

app = Flask(__name__)

# Conexión a PostgreSQL
user = 'jbpm'
password = 'jbpm'
host = 'localhost'
port = '5432'
database = 'jbpm'
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

@app.route('/')
def index():
    return render_template('index.html')

# GET GENERAR TABLA
@app.route('/generar_tabla', methods=['GET'])
def generar_tabla():
    try:
        # Cargar y pivotear
        # TABLA taskvariableimpl

        df_pivot = pd.read_sql("""
            SELECT
                taskvariableimpl.processinstanceid,
                taskvariableimpl.taskid as id_tarea,
                task.actualowner_id,
                task.formname,
                taskvariableimpl.name as campo,
                taskvariableimpl.value
            FROM taskvariableimpl
            JOIN task
                ON taskvariableimpl.processinstanceid = task.processinstanceid
            ORDER BY taskvariableimpl.processinstanceid;
        """, engine)

        
        # Insertar en la base de datos
        df_pivot.to_sql(
            name='x_mi_tabla_completa',
            con=engine,
            if_exists='replace',  # ' reemplazar completamente la tabla cada vez
            index=False
        )

        

        # Renderizar tabla
        nombre_tabla = "<h3>Tabla:</h3> <h1>x_mi_tabla_completa </h1><a> Se generó y almacenó en base de datos</a><hr>"
        tabla_html = df_pivot.to_html(classes='table table-bordered', index=False)
        return jsonify({'tabla': nombre_tabla + tabla_html})
    
    except Exception as e:
        return jsonify({'tabla': f"<p style='color:red;'>Error al generar o almacenar la tabla: {e}</p>"})

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)