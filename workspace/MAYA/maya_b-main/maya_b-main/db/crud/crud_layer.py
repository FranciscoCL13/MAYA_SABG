from sqlalchemy.orm import Session
from sqlalchemy import text


class CrudLayer:
    def load_layer(self, db: Session, id: int):
        with db.connection() as conn:

            table_name = '"TM-fonatur".pol_tramos_unidos'
            
            if id == 1:
                tramo = 'Tramo 1'
            elif id == 2:
                tramo = 'Tramo 2'
            elif id == 3:
                tramo = 'Tramo 3'
            elif id == 4:
                tramo = 'Tramo 4'
            elif id == 5:
                tramo = 'Tramo 4-2'
            elif id == 6:
                tramo = 'Tramo 5'
            elif id == 7:
                tramo = 'Tramo 6'
            elif id == 8:
                tramo = 'Tramo 6-2'
            elif id == 9:
                tramo = 'Tramo 7'
            elif id == 10:
                tramo = 'Tramo 7-pend'
            elif id == 11:
            # Llamamos al método load_areas
                return self.load_areas(db, id)

                
                # table_name = '"TM-fonatur"."anpmx.shp"'
                # tramo = 'anpmx.shp'



            """
            Construye la consulta dinámica.
            """
            sql_query = text(f"""
                SELECT jsonb_build_object(
                    'type', 'FeatureCollection',
                    'layer', '{table_name}',
                    'features', jsonb_agg(
                        jsonb_build_object(
                            'type', 'Feature',
                            'geometry', ST_AsGeoJSON(geom)::jsonb,
                            'capa', '{tramo}',
                            'properties', jsonb_strip_nulls(to_jsonb(t) - 'geom')
                        )
                    )
                ) AS geojson
                FROM {table_name} AS t

            
                WHERE TRAMO = '{tramo}'
            """)


            return conn.execute(sql_query).fetchone()[0]
            
    def load_areas(self, db: Session, id: int):
        with db.connection() as conn:

            # table_name = '"TM-fonatur".pol_tramos_unidos'
            table_name = '"TM-fonatur"."anpmx.shp"'
            
            if id == 11:
                tramo = 'anpmx.shp'


            """
            Construye la consulta dinámica.
            """
            sql_query = text(f"""
                SELECT jsonb_build_object(
                    'type', 'FeatureCollection',
                    'layer', '{table_name}',
                    'features', jsonb_agg(
                        jsonb_build_object(
                            'type', 'Feature',
                            'geometry', ST_AsGeoJSON(geom)::jsonb,
                            'capa', '{tramo}',
                            'properties', jsonb_strip_nulls(to_jsonb(t) - 'geom')
                        )
                    )
                ) AS geojson
                FROM {table_name} AS t
                --WHERE TRAMO = '{tramo}'
            """)

            print(sql_query)


            return conn.execute(sql_query).fetchone()[0]

crud_layer = CrudLayer()
