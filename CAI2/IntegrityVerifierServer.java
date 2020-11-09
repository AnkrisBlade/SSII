import java.io.*;
import java.net.*;
import javax.net.*;
import java.nio.*;
import java.util.Random;

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
	private void runServer(String[] args) {
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
				
				//OBTENEMOS LA CLAVE ; EN EL SERVIDOR LA OBTENEMOS DEL FICHERO SEÑALADO EN EL PRIMERO ARGUMENTO
				String claveStr = "";
                try{  
                    BufferedReader br=new BufferedReader(new FileReader(args[0]));    
                    String linea;
                    while((linea=br.readLine()) != null){
                        claveStr += linea;
                    };
                    br.close();    
                }catch (Exception ex) {
                    ex.printStackTrace();  
                }                 
            
                byte[] clave = claveStr.getBytes();
				
				
				//GENERAR EL NONCE DE FORMA ALEATORIA
				Random rand = new Random();
				byte[] nonce_byte = ByteBuffer.allocate(8).putLong(rand.nextLong()).array();
                String nonce = MAC.byteArrayToHexString(nonce_byte);
				
				//ENVIAR EL NONCE
				output.println(nonce);
				output.println(MAC.performMACTest(nonce,clave));
				output.flush();
				
				String mensaje = input.readLine();
				String macdelMensajeEnviado = input.readLine();
				
				// a continuaciÃ³n habrÃ­a que verificar el MAC
				String macdelMensajeCalculado = MAC.performMACTest(mensaje+nonce,clave);
				System.err.println(mensaje);
				if (macdelMensajeEnviado.equals(macdelMensajeCalculado)) {
					output.println("ACK");
				} else {
					output.println("NACK");
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
		server.runServer(args);
	}
}
