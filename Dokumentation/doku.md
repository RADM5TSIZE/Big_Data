# Dokumentation

## Aufgabenstellung
Im Rahmen der Gruppenarbeit soll eine Anwendung erarbeitet werden, welche unter Berücksichtigung der in der Vorlesung vorgestellten Komponenten konzipiert und aufgebaut wird. Die Anwendungsidee und der Datensatz werden von der Gruppe selbst ausgewählt.

## Idee
Die Anwendungsidee besteht in der Verarbeitung und Visualisierung von polizeilich erfassten Verbrechen in Chicago (USA). Der Datensatz umfasst alle von dem Chicago Police Department erfassten Verbrechen im Zeitraum von 2001 bis 2017 und wurde dem System CLEAR (Citizen Law Enforcement Analysis and Reporting) entnommen. Für die Visualisierung werden ausgewählte Merkmale in Zusammenhang gebracht und graphisch in geeigneten Plots in der Webanwendung dargestellt.

## Entwurf
Bild einmal beschreiben (allgemein)
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

## Funktion
wie spielt das zusammen...wer gibt was an wen weiter etc
