import java.io.*;

import javax.net.ssl.*;
import javax.swing.*;

public class BYODCliente {

	public BYODCliente() {
		// Constructor que abre una conexión Socket para enviar mensaje/MAC al
		// servidor
		try {
			// CREAR SOCKET
			SSLSocketFactory socketFactory = (SSLSocketFactory) SSLSocketFactory
					.getDefault();
			SSLSocket socket = (SSLSocket) socketFactory.createSocket("localhost",
					7070);
					
			// crea un PrintWriter para enviar mensaje/MAC al servidor
			PrintWriter output = new PrintWriter(new OutputStreamWriter(
					socket.getOutputStream()));
			// crea un objeto BufferedReader para leer la respuesta del servidor
			BufferedReader input = new BufferedReader(new InputStreamReader(
					socket.getInputStream()));
				
			//OBTENEMOS USUARIO
			String user = JOptionPane.showInputDialog(null, "Introduzca su usario");
			output.println(user);
			//OBTENEMOS CONTRASEÑA
			String passwd = JOptionPane.showInputDialog(null,"Introduzca su clave:");
			output.println(passwd);
 			
			//OBTENER MENSAJE
			String mensaje = JOptionPane.showInputDialog(null,"Introduzca su mensaje:");
	
			output.println(mensaje);
			
			output.flush();
			//Imprimimos la respuesta del servidor
			String respuesta = input.readLine();
			JOptionPane.showMessageDialog(null,respuesta);
			
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
		new BYODCliente();
	}
}
