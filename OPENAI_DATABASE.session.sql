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
Aus diesem Grund sollen zukünftig Cloud-Technologien und -Services der <Cloud-Anbieter> eingesetzt werden, um das Kundenerlebnis für die Versicherten zu verbessern, wobei stets auf Rechtskonformität und den Schutz der persönlichen Daten geachtet wird. Zusätzlich werden schrittweise Cloud-Services in interne Prozesse integriert, und alle zukünftigen digitalen Vorhaben werden auf ihre Umsetzbarkeit mit Cloud-Lösungen überprüft.'),
('1.1', 'Zweck und Ziel des Dokumentes', 'Dieses Dokument dient dazu, gegenüber der Rechtsaufsicht nachzuweisen, wie die <Kunde> die Ziele des Datenschutzes <§ 80 SGB X> und der Informationssicherheit erreicht. Es beschreibt die technischen und organisatorischen Maßnahmen, die im Rahmen der Integrationspartnerschaft für digitale Services und KI geprüft, implementiert und weiterentwickelt werden. Ergänzend wird dargelegt, wie diese Maßnahmen kontinuierlich überwacht und angepasst werden, um den höchsten Standards hierzulande in der Datensicherheit zu entsprechen. Zudem wird erläutert, wie die Zusammenarbeit mit Partnern gestaltet wird <§ 11 BDSG> <Art. 28 DSGVO>, um den Schutz der Versichertendaten langfristig und nachhaltig zu gewährleisten.'), 
('1.2', 'Geltungsbereich', 'Dieses Dokument und die nachfolgend beschriebenen Anwendungsfälle nach <§ 393 SGB V> gelten innerhalb der <Kunde> für die Unternehmensbereiche IT Projekt- und Solutionsmanagement. Dies trägt zur Effizienz und Zielerreichung innerhalb <Kunde>.');

SELECT * FROM ANZEIGE_PRE;


-- Create table `ANZEIGE_TEMP` for Paragraph templates
DROP TABLE ANZEIGE_TEMP;
CREATE TABLE ANZEIGE_TEMP (
    PARAGRAPH       varchar(12),
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


-- Creating View
DROP VIEW paragraphs;
CREATE VIEW paragraphs AS
    SELECT ANZEIGE_PARAGRAPHS.PARAGRAPH, ANZEIGE_PARAGRAPHS_DETAILS.PARAGRAPH_DESC, ANZEIGE_PARAGRAPHS_DETAILS.PARAGRAPH_DETAILS
    FROM ANZEIGE_PARAGRAPHS
    LEFT JOIN ANZEIGE_PARAGRAPHS_DETAILS 
    ON ANZEIGE_PARAGRAPHS.PARAGRAPH = ANZEIGE_PARAGRAPHS_DETAILS.PARAGRAPH;

SELECT * FROM paragraphs;