import java.io.*;

import javax.net.*;
import javax.swing.*;
import java.net.*;
import java.util.*;

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
				
			//OBTENER CLAVE ; EN EL CLIENTE LA PEDIMOS GRAFICAMENTE
			JFileChooser jq = new JFileChooser(".");
 			int op = jq.showOpenDialog(null);
 			
 			String claveStr = "";
 			if( op == JFileChooser.APPROVE_OPTION ){    
                File fd = jq.getSelectedFile();    
                try{  
                    BufferedReader br=new BufferedReader(new FileReader(fd));    
                    String linea;
                    while((linea=br.readLine()) != null){
                        claveStr += linea;
                    };
                    br.close();    
                }catch (Exception ex) {
                    ex.printStackTrace();  
                }                 
            }else{
                System.err.println("Debe introducir la contraseña!");
                System.exit(-1);
            }
        
			byte[] clave = claveStr.getBytes();
			
			// OBTENER NONCE
			String nonce = input.readLine();
			String nonce_mac = input.readLine();
			String nonce_local_mac = MAC.performMACTest(nonce,clave);
			
			if(nonce_mac.equals(nonce_local_mac)){
				System.out.println("Nonce integro!");
			}else{
				System.err.println("Fallo de integridad");
				JOptionPane.showMessageDialog(null, "No se puedo establecer la sesión (Fallo al autentificar nonce)",
                        "Fallo de autentificación", JOptionPane.ERROR_MESSAGE);
				System.exit(-1);
			}
			
			//OBTENER MENSAJE
			String mensaje = JOptionPane.showInputDialog(null,
					"Introduzca su mensaje:");
			String macdelMensaje = MAC.performMACTest(mensaje+nonce,clave);
	
			output.println(mensaje);
			output.println(macdelMensaje);
			
			output.flush();
			
			String res = input.readLine();
			if(res.equals("ACK")){
                JOptionPane.showMessageDialog(null, "Transacción completada con éxito",
                        "Éxito",JOptionPane.INFORMATION_MESSAGE);
			}else{
                System.err.println("Fallo de integridad");
				JOptionPane.showMessageDialog(null, "No se puedo establecer la sesión (Fallo al autentificar el mensaje)",
                        "Fallo de autentificación", JOptionPane.ERROR_MESSAGE);
				System.exit(-1);
			}
			
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
