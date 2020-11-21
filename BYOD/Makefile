all:
	javac main.java
	java main
	
server:
	javac BYODServer.java
	java -Djavax.net.ssl.keyStore="/home/fran/.keystore" -Djavax.net.ssl.keyStorePassword="naranjito" BYODServer

client:
	javac BYODCliente.java 
	java -Djavax.net.ssl.trustStore="/home/fran/.keystore" -Djavax.net.ssl.trustStorePassword="naranjito" BYODCliente
