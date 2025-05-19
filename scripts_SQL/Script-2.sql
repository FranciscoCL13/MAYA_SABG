/*SELECCIONAR COLUMNAS Y TIPO DE DATO*/
select column_name, data_type 
from information_schema.columns
where table_name = 'audittaskimpl';

select  processinstanceid, actualowner   
from audittaskimpl a
where actualowner != 'wbadmin' 
order by processinstanceid desc ;

select  *   
from audittaskimpl a
order by processinstanceid desc ;


/*Proyecto MYSPACE - projectfive*/
select * from ujackone ;
select * from ujohn;
select * from ukaty;
select * from ujacktwo;

select * from tablacontodos t ;

/*MYSPACE - pruebasids*/
select * from wprocessid;

drop table ujackone, ujohn, ukaty, ujacktwo, tablacontodos;


-- ¡PELIGRO! Esto borrará todos los datos de las tablas de jBPM!
TRUNCATE TABLE AuditTaskImpl CASCADE;
TRUNCATE TABLE BAMTaskSummary CASCADE;
TRUNCATE TABLE CaseFileDataLog CASCADE;
TRUNCATE TABLE caseroleassignmentlog CASCADE;
TRUNCATE TABLE ContextMappingInfo CASCADE;
TRUNCATE TABLE CorrelationKeyInfo CASCADE;
TRUNCATE TABLE CorrelationPropertyInfo CASCADE;
TRUNCATE TABLE EventTypes CASCADE;
TRUNCATE TABLE ExecutionErrorInfo CASCADE;
TRUNCATE TABLE NodeInstanceLog CASCADE;
TRUNCATE TABLE ProcessInstanceInfo CASCADE;
TRUNCATE TABLE RequestInfo CASCADE;
TRUNCATE TABLE SessionInfo CASCADE;
TRUNCATE TABLE TaskEvent CASCADE;
TRUNCATE TABLE Task CASCADE;
TRUNCATE TABLE VariableInstanceLog CASCADE;
TRUNCATE TABLE WorkItemInfo CASCADE;

CREATE SEQUENCE hibernate_sequence START WITH 1 INCREMENT BY 1;

-- ¡PELIGRO! Esto reiniciará las secuencias (si las usa jBPM)!
ALTER SEQUENCE hibernate_sequence RESTART WITH 1; -- Nombre común de Hibernate
ALTER SEQUENCE ENTIDAD_ID_SEQ RESTART WITH 1;   -- Tu secuencia (si la definiste)
-- Busca otras secuencias que puedan estar relacionadas con jBPM

select * from x_documentos_cargados_prueba;

select * from variableinstancelog;

-- CONSULTAR TABLAS EXISTENTES:

SELECT table_name
FROM information_schema.tables;


-- CONSULTAR DOCUMENTO CARGADO:

SELECT 
    a.id AS attachment_id,
    a.name AS attachment_name,
    a.contenttype AS attachment_content_type,
    c.content AS attachment_data -- este campo tiene el archivo
FROM 
    attachment a
JOIN 
    content c ON a.attachmentcontentid = c.id;


-- CONSULTAR ESSQUEMA DE UNA TABLA

SELECT column_name, data_type, column_default, is_nullable
FROM information_schema.columns
WHERE table_name = 'tabla_document_collections';

select * from  task;


select processinstanceid, taskid, name, value from taskvariableimpl t ;
select processinstanceid, id as taskid, actualowner_id, formname from task;


select * from x_mi_tabla_completa ;

-- JOIN POR PROCESSINSTANCEID,TASKID,NAME, ETC

SELECT
    taskvariableimpl.processinstanceid,
    taskvariableimpl.processid,
    task.actualowner_id,
    task.formname,
    taskvariableimpl.name,
    taskvariableimpl.value
FROM taskvariableimpl
JOIN task
    ON taskvariableimpl.processinstanceid = task.processinstanceid
    and taskvariableimpl.taskid = task.id
WHERE taskvariableimpl.value LIKE '%####%' or taskvariableimpl.value LIKE '%@%'
ORDER BY taskvariableimpl.processinstanceid;


SELECT processinstanceid, taskid, name as Campo_llenado, value as registro_de_campo, processid
            FROM taskvariableimpl;

select * from task;

select * from taskvariableimpl t;

select * from x_mi_tabla_completa xmtc ;

select * from tabla_document_collections tdc ;
-----------------------------------------------------------------------------------

		SELECT 
              x.numero_catastral,
              x.usuario,
              x.processinstanceid,
              x.value,
              x.variable,
              x.modificationdate
            FROM x_mi_tabla_completa x
            WHERE x.value ~ '####[0-9]+####'

            UNION ALL

            SELECT 
              x.numero_catastral,
              x.usuario,
              d.processinstanceid,
              d.value,
              d.variable,
              x.modificationdate
            FROM x_mi_tabla_completa x
            JOIN tabla_document_collections d
              ON x.processinstanceid = d.processinstanceid
             AND x.variable = d.variable
            WHERE x.value !~ '####[0-9]+####'
            ORDER BY numero_catastral;

