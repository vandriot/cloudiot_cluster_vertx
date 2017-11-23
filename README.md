# README

## Compilation : 
“mvn clean package” à la racine du dossier 

## RPI Serveur :
Get in the core-examples/target/classes/java and execute :
vertx run io.vertx.example.core.ha.Server -ha -cp target/classes -cluster-host  [ADDRESSE_IP_RPI]

## RPI Backup :
Get in the core-examples/target/classes/java and execute :
vertx bare -cp target/classes/ -cluster-host [ADDRESSE_IP_RPI] 

## Tester :
Pour tester, ouvrir sur http://[ADDRESSE_IP_RPI]:8080
Killer le serveur avec “kill -9 [N°PID]” → on aperçoit que le serveur change de RPI (on peut trouver le PID du verticle en lançant “jps | grep Launcher”

## Référence : 
https://github.com/vert-x3/vertx-examples/tree/master/core-examples 

## Cluster vertX + rabbitMQ 
In order to make the cluster work follow this step : 

### 1. Uninstall OpenJDK and / or old version of Oracle Java 
```
sudo apt-get purge openjdk*
sudo apt-get purge java7*
sudo apt-get autoremove
```

### 2. Install latest version of Oracle Java
```
sudo apt-key adv --recv-key --keyserver keyserver.ubuntu.com EEA14886
```
If you have an dirmngr error —> `sudo apt-get install dirmngr`

Go to this file
```
sudo vim /etc/apt/sources.list
```
Add the following lines 
```
deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main
deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main
```

Install Java 
```
sudo apt-get update
sudo apt-get install oracle-java8-installer
sudo apt-get install oracle-java8-set-default
```

Check success 
```
java -version
```

Source : https://raspberrypi.stackexchange.com/questions/45976/how-do-i-update-java-8-in-raspbian

### 3. Installation of Vert.x

Download the full of Vert.x : http://vertx.io/download/

Extract and move the folder “vertx “ into “~”

Add to .bashrc
```
export PATH=$PATH:~/vertx/bin
```
Run `source .bashrc`


### 4. Configuration of Vert.x

Go the this file `cloudiot_cluster_vertx/core-examples/src/main/java/io/vertx/example/core/ha/Server.java` and check if the following parameter are correct with the rabbitMQ configuration.
```
String QUEUE_NAME = "task_queue"; // Name of the queue
// PARAMETRE DE CONNEXION RABBITMQ
RabbitMQOptions config = new RabbitMQOptions();
config.setUser("test");
config.setPassword("test");
config.setHost("10.45.0.254"); // IP address of rabbitMQ cluster
```

Next, go to ```cloudiot_cluster_vertx/core-examples/src/main/resources/cluster.xml``` and modify the IP to match your network

```xml
  <tcp-ip enabled="false">
    <interface>192.168.1.*</interface>
  </tcp-ip>
</join>
<interfaces enabled="true">
  <interface>192.168.1.*</interface>
</interfaces>
```

### 5. Configuration of rabbitMQ

Make sure you have the rabbitMQ cluster up and running with messages in the queue.

To send messages into the queue, you can use the python script under rabbitMQ/send.py.

Don't forget to change the script to match your rabbitMQ configuration.

### 6. Compile Vert.x project

If you don't want to install maven on every Raspberry Pi, on your computer run the following command 
```
mvn clean package
```

When this is done, you can upload the folder to your Raspberry Pis with scp
```
scp -r cloudiot_cluster_vertx/ pi@10.45.0.105
```

On the RPI server (one in the cluster), get in the core-examples/target/classes and execute
```
vertx run io.vertx.example.core.ha.Server -ha -cp target/classes -cluster-host [ADDRESSE_IP_RPI]
```

On the RPI backup (every other RPI, get in the core-examples/target/classes and execute
```
vertx bare -cp target/classes/ -cluster-host [ADDRESSE_IP_RPI] 
```

The deployment of the verticle is quiet long (for the server and backup), so be patient !

On the server, you should see in the console something like this
```
Got Message : #5771 17.4752025023 11/23/17 00:03:20
Got Message : #5772 18.0021845919 11/23/17 00:03:20
Got Message : #5773 15.6700641506 11/23/17 00:03:20
Got Message : #5774 18.4193061289 11/23/17 00:03:20
Got Message : #5775 10.5818496117 11/23/17 00:03:20
```

If you have an error like `io.vertx.core.impl.NoStackTraceThrowable: Not connected`, it propably means that the vertx client can't connect to the rabbitMQ cluster. 

I had this error, my rabbitMQ server was on my computer. I resolved it by doing the following action.

On every rabbitMQ server of the cluster go to `etc/rabbitmq/rabbitmq-env.conf`
If you have a line with NODE_IP_ADDRESS, remove it. Removing the NODE_IP_ADDRESS entry from the config binds the port to all network inferfaces.

Source : https://superuser.com/questions/464311/open-port-5672-tcp-for-access-to-rabbitmq-on-mac


### 7. Testing the Vert.X cluster

For example, make a Vert.X cluster with 3 nodes. Make sure you see the terminal output of Vert.X of the 3 nodes 

When the messages are being read by the server, connect via ssh to this node.

Get the PID of Vert.X with the command `top`, it should have the name "java".

Kill the processus with `kill -9 [PID]`

You should see that the Vert.X application has been redeployed on another node. 

See the demo of this test —> https://www.youtube.com/watch?v=VsiiOOSNfqs
