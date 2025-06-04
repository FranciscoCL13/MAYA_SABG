from sqlalchemy.orm import Session
from sqlalchemy import text


class CrudMetadata:
    def get_metadata_list(self, db: Session):
        with db.connection() as conn:
            return conn.execute(text('select id as value, table_name as label from ogr_system_tables.metadata order by id')).fetchall()


crud_metadata = CrudMetadata()
