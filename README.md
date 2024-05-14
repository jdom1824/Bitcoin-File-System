# Bitcoin Networking

El protocolo de Bitcoin permite la conexión entre computadoras que ejecutan el mismo software o trabajan dentro del mismo protocolo. La comunicación de Bitcoin se realiza a través de Internet utilizando el protocolo TCP en el puerto 8333. Al conectarte a la red de Bitcoin, te unes a una estructura P2P (peer-to-peer) donde numerosos nodos se conectan entre sí.

Dado que el protocolo de Bitcoin facilita la conexión a la red de nodos, cualquiera puede escribir su propio programa para conectarse a la red. Solo es necesario conocer el lenguaje de comunicación de los nodos.


## Messages

El protocolo de Bitcoin establece que el primer mensaje que deben intercambiar los nodos es el mensaje de versión. Este mensaje proporciona información sobre el nodo transmisor al nodo receptor al inicio de una conexión. Hasta que los nodos no intercambien y verifiquen estos mensajes de versión, no se aceptarán otros tipos de mensajes.
