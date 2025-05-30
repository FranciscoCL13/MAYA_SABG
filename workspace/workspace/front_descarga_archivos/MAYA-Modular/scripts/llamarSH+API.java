try {
    // === Ejecuta script de copiado dentro del contenedor jbpm-server ===
    System.out.println("[ZZ] ---- Iniciar copiado de archivos ---- ");
    String[] copyCmd = {"/bin/bash", "/opt/scripts/copiar_completo_CC_dentroDocker.sh"};
    Process copyProc = Runtime.getRuntime().exec(copyCmd);
    int copyExitCode = copyProc.waitFor();
    System.out.println("[ZZ] ---- Proceso de copiado terminado con código: " + copyExitCode + " ---- ");

    // === Ejecuta script de limpieza dentro del contenedor jbpm-server ===
    System.out.println("[ZZ] ---- Iniciar limpieza de archivos ---- ");
    String[] cleanCmd = {"/bin/bash", "/opt/scripts/limpiar_jbpm_docs_dentroDocker.sh"};
    Process cleanProc = Runtime.getRuntime().exec(cleanCmd);
    int cleanExitCode = cleanProc.waitFor();
    System.out.println("[ZZ] ---- Proceso de limpieza terminado con código: " + cleanExitCode + " ---- ");

    // === Llama a la API del contenedor flask-api desde jbpm-server ===
    System.out.println("[ZZ] ---- INICIO de ejecución de API ----");
    java.net.URL url = new java.net.URL("http://flask-api:8083/copiar_y_limpiar");
    java.net.HttpURLConnection con = (java.net.HttpURLConnection) url.openConnection();
    con.setRequestMethod("POST");
    con.setDoOutput(true);
    con.setConnectTimeout(5000);
    con.setReadTimeout(5000);

    int httpResponseCode = con.getResponseCode();
    System.out.println("[ZZ] Respuesta HTTP de Flask API: " + httpResponseCode);

} catch (Exception e) {
    System.out.println("[ZZ][ERROR] Fallo durante la ejecución:");
    e.printStackTrace();
}
