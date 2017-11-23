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
If you have an dirmngr error —> ```sudo apt-get install dirmngr```

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
### 3. Installation of Vert.x

Download the full of Vert.x : http://vertx.io/download/

Extract and move the folder “vertx “ into “~”

Add to .bashrc
```
export PATH=$PATH:~/vertx/bin
```
Run ```source .bashrc```


### 4. Configuration of Vert.x

Go the this file ```cloudiot_cluster_vertx/core-examples/src/main/java/io/vertx/example/core/ha/Server.java``` and check if the following parameter are correct with the rabbitMQ configuration.
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

To have messages in the queue, you can use the python script under rabbitMQ/send.py.

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

The deployment of the verticle is quiet long, so be patient !

On the server, you should see in the console something like this
```
Got Message : #5771 17.4752025023 11/23/17 00:03:20
Got Message : #5772 18.0021845919 11/23/17 00:03:20
Got Message : #5773 15.6700641506 11/23/17 00:03:20
Got Message : #5774 18.4193061289 11/23/17 00:03:20
Got Message : #5775 10.5818496117 11/23/17 00:03:20
```
