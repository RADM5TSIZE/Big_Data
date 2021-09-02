Das folgende Projekt wurde für das Modul "Big Data" konzipiert:

# Mitarbeiter

- 9803923
- 6681465 
- 2512023
- 9917195
- 4151972
- 2966851

# Beschreibung Big Data Use Case
Unser Big Data Use Case stellt über eine Flask Web-Anwendung verschiedene Information zur Kriminalität in Chicago (USA) dar.
<br/>Die Flask Anwendung greift für die benötigten Daten auf eine MySQL Datenbank zu. Des Weiteren werden die Daten durch Memcached für eine bestimmte Zeit im Cache gespeichert, um so eine bessere Performance zu ermöglichen. 

# Daten
Die originalen Daten zu diesem Projekt sind unter folgendem [Link](https://www.kaggle.com/currie32/crimes-in-chicago) zu finden.

# Genuzte Software
1. spark v3.0.0
2. minikube v1.22.0 mit Kubernetes v1.21.2
3. kubectl v1.21.4
4. kafka v2.6
5. docker v20.10.8
6. mysql v1.22.1
7. flask v2.0.1

# Leitfaden

Folgenden Befehle sollten unter Berücksichtigung der jeweiligen Ordnerstruktur ausgeführt werden.

### 1. Installiere Minikube

Sollte Minikube auf der lokalen Maschine noch nicht installiert sein, befindet sich unter folgendem Link die entsprechenden [Anleitung](https://kubernetes.io/de/docs/tasks/tools/install-minikube/).

Daraufhin wird mit folgendem Befehl Minikube egestartet:

```
minikube start
```

### 2. Installiere Skaffold

Um später Skaffold nutzen zu können muss dieses auf den localen Maschine installiert sein:
Unter folgendem Link befindet sich die dazugehörige [Dokumentation](https://skaffold.dev/docs/install/).

### 3. Aktiviere ingress addon

Aktiviere die Addons mittels des Befehls: 

```
minikube addons enable ingress
```


### 4. kontext Minikube-Docker

Mittels des folgenden Befehls wird die Wiederbenutzung des Docker-Deamon in der Minikube Instanz ermöglicht.

```
eval $(minikube docker-env)
```


### 5. Starte die Cluster 

Mit den zuvor installierten Tools lässt nun die Applikation mit folgendem Befehl starten:


```
skaffold dev
```


#minikube start --addons=ingress --driver=none --memory 4096 --cpus 2 


# Screencast
[Link]()

# Dokumentation

# Aufgabenstellung
Im Rahmen der Gruppenarbeit soll eine Anwendung erarbeitet werden, welche unter Berücksichtigung der in der Vorlesung vorgestellten Komponenten konzipiert und aufgebaut wird. Die Anwendungsidee und der Datensatz werden von der Gruppe selbst ausgewählt.

# Idee
Die Anwendungsidee besteht in der Verarbeitung und Visualisierung von polizeilich erfassten Verbrechen in Chicago (USA). Der Datensatz umfasst alle von dem Chicago Police Department erfassten Verbrechen im Zeitraum von 2001 bis 2017 und wurde dem System CLEAR (Citizen Law Enforcement Analysis and Reporting) entnommen. Für die Visualisierung werden ausgewählte Merkmale in Zusammenhang gebracht und graphisch in geeigneten Plots in einer Webanwendung dargestellt.

# Entwurf
Zu Beginn liegen die Rohdaten im Data Lake. Über ein Big Data Messaging Dienst werden diese Daten an eine Big Data Processing Applikation gestreamt. Diese Applikation stellt Berechnungen auf diesen Daten an und speichert diese in der Datenbank. Wenn Nutzer dann auf die Webapp zugreifen möchten, wird dieser zur Lastverteilung über einen Load Balancer geschickt. Danach überprüft die Webapp zuerst, ob es die benötigten Daten im Cache vorliegen hat. Ist dies nicht der Fall, greift die Webapp auf die Datenbank zu und lädt die Daten und speichert sie ebenfalls im Cache.
<br/>
<br/>
![alt text](/bigdata_platform.png)

# Architektur
## Webapp
Die Webapp ist eine Flask und stellt auf verschiedenen Seiten, erreichbar über die Menübar am oberen Bildschirmrand, Information in Form von Diagrammen dar. 
Die in der Webapp dargestellten Diagramme werden mit Hilfe von Matplotlib erstellt. Für jedes Diagramm wird ein Bild erzeugt, welches dann auf den Unterseiten zur Darstellung referenziert wird.
Daten für die Diagramme werden mit Hilfe einer Anbindung an die Datenbank eingelesen. Hierfür wird mit MySQL und PyMySQL eine Verbindung zur Datenbank hergestellt.
Erreichbar ist die Webapp über den Port 5000.
## Cache
Der Cache ist über Memcached realisiert und speichert die Daten nach dem ersten Zugriff für die nächsten 30 Sekunden. Nach dieser Zeit werden die Daten wieder neu geladen. 
Innerhalb der Webapp wird das Python-Modul pymemcache genutzt. Dort wird gecheckt, ob ein Wert im Cache vorhanden ist. Falls der Wert vorhanden ist, wird er sofort aus dem Cache gezogen, falls nicht, wird die Berechnungs-Funktion aufgerufen, der Wert berechnet und aufgerufen, und außerdem im Cache gespeichert.
## Datenbank
Die Datenbank ist realsiert mit einer MySQL Datenbank und läuft in einem eigenen Container und ist über den mysql-service und dem Port 3306 erreichbar. 
## Data Lake
Der Data Lake ist über ein HDFS realisiert. 
## Big Data Messaging
Text



