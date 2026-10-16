# AuftragsKompass: Zugang und Dashboard-Einträge

Die beiden Homer-Dashboards verlinken unter **Alltag & Organisation** auf dieselbe
HTTPS-Adresse: `https://auftragskompass.samuelgesang.de`.

## Stand des Testzugangs

Die Adresse führt seit 16.10.2026 auf die isolierte AuftragsKompass-Testinstallation
in CT 114. Die App verwendet ihren eigenen Login per E-Mail oder Benutzername und
Passwort. Zugangsdaten liegen ausschließlich privat außerhalb von Git.
Die Dashboard-Karte trägt den Zusatz „Testbetrieb“; echte Kundendaten wurden nicht
importiert. Passwortwechsel, Wiederherstellung und die vollständige Betriebsabnahme
sind vor Produktivbetrieb noch offen.

Caddy erreicht den Admin-Dienst auf `192.168.68.194:4177`. Eine eigene nftables-Regel
auf dem Podman-Host erlaubt diesen Port vor DNAT ausschließlich von Caddy
(`192.168.68.199`). API, Worker und Datenbank haben keine veröffentlichten Ports.
Anmeldung mit beiden Kennungen, unbefugter API-Zugriff, CSRF und Logout wurden
über TLS geprüft; die öffentliche Browser-Anmeldung funktioniert.

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

## Abnahme und weitere Freigabe

Die Caddy-Konfiguration wurde vor dem gezielten Austausch der App-Route gesichert,
mit dem vorhandenen Cloudflare-Binary validiert und neu geladen. Andere Routen und
beide Cloudflare-Connectoren blieben unverändert. Der einmalige Bootstrap-Zugang
wurde aus der installierten API-Konfiguration entfernt; Neustart und erneute
Anmeldung ohne Bootstrap-Datei und -Secret wurden geprüft. Eine erste Datenbank-
Sicherung liegt privat auf dem Host und mit geprüftem Hash auf dem Betreiberrechner.
Dies ersetzt noch keine verschlüsselte, automatische Produktivsicherung.

Ein Proxy-Login allein ersetzt keine in der App angemeldete Sitzung. Updates werden
im [App-Repository](https://github.com/gcode-de/auftragskompass/tree/codex/local-runtime-ci)
getestet und als bewusst gepinnte Docker-Hub-Images installiert.
