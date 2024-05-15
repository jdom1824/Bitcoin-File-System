# Bitcoin Networking

El protocolo de Bitcoin permite la conexión entre computadoras que ejecutan el mismo software o trabajan dentro del mismo protocolo. La comunicación de Bitcoin se realiza a través de Internet utilizando el protocolo TCP en el puerto 8333. Al conectarte a la red de Bitcoin, te unes a una estructura P2P (peer-to-peer) donde numerosos nodos se conectan entre sí.

Dado que el protocolo de Bitcoin facilita la conexión a la red de nodos, cualquiera puede escribir su propio programa para conectarse a la red. Solo es necesario conocer el lenguaje de comunicación de los nodos.


## Messages

El protocolo de Bitcoin establece que el primer mensaje que deben intercambiar los nodos es el mensaje de versión. Este mensaje proporciona información sobre el nodo transmisor al nodo receptor al inicio de una conexión. Hasta que los nodos no intercambien y verifiquen estos mensajes de versión, no se aceptarán otros tipos de mensajes.


## Header 

El encabezado incluye un resumen del mensaje que se va a enviar y es uniforme para todos los mensajes.

- Magic bytes: Este es un conjunto único de bytes utilizado para identificar el inicio de un nuevo mensaje. Siempre es el mismo para todos los nodos. Dado que el flujo de bits en la conexión TCP es continuo, es útil poder identificar cuándo comienza un nuevo mensaje. Este conjunto de bytes, que parece aleatorio, ha sido seleccionado específicamente para que sea improbable que aparezca en otra parte del mensaje.
- Command: Indica el tipo de mensaje que se envía. En el protocolo Bitcoin, se pueden enviar diferentes tipos de mensajes, cada uno conteniendo distintos tipos de información. Este campo de 12 bytes contiene la codificación ASCII del nombre del mensaje. Por ejemplo, "version".
- Size: Es el tamaño de la próxima carga útil. Este campo indica cuántos bytes se necesitan leer del socket para recibir el mensaje completo.
- CheckSum: Es una pequeña huella digital de la carga útil. Permite verificar rápidamente que los datos de la carga útil no han sido manipulados durante el tránsito.

### Message Header Structure:

| Name        | Example Data | Format        | Size | Bytes                               |
|-------------|--------------|---------------|------|-------------------------------------|
| Magic Bytes |              | bytes         | 4    | F9 BE B4 D9                         |
| Command     | "version"    | ascii bytes   | 12   | 76 65 72 73 69 6F 6E 00 00 00 00 00 |
| Size        | 85           | little-endian | 4    | 55 00 00 00                         |
| Checksum    |              | bytes         | 4    | F7 63 9C 60                         |


## Message Version

El mensaje de versión es uno de los más completos que se puede enviar en Bitcoin, ya que contiene mucha información. Sin embargo, es un buen punto de partida, porque si puedes construir un mensaje de versión, podrás construir cualquier mensaje dentro del protocolo de Bitcoin. El código en Python lo encuentras aquí: [version_message.py](https://github.com/jdom1824/Bitcoin-File-System/blob/main/version_message.py)


- Protocol version: Este campo indica la versión del protocolo que está en uso y define los comandos que el protocolo puede entender. Diferentes versiones soportan diferentes tipos de mensajes, por lo que, conociendo la versión del protocolo, podemos determinar qué tipos de mensajes se pueden manejar.
- Services: Este campo es una lista opcional de servicios que tu nodo puede ofrecer. Es un campo de 32 bits, donde cada bit en 1 indica que el nodo puede proporcionar diferentes servicios. Por ejemplo, tener el primer bit en 1 indica que eres un nodo completo y puedes ofrecer todos los bloques de la blockchain. Dejar este campo en 0 indica que el nodo está en modo de prueba.
- Time: Es el tiempo en formato Unix
- Remote services: Esta es una lista opcional de servicios que crees que están disponibles en el nodo remoto al que te vas a conectar. Es similar a la estructura principal de servicios.
- Remote IP: Esta es la dirección IP del nodo al que te vas a conectar o piensas que puedes conectarte. Esta dirección está en formato IPv6.
- Remote Port: Este es el puerto al que nos debemos conectar, por defecto 8333.
- Local Services: Esta es una lista de servicios que puede ofrecer tu nodo.
- Local IP: Esta es la dirección IP de tu nodo a nivel local.
- Local Port: Este es el puerto del nodo a nivel local, generalmente es el mismo 8333.
- Nonce: Es un número generado aleatoriamente que puede usarse para detectar conexiones a ti mismo más tarde. Se puede dejar en 0.
- User Agent: Es una cadena de texto que puede identificarte en la red. Por ejemplo, /Satoshi:22-0-0/, pero también puedes poner "Nodo escalable versión 1".
- Last Block: La altura del bloque en tu blockchain local. Puedes dejarlo en 0 si no tienes ningún bloque descargado.

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

## Handshake

El handshake es el proceso que establece comunicacion entre dos nodos de Bitcoin. Antes de empezar a recibir data, necesitamos realizar un handshake con otro nodo. Esto es solo una secuencia de mensajes. 

En el protocolo de Bitcoin el hanshake trabaja de la siguiente manera: 

![Handshake](https://github.com/jdom1824/Bitcoin-File-System/blob/main/images/Handshake.jpg)

Basicamente el handshake esta compuesto de 2 pasos. 

1. La comunicación se inicia enviando el mensaje de versión, y el nodo con el que nos conectamos envía su propio mensaje de versión.
2. Luego, el nodo envía el mensaje verack ("verification acknowledge") confirmando la recepción de nuestra versión, y nosotros finalizamos enviando nuestro propio verack confirmando la recepción del mensaje de versión del nodo.


## Verack

El mensaje verack es un simple mensaje de encabezado sin carga útil.

# Verack Message Structure:

| Name        | Example Data | Format        | Size | Example Bytes                       |
|-------------|--------------|---------------|------|-------------------------------------|
| Magic Bytes |              | bytes         | 4    | F9 BE B4 D9                         |
| Command     | "verack"     | ascii bytes   | 12   | 76 65 72 61 63 6B 00 00 00 00 00 00 |
| Size        | 0            | little-endian | 4    | 00 00 00 00                         |
| Checksum    |              | bytes         | 4    | 5D F6 E0 E2                         |












