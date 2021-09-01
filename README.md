# Readme

## Beschreibung Big Data Use Case
Unser Big Data Use Case stellt über eine Flask Web-Anwendung verschiedene Information zur Kriminalität in Chicago (USA) dar.
<br/>Die Flask Anwendung greift für die benötigten Daten auf eine MySQL Datenbank zu. Des Weiteren werden die Daten durch Memcached für eine bestimmte Zeit im Cache gespeichert, um so eine bessere Performance zu ermöglichen. 

## Daten
Die originalen Daten zu diesem Projekt sind unter folgendem [Link](https://www.kaggle.com/currie32/crimes-in-chicago) zu finden.

## Erforderliche Software
1. spark v
2. minikube v mit Kubernetes v
3. kubectl v
4. kafka v
5. docker v
6. mysql v
7. flask v

## Leitfaden
Schritt für Schritt um das Ding zu starten

## Screencast
[Link]()

# Dokumentation

## Aufgabenstellung
Im Rahmen der Gruppenarbeit soll eine Anwendung erarbeitet werden, welche unter Berücksichtigung der in der Vorlesung vorgestellten Komponenten konzipiert und aufgebaut wird. Die Anwendungsidee und der Datensatz werden von der Gruppe selbst ausgewählt.

## Idee
Die Anwendungsidee besteht in der Verarbeitung und Visualisierung von polizeilich erfassten Verbrechen in Chicago (USA). Der Datensatz umfasst alle von dem Chicago Police Department erfassten Verbrechen im Zeitraum von 2001 bis 2017 und wurde dem System CLEAR (Citizen Law Enforcement Analysis and Reporting) entnommen. Für die Visualisierung werden ausgewählte Merkmale in Zusammenhang gebracht und graphisch in geeigneten Plots in einer Webanwendung dargestellt.

## Entwurf
Zu Beginn liegen die Rohdaten im Data Lake. Über ein Big Data Messaging Dienst werden diese Daten an eine Big Data Processing Applikation gestreamt. Diese Applikation stellt Berechnungen auf diesen Daten an und speichert diese in der Datenbank. Wenn Nutzer dann auf die Webapp zugreifen möchten, wird dieser zur Lastverteilung über einen Load Balancer geschickt. Danach überprüft die Webapp zuerst, ob es die benötigten Daten im Cache vorliegen hat. Ist dies nicht der Fall, greift die Webapp auf die Datenbank zu und lädt die Daten und speichert sie ebenfalls im Cache.
<br/>
<br/>
![alt text](/bigdata_platform.png)

## Architektur
### Webapp
Die Webapp ist eine Flask und stellt auf verschiedenen Seiten, erreichbar über die Menübar am oberen Bildschirmrand, Information in Form von Diagrammen dar. 
### Cache
Der Cache ist über Memcached realisiert und speichert die Daten nach dem ersten Zugriff für die nächsten 30 Sekunden. Nach dieser Zeit werden die Daten wieder neu geladen. 
### Datenbank
Die Datenbank ist realsiert mit einer MySQL Datenbank und läuft in einem eigenen Container und ist über den mysql-service und dem Port 3306 erreichbar. 
### Data Lake
Der Data Lake ist über ein HDFS realisiert. 
### Big Data Messaging
- [ ] Infos Miguel



