import java.io.*;
import java.net.*;
import javax.net.ssl.*;
import java.util.logging.FileHandler;
import java.util.logging.Logger;

import java.util.logging.SimpleFormatter;

public class BYODServer{
	private final static String USER_CORRECT = "pepito";
	private final static String PASSWD_CORRECT = "H89rtaW_16K";
	private SSLServerSocket serverSocket;

	// Constructor
	public BYODServer() throws Exception {
		// ServerSocketFactory para construir los ServerSockets
        SSLServerSocketFactory socketFactory = (SSLServerSocketFactory) SSLServerSocketFactory
					.getDefault();
        
		// creaciÃ³n de un objeto ServerSocket (se establece el puerto)
		serverSocket = (SSLServerSocket) socketFactory.createServerSocket(7070);
        //Cipher Suites soportadas
        String[] enCiphersuite = serverSocket.getEnabledCipherSuites();
		//Protocolos soportados
		String[] enProtocols = serverSocket.getEnabledProtocols();
		
		//Mostramos los Cipher Suites soportados
        for (String c : enCiphersuite)
            System.out.println("Enabled ciphersuites are: "+c);
        //Mostramos los protocolos soportados
        for (String p : enProtocols)
            System.out.println("Enabled protocols are: "+p);
		
		
        String pickedCipher[] ={"TLS_RSA_WITH_AES_256_CBC_SHA256"}; 
		//Forzamos al servidor a usar el Cipher Suites declarado en la variable pickedCipher
		serverSocket.setEnabledCipherSuites(pickedCipher);
		//Forzamos al servidor a usar el protocolo
        serverSocket.setEnabledProtocols(new String[] {"TLSv1.3"});
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
				
				
				String user = input.readLine();
				String passwd = input.readLine();
				
				if(user.equals(USER_CORRECT) && passwd.equals(PASSWD_CORRECT)){
					output.println("Login correcto");
				}else{
					output.println("Login incorrecto");
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
		BYODServer server = new BYODServer();
		server.runServer(args);
	}
}
