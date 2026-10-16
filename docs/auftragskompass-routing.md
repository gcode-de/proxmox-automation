# AuftragsKompass: Zugang und Dashboard-Einträge

Die beiden Homer-Dashboards verlinken unter **Alltag & Organisation** auf dieselbe
HTTPS-Adresse: `https://auftragskompass.samuelgesang.de`.

## Stand des Testzugangs

Der Zugang zeigt vorerst eine Einrichtungsnachricht mit HTTP 503 und `no-store`.
Die App-Anmeldung ist noch nicht entschieden; es wird keine Verwaltungs-API
veröffentlicht. Die Dashboard-Karte trägt entsprechend den Zusatz „Einrichtung“.
Das ist noch keine laufende oder für Geschäftsdaten freigegebene App.

Der [Caddy-Block](../files/caddy/auftragskompass.caddy) gehört in den bestehenden
Wildcard-Serverblock auf CT 120, vor dessen abschließende 404-Antwort. Vor Änderungen
die bestehende Datei sichern, die vollständige Konfiguration mit `/usr/local/bin/caddy-cloudflare` und Caddys
vorhandener Umgebungsdatei prüfen und anschließend Caddy neu laden. Keine TLS-Secrets in Git.

Der bestehende Cloudflare Tunnel hat zwei aktive Connectoren (CT 119 und CT 121).
Beide benötigen diesen Ingress-Eintrag vor dem Catch-all. Die DNS-Route wird einmal
mit der vorhandenen `cfhost`-Verwaltung angelegt:

```yaml
- hostname: auftragskompass.samuelgesang.de
  service: https://192.168.68.199
  originRequest:
    originServerName: auftragskompass.samuelgesang.de
    httpHostHeader: auftragskompass.samuelgesang.de
```

Die TLS-Prüfung bleibt aktiv. Der Servername und Host-Header sind erforderlich,
weil Caddy über seine IP angesprochen wird und ein Zertifikat für die Domain nutzt.
Tunnel-Konfiguration und Credentials verbleiben auf dem Host. Die vorhandene
Verwaltung sichert und validiert die Konfiguration vor dem Neustart; keine Änderung
an anderen Ingress-Einträgen. `cfhost` aktualisiert derzeit nur CT 119. Deshalb muss
die Regel auch auf CT 121 mit eigenem Backup und nativer Ingress-Validierung
ergänzt werden; andernfalls liefert ein Teil der Anfragen weiterhin 404. Keine
komplette Konfiguration zwischen Connectoren kopieren.

## Homer-Synchronisierung

Die Quellen liegen in `homer-config_remote.yml` und `homer-config_local.yml` auf
`main` dieses Repositories. Beide Homer-Container verwenden das vorhandene Skript
`/usr/local/bin/homer-update-config.sh`, das die jeweilige GitHub-Datei lädt und die
vorherige Konfiguration sichert. Der Remote-Homer läuft in CT 110, der lokale in
CT 105; der jeweils aktuelle Proxmox-Knoten ist vor dem Aufruf zu prüfen.

## Spätere App-Freigabe

Nach eingerichtetem und geprüftem App-Login den Caddy-Block gezielt auf den
AuftragsKompass-Admin-Dienst umstellen. Datenbank und Worker erhalten keine
öffentlichen Ports. Zuerst erlaubten und unerlaubten Zugriff über die HTTPS-Adresse
testen; dann „Einrichtung“ auf den Dashboard-Karten entfernen. Ein Proxy-Login allein
ersetzt keine in der App angemeldete Sitzung.
