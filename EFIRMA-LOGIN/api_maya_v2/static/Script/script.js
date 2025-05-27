let sesion = null;
         document.getElementById("fuera").style = "";
         document.getElementById("dentro").style = "display: none;";
         async function inicia_sesion(datos) {
           const respuesta = await fetch("/", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: datos ? JSON.stringify(datos) : "{}"
           });
           sesion = await respuesta.json();
           
     
           if ("rfc" in sesion) {
              document.getElementById("dentro").style = "";
              document.getElementById("fuera").style = "display: none;";
              document.getElementById("rfc").innerText = sesion.rfc;
           } else {
              document.getElementById("fuera").style = "";
              document.getElementById("dentro").style = "display: none;";
           }
           //Oculta el loader al finalizar
           document.getElementById('loader-overlay').style.display = 'none';
        }
     
        async function cierra_sesion() {
         /*----------------------Implementación 25/04/25----------------------*/
         localStorage.removeItem("usuarioAutenticado");
         /*----------------------Implementación 25/04/25----------------------*/
         inicia_sesion({ salir: true });
        }
     
        async function autentica(forma) {
           function cadena_binaria(arr) {
              return Array.from(arr).map(byte => String.fromCharCode(byte)).join('');
              /*----------------------Implementación 25/04/25----------------------*/
              sessionStorage.setItem("usuarioAutenticado", "true");
              /*----------------------Implementación 25/04/25----------------------*/
           }

           //Mostrar loader
           document.getElementById('loader-overlay').style.display = 'flex';
     
           try {
              const certificado = cadena_binaria(new Uint8Array(await forma.certificado.files[0].arrayBuffer()));
              const llave_privada = cadena_binaria(new Uint8Array(await forma.llave_privada.files[0].arrayBuffer()));
              const fiel = credentials.Credential.create(certificado, llave_privada, forma.password.value);
              const timestamp = Math.floor(Date.now() / 1000);
              const cadena_original = `${timestamp}_${sesion.challenge}`;
     
              const enviar = {
                 certificado: btoa(certificado),
                 timestamp: timestamp,
                 firma_cadena: btoa(fiel.sign(cadena_original))
              };
     
              inicia_sesion(enviar);
           } catch (e) {
               //Ocultar loader si falla
               document.getElementById('loader-overlay').style.display = 'none';
              alert(`Se produjo un error inesperados ${e.message}`);
           }
        }
