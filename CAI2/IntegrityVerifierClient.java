import java.io.*;

import javax.net.*;
import javax.swing.*;
import java.net.*;

public class IntegrityVerifierClient {

	public IntegrityVerifierClient() {
		// Constructor que abre una conexión Socket para enviar mensaje/MAC al
		// servidor
		try {
			// CREAR SOCKET
			SocketFactory socketFactory = (SocketFactory) SocketFactory
					.getDefault();
			Socket socket = (Socket) socketFactory.createSocket("localhost",
					7070);
					
			// crea un PrintWriter para enviar mensaje/MAC al servidor
			PrintWriter output = new PrintWriter(new OutputStreamWriter(
					socket.getOutputStream()));
			// crea un objeto BufferedReader para leer la respuesta del servidor
			BufferedReader input = new BufferedReader(new InputStreamReader(
					socket.getInputStream()));
				
			//OBTENER CLAVE
			byte clave[] = {12,34,56,78,90,12,34,56}; //32 bits
				
			// OBTENER NONCE
			String nonce = input.readLine();
			String nonce_mac = input.readLine();
			String nonce_local_mac = MAC.performMACTest(nonce,clave);
			
			if(nonce_mac.equals(nonce_local_mac)){
				System.out.println("Nonce integro!");
			}else{
				System.err.println("Fallo de integridad");
				System.exit(-1);
			}
			
			//OBTENER MENSAJE
			String mensaje = JOptionPane.showInputDialog(null,
					"Introduzca su mensaje:");
			String macdelMensaje = MAC.performMACTest(mensaje+nonce,clave);
	
			output.println(mensaje);
			output.println(macdelMensaje);
			
			output.flush();
			
			output.close();
			input.close();
			socket.close();
		} // end try
		catch (IOException ioException) {
			ioException.printStackTrace();
		}
		// Salida de la aplicacion
		finally {
			System.exit(0);
		}
	}

	// ejecución del cliente de verificación de la integridad
	public static void main(String args[]) {
		new IntegrityVerifierClient();
	}
}
