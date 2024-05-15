# Bitcoin Networking

El protocolo de Bitcoin permite la conexión entre computadoras que ejecutan el mismo software o trabajan dentro del mismo protocolo. La comunicación de Bitcoin se realiza a través de Internet utilizando el protocolo TCP en el puerto 8333. Al conectarte a la red de Bitcoin, te unes a una estructura P2P (peer-to-peer) donde numerosos nodos se conectan entre sí.

Dado que el protocolo de Bitcoin facilita la conexión a la red de nodos, cualquiera puede escribir su propio programa para conectarse a la red. Solo es necesario conocer el lenguaje de comunicación de los nodos.


## Messages

El protocolo de Bitcoin establece que el primer mensaje que deben intercambiar los nodos es el mensaje de versión. Este mensaje proporciona información sobre el nodo transmisor al nodo receptor al inicio de una conexión. Hasta que los nodos no intercambien y verifiquen estos mensajes de versión, no se aceptarán otros tipos de mensajes.


## Header 

El encabezado incluye un resumen del mensaje que se va a enviar y es uniforme para todos los mensajes.

- Magic bytes: Este es un conjunto único de bytes utilizado para identificar el inicio de un nuevo mensaje. Siempre es el mismo para todos los nodos. Dado que el flujo de bits en la conexión TCP es continuo, es útil poder identificar cuándo comienza un nuevo mensaje. Este conjunto de bytes, que parece aleatorio, ha sido seleccionado específicamente para que sea improbable que aparezca en otra parte del mensaje.
- Command: Indica el tipo de mensaje que se envía. En el protocolo Bitcoin, se pueden enviar diferentes tipos de mensajes, cada uno conteniendo distintos tipos de información. Este campo de 12 bytes contiene la codificación ASCII del nombre del mensaje. Por ejemplo, "version".

### Message Header Structure:

| Name        | Example Data | Format        | Size | Bytes                               |
|-------------|--------------|---------------|------|-------------------------------------|
| Magic Bytes |              | bytes         | 4    | F9 BE B4 D9                         |
| Command     | "version"    | ascii bytes   | 12   | 76 65 72 73 69 6F 6E 00 00 00 00 00 |
| Size        | 85           | little-endian | 4    | 55 00 00 00                         |
| Checksum    |              | bytes         | 4    | F7 63 9C 60                         |


## Message Version


### Payload (version message):

| Name               | Example Data | Format                   | Size   | Example Bytes                                  |
|--------------------|--------------|--------------------------|--------|------------------------------------------------|
| Protocol Version   | 70014        | little-endian            | 4      | 7E 11 01 00                                    |
| Services           | 0            | bit field, little-endian | 8      | 00 00 00 00 00 00 00 00                        |
| Time               | 1640961477   | little-endian            | 8      | C5 15 CF 61 00 00 00 00                        |
| Remote Services    | 0            | bit field, little-endian | 8      | 00 00 00 00 00 00 00 00                        |
| Remote IP          | 64.176.221.94| ipv6, big-endian         | 16     | 00 00 00 00 00 00 00 00 00 00 FF FF 2E 13 89 4A|
| Remote Port        | 8333         | big-endian               | 2      | 20 8D                                          |
| Local Services     | 0            | bit field, little-endian | 8      | 00 00 00 00 00 00 00 00                        |
| Local IP           | 127.0.0.1    | ipv6, big-endian         | 16     | 00 00 00 00 00 00 00 00 00 00 FF FF 7F 00 00 01|
| Local Port         | 8333         | big-endian               | 2      | 20 8D                                          |
| Nonce              | 0            | little-endian            | 8      | 00 00 00 00 00 00 00 00                        |
| User Agent         | ""           | compact size, ascii      | compact| 00                                             |
| Last Block         | 0            | little-endian            | 4      | 00 00 00 00                                    |

