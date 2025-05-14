try {
    java.net.HttpURLConnection con = (java.net.HttpURLConnection)
        new java.net.URL("http://host.docker.internal:8083/copiar_y_limpiar").openConnection();
    con.setRequestMethod("POST");
    con.setDoOutput(true);
    int code = con.getResponseCode();
    System.out.println("[ZZ]Respuesta HTTP: " + code);
} catch (Exception e) {
    e.printStackTrace();
}



//---------------------------------------------------------------------------------------------------------
//LLAMAR APY DOCUMENTCOLLECTION
//---------------------------------------------------------------------------------------------------------

try {
    // Obtener el ID de la instancia de proceso actual
    String processInstanceId = kcontext.getProcessInstance().getId() + "";

    // Construir la URL con el ID
    String endpoint = "http://host.docker.internal:5001/actualizar_documentos/" + processInstanceId;

    // Crear y configurar la conexión
    java.net.URL url = new java.net.URL(endpoint);
    java.net.HttpURLConnection con = (java.net.HttpURLConnection) url.openConnection();
    con.setRequestMethod("GET");
    con.connect();

    // Leer la respuesta
    int responseCode = con.getResponseCode();
    System.out.println("[XX] Código de respuesta: " + responseCode);

    if (responseCode == 200) {
        System.out.println("[XX] Documentos actualizados exitosamente");
    } else {
        System.out.println("[XX] Error al actualizar documentos: " + responseCode);
    }

} catch (Exception e) {
    System.err.println("[XX] Error al llamar a la API de actualización de documentos: " + e.getMessage());
    e.printStackTrace();
}
