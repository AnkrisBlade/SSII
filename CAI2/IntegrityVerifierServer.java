import java.io.*;
import java.net.*;
import javax.net.*;

public class IntegrityVerifierServer {

	private ServerSocket serverSocket;

	// Constructor
	public IntegrityVerifierServer() throws Exception {
		// ServerSocketFactory para construir los ServerSockets
		ServerSocketFactory socketFactory = (ServerSocketFactory) ServerSocketFactory
				.getDefault();
		// creaciÃ³n de un objeto ServerSocket (se establece el puerto)
		serverSocket = (ServerSocket) socketFactory.createServerSocket(7070);
	}

	// ejecuciÃ³n del servidor para escuchar peticiones de los clientes
	private void runServer() {
		while (true) {
			// espera las peticiones del cliente para comprobar mensaje/MAC
			try {
				System.err.print("Esperando conexiones de clientes...");
				Socket socket = (Socket) serverSocket.accept();
				// abre un BufferedReader para leer los datos del cliente
				BufferedReader input = new BufferedReader(
						new InputStreamReader(socket.getInputStream()));
				// abre un PrintWriter para enviar datos al cliente
				PrintWriter output = new PrintWriter(new OutputStreamWriter(
						socket.getOutputStream()));
				// se lee del cliente el mensaje y el macdelMensajeEnviado
				
				//OBTENEMOS LA CLAVE
				byte clave[] = {12,34,56,78,90,12,34,56}; //32 bits
				
				
				//ENVIAMOS EL NONCE
				String nonce = "vosnososvenezuela";
				
				output.println(nonce);
				output.println(MAC.performMACTest(nonce,clave));
				output.flush();
				
				String mensaje = input.readLine();
				String macdelMensajeEnviado = input.readLine();
				
				// a continuaciÃ³n habrÃ­a que verificar el MAC
				String macdelMensajeCalculado = MAC.performMACTest(mensaje+nonce,clave);
				System.err.println(mensaje);
				if (macdelMensajeEnviado.equals(macdelMensajeCalculado)) {
					output.println("Mensaje enviado integro ");
				} else {
					output.println("Mensaje enviado no integro.");
				}
				
				output.close();
				input.close();
				socket.close();
			} catch (IOException ioException) {
				ioException.printStackTrace();
			}
		}
	}

	// ejecucion del servidor
	public static void main(String args[]) throws Exception {
		IntegrityVerifierServer server = new IntegrityVerifierServer();
		server.runServer();
	}
}
