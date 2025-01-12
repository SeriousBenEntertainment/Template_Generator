// Drop secret key
ALTER USER bengross_tech UNSET RSA_PUBLIC_KEY;


-- Creating a database in Snowflake 
CREATE DATABASE OPENAI_DATABASE;
CREATE SCHEMA PUBLIC;


-- Creating table `ANZEIGE_PRE` for Paragraph pre-samples
DROP TABLE ANZEIGE_PRE;
CREATE TABLE ANZEIGE_PRE (
    PARAGRAPH       varchar(12),
    PARAGRAPH_TITLE varchar(200),
    PARAGRAPH_TEXT  varchar(20000)
);

INSERT INTO ANZEIGE_PRE VALUES
('1', 'Einleitung in die Thematik', '<Kunde> <Kundeninfo> Selbstentwickelte Programme und Dienstleistungen sind wesentliche Bestandteile des Kerngeschäfts einer Krankenkasse und spielen eine wichtige Rolle bei der Digitalisierung im Bereich der Gesetzlichen Krankenversicherung. Der Schwerpunkt verlagert sich mehr und mehr auf papierlose Prozesse sowie digitale Services und Produkte, wodurch diese Entwicklungen die Versicherten stärker einbeziehen. Zukünftig werden die Anforderungen an die IT und die digitalen Produkte der Kassen an vielen Stellen flexibler und leistungsfähiger aus der Cloud heraus als aus herkömmlichen Rechenzentren erfüllt werden können.
Aus diesem Grund sollen zukünftig Cloud-Technologien und -Services der <Cloud-Anbieter> vom Anbieter <option_0_0> eingesetzt werden, um das Kundenerlebnis für die Versicherten zu verbessern, wobei stets auf Rechtskonformität und den Schutz der persönlichen Daten geachtet wird. Zusätzlich werden schrittweise Cloud-Services in interne Prozesse integriert, und alle zukünftigen digitalen Vorhaben werden auf ihre Umsetzbarkeit mit Cloud-Lösungen überprüft.'),
('1.1', 'Zweck und Ziel des Dokumentes', 'Dieses Dokument dient dazu, gegenüber der Rechtsaufsicht nachzuweisen, wie die <Kunde> die Ziele des Datenschutzes <§ 80 SGB X> und der Informationssicherheit (<option_3_42>, <option_3_43>) erreicht. Es beschreibt die technischen und organisatorischen Maßnahmen, die im Rahmen der Integrationspartnerschaft für digitale Services und KI geprüft, implementiert und weiterentwickelt werden. Ergänzend wird dargelegt, wie diese Maßnahmen kontinuierlich überwacht und angepasst werden, um den höchsten Standards hierzulande in der Datensicherheit zu entsprechen. Zudem wird erläutert, wie die Zusammenarbeit mit Partnern gestaltet wird <§ 11 BDSG> <Art. 28 DSGVO>, um den Schutz der Versichertendaten langfristig und nachhaltig zu gewährleisten.'), 
('1.2', 'Geltungsbereich', 'Dieses Dokument und die nachfolgend beschriebenen Anwendungsfälle nach <§ 393 SGB V> gelten innerhalb der <Kunde> für die Unternehmensbereiche IT Projekt- und Solutionsmanagement. Dies trägt zur Effizienz und Zielerreichung innerhalb <Kunde>.'),
('1.3', 'Anwendungsbereich', '1.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('1.3.1', 'Anwendungsfälle', '1.3.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('1.3.2', 'Geschäftsnutzen', '1.3.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2', 'Rechtliche Grundlagen', '2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.1', 'Verarbeitung von Sozialdaten im Auftrag ($ 80 SGB X)', '2.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.2', 'Auftragsverarbeiter', '2.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.3', 'Cloud-Einsatz im deutschen Gesundheitswesen ($ 391 Abs. 1 SGB V)', '2.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.4', 'Datenschutz und Datensicherheit', '2.4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.4.1', 'Datenkategorien und deren Schutzbedarf', '2.4.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.4.2', 'Vereinbarung zur Auftragsverarbeitung', '2.4.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.4.3', 'Datenschutz-Folgenabschätzung', '2.4.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.4.4', 'Räumliche Beschränkung der Datenverarbeitung', '2.4.4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('2.4.5', 'Sicherheit der Datenverarbeitung', '2.4.5 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3', 'Zentrale Aspekte der Nutzung von Cloud-Computing', '3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.1', 'Definition und Zweck des Cloud-Computing', '3.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.2', 'Aufgabenbezug', '3.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.3', 'Wirtschaftlichkeitsbetrachtung', '3.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.4', 'Vermeidung des Vendor Lock-In', '3.4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.4.1', 'Cloud-Agnostik', '3.4.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.4.2', 'Multi-Cloud-Ansatz', '3.4.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.4.3', 'Verwendung Drittanbieterprodukte', '3.4.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.4.4', 'Heterogene IT-Umgebung', '3.4.4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('3.5', 'Exit-Strategie', '3.5 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4', 'Cloud-Sicherheitskonzept', '4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.1', 'Beschreibung des Datenflusses', '4.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.2', 'Identität und Zugriff', '4.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.2.1', 'Least-Privilege-Prinzip', '4.2.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.2.2', 'Multifactor Authentification', '4.2.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.3', 'Rollen und Berechtigungen', '4.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.3.1', 'Berechtigungsgruppen', '4.3.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.3.2', 'Rollenzuweisungen', '4.3.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.3.3', 'Administration von Privileged Identity Management', '4.3.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.3.4', 'Benutzerverwaltung', '4.3.4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.4', 'Verschlüsselung von Daten', '4.4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.4.1', 'Verschlüsselung ruhender Daten', '4.4.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.4.2', 'Customer Managed Keys', '4.4.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.4.3', 'Google Key Vauld', '4.4.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.4.4', 'Verschlüsselung von Übertragungsdaten', '4.4.4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.4.5', 'Verschlüsselung beim Datentransport', '4.4.5 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.5', 'Netzwerk', '4.5 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.5.1', 'Network Security Groups', '4.5.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.5.2', 'Virtual Networks', '4.5.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.5.3', 'Private Endpoints', '4.5.3 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.5.4', 'VPN-Gateway', '4.5.4 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.5.5', 'Private DNS Resolver', '4.5.5 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.5.6', 'Schutz vor Distributed Denial of Service', '4.5.6 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.5.7', 'Firewallfreigaben und Berechtigungskonzept', '4.5.7 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.6', 'Monitoring und Logging', '4.6 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.7', 'Google Policies', '4.7 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('4.8', 'Weitere Services', '4.8 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('5', 'Zertifizierungen', '5 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('5.1', 'C5-Zertifizierung', '5.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
('5.2', 'ISO 27001', '5.2 Lorem ipsum dolor sit amet, consectetur adipiscing elit');

SELECT * FROM ANZEIGE_PRE;


-- Create table `ANZEIGE_TEMP` for Paragraph templates
DROP TABLE ANZEIGE_TEMP;
CREATE TABLE ANZEIGE_TEMP (
    PARAGRAPH       varchar(12),
    PARAGRAPH_TITLE varchar(200),
    PARAGRAPH_TEXT  varchar(20000)
);

SELECT * FROM ANZEIGE_TEMP;


-- Create table `ANZEIGE_PARAGRAPHS` for Paragraph templates from URL
DROP TABLE ANZEIGE_PARAGRAPHS;
CREATE TABLE ANZEIGE_PARAGRAPHS (
    PARAGRAPH       varchar(20),
    PARAGRAPH_DESC  varchar(80),
    PARAGRAPH_URL  varchar(400)
);

INSERT INTO ANZEIGE_PARAGRAPHS VALUES
('§ 80 SGB X', 'Verarbeitung von Sozialdaten im Auftrag', 'https://www.gesetze-im-internet.de/sgb_10/__80.html'),
('§ 11 BDSG', 'Erhebung, Verarbeitung oder Nutzung personenbezogener Daten im Auftrag', 'https://dejure.org/gesetze/BDSG_a.F./11.html'),
('Art. 28 DSGVO', 'Auftragsverarbeiter', 'https://dejure.org/gesetze/DSGVO/28.html'),
('§ 393 SGB V', 'Cloud-Einsatz im Gesundheitswesen & Verordnungsermächtigung', 'https://dejure.org/gesetze/SGB_V/393.html');

SELECT * FROM ANZEIGE_PARAGRAPHS;


-- Create table `ANZEIGE_PARAGRAPHS_DETAILS` for Paragraph templates
DROP TABLE ANZEIGE_PARAGRAPHS_DETAILS;
CREATE TABLE ANZEIGE_PARAGRAPHS_DETAILS (
    PARAGRAPH       varchar(20),
    PARAGRAPH_DESC  varchar(80),
    PARAGRAPH_DETAILS  varchar(8000)
);

INSERT INTO ANZEIGE_PARAGRAPHS_DETAILS VALUES
('§ 80 SGB X', 'Verarbeitung von Sozialdaten im Auftrag', 'Die Erteilung eines Auftrags im Sinne des Artikels 28 der Verordnung (EU) 2016/679 zur Verarbeitung von Sozialdaten ist nur zulässig, wenn der Verantwortliche seiner Rechts- oder Fachaufsichtsbehörde rechtzeitig vor der Auftragserteilung 1. den Auftragsverarbeiter, die bei diesem vorhandenen technischen und organisatorischen Maßnahmen und ergänzenden Weisungen, 2. die Art der Daten, die im Auftrag verarbeitet werden sollen, und den Kreis der betroffenen Personen, 3. die Aufgabe, zu deren Erfüllung die Verarbeitung der Daten im Auftrag erfolgen soll, sowie 4. den Abschluss von etwaigen Unterauftragsverhältnissen schriftlich oder elektronisch anzeigt. Soll eine öffentliche Stelle mit der Verarbeitung von Sozialdaten beauftragt werden, hat diese rechtzeitig vor der Auftragserteilung die beabsichtigte Beauftragung ihrer Rechts- oder Fachaufsichtsbehörde schriftlich oder elektronisch anzuzeigen.'),
('§ 11 BDSG', 'Erhebung, Verarbeitung oder Nutzung personenbezogener Daten im Auftrag', 'Werden personenbezogene Daten im Auftrag durch andere Stellen erhoben, verarbeitet oder genutzt, ist der Auftraggeber für die Einhaltung der Vorschriften dieses Gesetzes und anderer Vorschriften über den Datenschutz verantwortlich. 2Die in den §§ 6, 7 und 8 genannten Rechte sind ihm gegenüber geltend zu machen. Der Auftragnehmer ist unter besonderer Berücksichtigung der Eignung der von ihm getroffenen technischen und organisatorischen Maßnahmen sorgfältig auszuwählen.'),
('Art. 28 DSGVO', 'Auftragsverarbeiter', '1. Erfolgt eine Verarbeitung im Auftrag eines Verantwortlichen, so arbeitet dieser nur mit Auftragsverarbeitern, die hinreichend Garantien dafür bieten, dass geeignete technische und organisatorische Maßnahmen so durchgeführt werden, dass die Verarbeitung im Einklang mit den Anforderungen dieser Verordnung erfolgt und den Schutz der Rechte der betroffenen Person gewährleistet. 2. Der Auftragsverarbeiter nimmt keinen weiteren Auftragsverarbeiter ohne vorherige gesonderte oder allgemeine schriftliche Genehmigung des Verantwortlichen in Anspruch. Im Fall einer allgemeinen schriftlichen Genehmigung informiert der Auftragsverarbeiter den Verantwortlichen immer über jede beabsichtigte Änderung in Bezug auf die Hinzuziehung oder die Ersetzung anderer Auftragsverarbeiter, wodurch der Verantwortliche die Möglichkeit erhält, gegen derartige Änderungen Einspruch zu erheben. 3. Die Verarbeitung durch einen Auftragsverarbeiter erfolgt auf der Grundlage eines Vertrags oder eines anderen Rechtsinstruments nach dem Unionsrecht oder dem Recht der Mitgliedstaaten, der bzw. das den Auftragsverarbeiter in Bezug auf den Verantwortlichen bindet und in dem Gegenstand und Dauer der Verarbeitung, Art und Zweck der Verarbeitung, die Art der personenbezogenen Daten, die Kategorien betroffener Personen und die Pflichten und Rechte des Verantwortlichen festgelegt sind.'),
('§ 393 SGB V', 'Cloud-Einsatz im Gesundheitswesen & Verordnungsermächtigung', '1. Leistungserbringer im Sinne des Vierten Kapitels und Kranken- und Pflegekassen sowie ihre jeweiligen Auftragsdatenverarbeiter dürfen Sozialdaten und Gesundheitsdaten auch im Wege des Cloud-Computing-Dienstes verarbeiten, sofern die Voraussetzungen der Absätze 2 bis 4 erfüllt sind. 2. Die Verarbeitung von Sozial- und Gesundheitsdaten im Wege des Cloud-Computing-Dienstes darf nur im Inland, in einem Mitgliedstaat der Europäischen Union oder in einem diesem nach § 35 Absatz 7 des Ersten Buches gleichgestellten Staat oder, sofern ein Angemessenheitsbeschluss gemäß Artikel 45 der Verordnung (EU) 679/2016 vorliegt, in einem Drittstaat erfolgen und sofern die datenverarbeitende Stelle über eine Niederlassung im Inland verfügt. 3. Eine Verarbeitung nach Absatz 1 ist nur zulässig, wenn zusätzlich zu den Anforderungen des Absatzes 2 nach dem Stand der Technik angemessene technische und organisatorische Maßnahmen zur Gewährleistung der Informationssicherheit ergriffen worden sind, ein aktuelles C5-Testat der datenverarbeitenden Stelle im Hinblick auf die C5-Basiskriterien für die im Rahmen des Cloud-Computing-Dienstes eingesetzten Cloud-Systeme und die eingesetzte Technik vorliegt und die im Prüfbericht des Testats enthaltenen, korrespondierenden Kriterien für Kunden umgesetzt sind.
4. Bis zum 30. Juni 2025 gilt als aktuelles C5-Testat im Sinne des Absatzes 3 Nummer 2 ein C5-Typ1-Testat. 2Ab dem 1. Juli 2025 gilt als aktuelles C5-Testat im Sinne des Absatzes 3 Nummer 2 ein aktuelles C5-Typ2-Testat. 3. Eine Verarbeitung nach Absatz 3 Nummer 2 ist ferner auch zulässig, soweit für die im Rahmen des Cloud-Computing-Dienstes eingesetzten Cloud-Systeme und die Cloud-Technik anstelle eines aktuellen C5-Testats ein Testat oder Zertifikat nach einem Standard vorliegt, dessen Befolgung ein im Vergleich zum C5-Standard vergleichbares oder höheres Sicherheitsniveau sicherstellt. 4. Das Bundesministerium für Gesundheit wird ermächtigt, durch Rechtsverordnung ohne Zustimmung des Bundesrates im Einvernehmen mit dem Bundesamt für Sicherheit in der Informationstechnik festzulegen, welche Standards die Anforderungen nach Satz 3 erfüllen. 5. Technische und organisatorische Maßnahmen gelten als angemessen im Sinne von Absatz 3 Nummer 1, wenn folgende Anforderungen erfüllt werden. 6. In allen anderen Fällen gelten technische und organisatorische Maßnahmen als angemessen im Sinne von Absatz 3 Nummer 1, wenn sie gleichwertig zu den Anforderungen nach § 391 sind. 2Der Angemessenheitsmaßstab nach Satz 1 gilt nicht, soweit Verarbeiter nach Absatz 1 ohnehin als Betreiber Kritischer Infrastrukturen gemäß § 8a des BSI-Gesetzes angemessene technische Vorkehrungen zu treffen haben. 7. Informationen über die nach Absatz 3 Nummer 2 testierten Cloud-Systeme und testierte Cloud-Technik werden von dem Kompetenzzentrum für Interoperabilität im Gesundheitswesen auf der Plattform nach § 385 Absatz 1 Satz 2 Nummer 5 auf Antrag veröffentlicht. 2Dem Antrag nach Satz 1 ist eine Kontrollliste zu den korrespondierenden Kriterien für Kunden anzufügen. 8. Die Vorschriften des Zehnten Buches und des Bundesdatenschutzgesetzes bleiben unberührt.');

SELECT * FROM ANZEIGE_PARAGRAPHS_DETAILS;


-- Create table `ANZEIGE_OPTIONS` for Options values
DROP TABLE ANZEIGE_OPTIONS;
CREATE TABLE ANZEIGE_OPTIONS(
    OPTION_DESC  varchar(20),
    OPTION_TEXT  varchar(4000)
);

INSERT INTO ANZEIGE_OPTIONS VALUES
('option_0_0', 'Google LLC'),
('option_1_0a', 'True'),
('option_1_0b', 'False'),
('option_1_1', 'Versichertendaten'),
('option_1_2', 'Versicherte'),
('option_1_3', 'Die Versichertendaten werden zur weiteren Bearbeitung temporär in der Cloud gespeichert.'),
('option_2_0', 'False'),
('option_3_0', 'True'),
('option_3_1', 'Versichertendaten'),
('option_3_2', 'Abrechnungserstellung'),
('option_3_3', 'True'),
('option_3_4', 'Versichertendaten'),
('option_3_5', 'Abrechnungserstellung'),
('option_3_6', 'False'),
('option_3_7', 'True'),
('option_3_8', 'Versichertendaten'),
('option_3_9', 'Abrechnungserstellung'),
('option_3_10', 'True'),
('option_3_11', 'False'),
('option_3_12', 'True'),
('option_3_13', 'False'),
('option_3_14', 'True'),
('option_3_15', 'False'),
('option_3_16', 'True'),
('option_3_17', 'False'),
('option_3_18', 'False'),
('option_3_19', 'False'),
('option_3_20', 'True'),
('option_3_21', 'False'),
('option_3_22', 'False'),
('option_3_23', 'True'),
('option_3_24', 'Im Design der Landing Zone werden die Elemente wie Netzwerke, Identitäts- und Zugriffsmanagement, Sicherheitsrichtlinien und Überwachungsdienste integriert. Für die Implementierung werden vordefinierte Lösungen genutzt werden, die den Einstieg erleichtern und Best Practices der Branche widerspiegeln.'),
('option_3_25', 'True'),
('option_3_26', 'Innerhalb der Landing Zone werden Identitäten und Zugriffsrechte durch ein zentrales Identitäts- und Zugriffsmanagementsystem verwaltet, das auf Identity and Access Management (IAM) basiert.'),
('option_3_27', 'True'),
('option_3_28', 'Maßnahmen zur Datenhoheit und Standortwahl. Die Daten werden verschlüsselungstechnisch geschützt. Verträge und Zertifizierungen (Compliance-Zertifizierungen). Transparenzberichte und Kundenbenachrichtigungen. Die Sicherheitspraktiken und Compliance wird regelmäßig von unabhängigen Dritten überprüft. Datenschutz- und Sicherheitszentrum.'),
('option_3_29', 'Durch gezielte Datenlokalisierung und Regionenauswahl. Mit Standardvertragsklauseln sowie zusätzliche Sicherheitsmaßnahmen. Dazu kommen Datenschutzbewertungen und Risikomanagement. Außerdem mittels Transparenz und Verantwortlichkeitsmanagement.'),
('option_3_30', 'Durch die Datenlokalisierung und Regionenauswahl. Vertragsvereinbarungen mit dem Anbieter. Einsatz von Verschlüsselung. Zugriffs- und Sicherheitskontrollen. Regelmäßige Überprüfung und Audits. Verpflichtung zur Benachrichtigung.'),
('option_3_31', 'Standardvertragsklauseln (SCCs). Zusätzliche technische, organisatorische und vertragliche Schutzmaßnahmen. Datenlokalisierung (Speicherung und Verarbeitung der Daten ausschließlich innerhalb der EU). Individuelle Risikobewertung für jede Datenübermittlung in ein Drittland durchführen. Klare Klauseln enthalten, die die Datenverarbeitung regeln.'),
('option_3_32', 'Daten ausschließlich in der EU oder anderen Regionen. Verschlüsselung. Challenging Government Requests. Zero Trust Architecture. Transparenzberichte. Anwendung der Standardvertragsklauseln (SCCs).'),
('option_3_33', 'Datenkontrolle und -speicherung. Verschlüsselung und Schlüsselverwaltung. Vertragliche Verpflichtungen. Transparenz und Kontrolle. Souveräne Cloud-Lösungen.'),
('option_3_34', 'Datenlokalisierung und -kontrolle. Verschlüsselung und Schlüsselverwaltung. Vertragliche Verpflichtungen. Transparenz und Kontrolle. Spezifische Compliance-Programme.'),
('option_3_35', 'Datenlokalisierung und -kontrolle. Verschlüsselung und Schlüsselverwaltung. Vertragliche Verpflichtungen. Transparenz und Kontrolle. Spezifische Compliance-Programme.'),
('option_3_36', 'Google Cloud Compliance Manager. Verschlüsselung und Schlüsselverwaltung. Audit-Logs und Überwachung. Datenschutz-Folgenabschätzung (DPIA). Vertragliche Verpflichtungen und Zertifizierungen.'),
('option_3_37', 'Google Kubernetes Engine (GKE). Compute Engine. Cloud Storage. Cloud Load Balancing. Cloud SQL und Cloud Spanner.'),
('option_3_38', 'Google Cloud Storage. Google Cloud Backup and DR. Google Cloud Spanner. Google Kubernetes Engine (GKE). Cloud Load Balancing'),
('option_3_39', 'Interoperabilität und offene Standards. Multi-Cloud-Management-Tools. Datenmigrationstools. Containerisierung. Vertragliche Flexibilität.'),
('option_3_40', 'True'),
('option_3_41', 'Identity and Access Management (IAM). VPC Service Controls. Cloud Audit Logs. Access Transparency. Policy Intelligence.'),
('option_3_42', 'Zugriffskontrolle und Authentifizierung. Verschlüsselung. Überwachung und Auditierung. Netzwerksicherheit. Schulung und Sensibilisierung. Zero-Trust-Architektur.'),
('option_3_43', 'Zertifizierungen und Audits. Physische Sicherheitskontrollen. Zugangsprotokolle und Überwachung. Regelmäßige Audits und Inspektionen. Zusammenarbeit mit dem Rechenzentrumsanbieter.'),
('option_3_44', 'Zertifizierungen und Audits. Physische Sicherheitskontrollen. Zugangsprotokolle und Überwachung. Regelmäßige Audits und Inspektionen. Zusammenarbeit mit dem Rechenzentrumsanbieter.'),
('option_3_45', 'True'),
('option_3_46', 'True'),
('option_3_47', 'Diese Protokollierung erfolgt in sogenannten Audit-Logs und Zugriffprotokollen, die aufzeichnen, wer wann welche Änderungen an den Daten vorgenommen hat.'),
('option_3_48', 'Datenexport mitels APIs zur Verfügung. Datenzugriff für einen begrenzten Zeitraum nach Vertragsbeendigung. Datenlöschung nach der Beendigung des Vertrags. Unterstützung bei der Migration.'),
('option_3_49', 'Datenmigration, Datenexport und Datenlöschung'),
('option_3_50', 'Datenlöschungsprozess, Zertifizierung und Nachweis (Löschbestätigung und Audit-Logs).'),
('option_3_51', 'Zugriffskontrolle und Authentifizierung. Verschlüsselung. Überwachung und Auditierung. Netzwerksicherheit. Zero-Trust-Architektur. Schulung und Sensibilisierung.'),
('option_3_52', 'Daten werden im Ruhezustand standardmäßig mit AES-256 verschlüsselt. Daten werden während der Übertragung zwischen den Systemen verschlüsselt mittels TLS (Transport Layer Security). Mit Confidential Computing und Confidential VMs bleiben Daten auch während der Verarbeitung verschlüsselt.'),
('option_3_53', 'TLS (Transport Layer Security). IPSec-Tunnel. Managed SSL-Zertifikate. Verschlüsselung von VM-zu-VM-Datenverkehr.'),
('option_3_54', 'Confidential Computing und Confidential VMs werden Daten in-use verschlüsselt.'),
('option_3_55', '2'),
('option_3_56', 'Verschlüsselung at-rest. Verschlüsselung in-transit. Verschlüsselung in-use. KMS Schlüsselmanagement');

SELECT * FROM ANZEIGE_OPTIONS;


-- Creating View
DROP VIEW paragraphs;
CREATE VIEW paragraphs AS
    SELECT ANZEIGE_PARAGRAPHS.PARAGRAPH, ANZEIGE_PARAGRAPHS_DETAILS.PARAGRAPH_DESC, ANZEIGE_PARAGRAPHS_DETAILS.PARAGRAPH_DETAILS
    FROM ANZEIGE_PARAGRAPHS
    LEFT JOIN ANZEIGE_PARAGRAPHS_DETAILS 
    ON ANZEIGE_PARAGRAPHS.PARAGRAPH = ANZEIGE_PARAGRAPHS_DETAILS.PARAGRAPH;

SELECT * FROM paragraphs;


-- Misc
// Change default warehouse BJA51215.LR72456
USE warehouse "WH_Health_UseCase_AI";
ALTER USER LR72456 SET default_warehouse = "WH_Health_UseCase_AI";

// List Stages in DB
SHOW STAGES;

// List Files in Stage
SELECT DISTINCT METADATA$FILENAME FROM @GOOGLE_CLOUD;
SELECT DISTINCT METADATA$FILENAME FROM @TEMPLATEGENERATOR;

// Cortex AI
// Models
//mistral-large
//llama2-70b-chat
//llama3-8b
//llama3.1-8b
SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', 'Wie kann ich meine Daten in der Cloud sicher speichern?');
// https://quickstarts.snowflake.com/guide/getting_started_with_synthetic_data_and_distillation_for_llms/
CREATE OR REPLACE TABLE support_ticket_category (
  category string
);

INSERT INTO support_ticket_category (category) VALUES 
  ('Roaming fees'), 
  ('Slow data speed'), 
  ('Lost phone'), 
  ('Add new line'), 
  ('Closing account');

// In this step we prompt the LLM to generate 25 synthetic examples of customer support tickets for every category.
CREATE or REPLACE TABLE support_tickets AS (
    SELECT 
      category, 
      TRY_PARSE_JSON(
        SNOWFLAKE.CORTEX.COMPLETE(
          'mistral-large',
          CONCAT(
            'Bitte erstelle 25 Beispiele eines Kunden Anrufs in eines Telekommunikationsanbieters für die folgenden Kategorien:', category, 'Gebe detaillierte und realistische Szenarien vor, denen Kundendienstmitarbeiter begegnen könnten. Stelle sicher, dass die Beispiele vielfältig sind und verschiedene Situationen innerhalb jeder Kategorie abdecken. Bitte füge die Beispiele in eine JSON-Liste ein. Jedes Element der JSON-Liste sollte Folgendes enthalten: {"scenario": <Szenario>, "request": <detaillierte Anfrage des Kunden, die in der Regel weniger als 3 Sätze umfasst>}. Die Ausgabe sollte nur JSON und keine anderen Wörter enthalten.'))) AS tickets
    FROM support_ticket_category
);
SELECT * FROM support_tickets;

// The table support_tickets now contains our synthetic data but the data format is a bit inconvenient as each row contains multiple support tickets. To flatten the data we run
CREATE OR REPLACE TABLE flatten_support_tickets AS (
SELECT
    category, 
    abs(hash(value:request)) % 10000000 AS id,
    value:request AS request, 
    value:scenario AS scenario
FROM support_tickets, LATERAL flatten(input => tickets) 
);
// We now have a table flatten_support_tickets with one ticket per row. We also generated unique IDs for each ticket.
SELECT * FROM flatten_support_tickets;

// We want to make sure our data is of high quality. Again, we can use an LLM to help us with this task. Instead of prompting the LLM to generate the support tickets, we now ask the LLM to rate the synthetic data for two criteria: We want the tickets to be (1) realistic and (2) valid.
CREATE OR REPLACE TABLE rate_support_tickets as (
    SELECT category, id, request, scenario, TRY_PARSE_JSON(SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large', 
        CONCAT('Du beurteilst, ob ein Support-Ticket, das bei einem Telekommunikationsunternehmen eingegangen ist, realistisch und gültig ist. Bitte gebe Noten von 1 bis 5 für jede Kategorie und geben eine endgültige Empfehlung für die gegebene Frage. Supportanfrage: ', request, ' Bitte gebe die Punktzahl (5 hoch, 1 niedrig) allein im JSON-Format nach diesem Beispiel an: „{„trust“: <Punktzahl>}“. Füge den Grund für das Ergebnis in JSON als „reason“: <Grund> ein. Nehme nur JSON {z.B. {"trust": 1, "reason": "Die Anfrage ist realistisch und gültig, da Roaming-Gebühren im Ausland oft höher sind als erwartet."} in die Ausgabe auf und keine anderen Wörter.'))) AS rating
    FROM flatten_support_tickets
);
SELECT * FROM rate_support_tickets;

// Now we can filter out examples that are below the bar for realistic or valid. We create the filtered_support_tickets table for the next steps.
CREATE OR REPLACE TABLE filtered_support_tickets AS (
    SELECT * FROM rate_support_tickets WHERE rating['trust'] <= 3
);

// First, let's use Snowflake Cortex AI COMPLETE() to categorize the support tickets into our categories – Roaming Fees, Slow data speed, Add new line, Closing account and more.
//We can use any Cortex AI supported model under the hood to invoke the COMPLETE() function. In this quickstart, let's use llama3.1-405b and use the following prompt.
CREATE OR REPLACE FUNCTION CATEGORIZE_PROMPT_TEMPLATE(request STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
CONCAT('You are an agent that helps organize requests that come to our support team. 

The request category is the reason why the customer reached out. These are the possible types of request categories:

Roaming fees
Slow data speed
Lost phone
Add new line
Closing account

Try doing it for this request and return only the request category only.

request: ', request)
$$
;

// Using a powerful and large language model such as llama3.1-405b might be highly accurate without doing any complex customizations but running llama3.1-405b on millions of support tickets comes with a cost. So, let's try the same COMPLETE() function with the same prompt but this time with a smaller model such as llama3.1-8b.
SELECT id, SNOWFLAKE.CORTEX.COMPLETE(
    'llama3.1-8b', 
    CATEGORIZE_PROMPT_TEMPLATE(request)
    ) FROM filtered_support_tickets;

// We now split the data into a training and validation portion. We want to use 20% of the data for validation and the remaining 80% for training. To get a reproducible data split between runs, we use the unique ID we to determine if a ticket is part of the training portion or the validation portion:
CREATE OR REPLACE TABLE training_data AS (
    SELECT * FROM filtered_support_tickets WHERE ID % 10 < 8 
);
SELECT * FROM filtered_support_tickets;

CREATE OR REPLACE TABLE validation_data AS (
    SELECT * FROM filtered_support_tickets WHERE ID % 10 >= 8 
);
SELECT * FROM validation_data;