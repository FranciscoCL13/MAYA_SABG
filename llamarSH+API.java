try {
    // Ejecuta script de copiado dentro del contenedor jbpm-server
    System.out.println("[ZZ] ---- Iniciar copiado de archivos ---- ");
    String[] cmd = {"/bin/bash", "/opt/scripts/copiar_completo_CC_dentroDocker.sh"};
    Process proc = Runtime.getRuntime().exec(cmd);
    int scriptExitCode = proc.waitFor();
    System.out.println("[ZZ] ---- Proceso de copiado terminado ---- ");


   // Ejecuta script de limpieza dentro del contenedor jbpm-server
    System.out.println("[ZZ] ---- Iniciar limpieza de archivos ---- ");
    System.out.println("[ZZ] ---- Proceso de limpieza terminado ---- ");


    // Llama a la API del contenedor flask-api desde jbpm-server
    System.out.println("[ZZ] ---- INICIO de ejecución de API ----");
    java.net.URL url = new java.net.URL("http://flask-api:8083/copiar_y_limpiar");
    java.net.HttpURLConnection con = (java.net.HttpURLConnection) url.openConnection();
    con.setRequestMethod("POST");
    con.setDoOutput(true);
    con.setConnectTimeout(5000);
    con.setReadTimeout(5000);
    System.out.println("[ZZ]API ejecutada con código de salida (script): " + scriptExitCode);

    int httpResponseCode = con.getResponseCode();
    System.out.println("[ZZ] Respuesta HTTP de Flask API: " + httpResponseCode);

} catch (Exception e) {
    System.out.println("[ZZ][ERROR] Fallo al llamar a la API:");
    System.out.println(e.getMessage());
    e.printStackTrace();
}
