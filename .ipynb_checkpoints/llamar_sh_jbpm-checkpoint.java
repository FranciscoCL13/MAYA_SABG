Boolean kcontextEsSuceptibledeEntrega = false;
try {
    System.out.println("[YY]Iniciando script ");

    String[] cmd = {"/bin/bash", "/opt/jboss/wildfly/bin/jbpm_docs/MAYA-Modular/scripts/start_api.sh"};
    Process proc = Runtime.getRuntime().exec(cmd);
    int code = proc.waitFor();
    System.out.println("[YY]Script ejecutado con código de salida: " + code);
} catch (Exception e) {
    System.out.println("[YY]Error al ejecutar script: " + e.getMessage());
}

