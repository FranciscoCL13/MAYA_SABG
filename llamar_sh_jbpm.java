try {
    java.net.HttpURLConnection con = (java.net.HttpURLConnection)
        new java.net.URL("http://host.docker.internal:8083/copiar_y_limpiar").openConnection();
    con.setRequestMethod("POST");
    con.setDoOutput(true);
    int code = con.getResponseCode();
    System.out.println("Respuesta HTTP: " + code);
} catch (Exception e) {
    e.printStackTrace();
