try {
    java.net.URL url = new java.net.URL("http://host.docker.internal:8083/copiar_y_limpiar");
    java.net.HttpURLConnection con = (java.net.HttpURLConnection) url.openConnection();

    con.setRequestMethod("POST");
    con.setDoOutput(true);
    con.setConnectTimeout(5000);
    con.setReadTimeout(5000);

    int code = con.getResponseCode();
    System.out.println("[ZZ] Respuesta HTTP: " + code);
} catch (Exception e) {
    // Captura segura sin propagar
    System.out.println("[ZZ][ERROR] Fallo al llamar a la API:");
    System.out.println(e.getMessage());
    e.printStackTrace();

}