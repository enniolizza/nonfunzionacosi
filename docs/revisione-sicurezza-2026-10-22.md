# Revisione di sicurezza e manutenibilità — 22 ottobre 2026

Questo documento registra gli interventi del 22 ottobre. Per la successiva
riscrittura della cronologia, le note di archivio, la sitemap e la correzione
del titolo su mobile, vedere [l'aggiornamento del 23 ottobre](pulizia-cronologia-2026-10-23.md).
Le indicazioni sul PDF ancora nei rami e sulle formulazioni della home descrivono
lo stato precedente a quell'intervento.

## Esito

Il progetto esaminato è un sito statico: cinque documenti HTML, CSS incorporati
nella versione iniziale, JavaScript limitato a redirect, banner e finta
newsletter. Non sono presenti PHP, WordPress, plugin CMS, dipendenze npm,
Composer, database o API applicative nel repository. La notizia PHP2Shell
non richiede una patch PHP per questo codice o per l'esecuzione statica su
GitHub Pages. Questa conclusione non copre altri servizi eventualmente gestiti
dal proprietario, non identificati nel repository, né certifica l'infrastruttura
del fornitore.

Base esaminata: commit `230281eb986a0659544debee95bcb40c0e187f0c`, 18 aprile 2026.
Il sito pubblico risponde su `https://enniolizza.github.io/nonfunzionacosi/`.
La home ha restituito HTTP 200, riferimenti all'infrastruttura GitHub e
`Strict-Transport-Security: max-age=31556952`. Nella risposta osservata non
comparivano CSP, X-Frame-Options o X-Content-Type-Options.

## La notizia Rai e le conferme primarie

L'articolo Rai del 22 ottobre descrive l'allarme, tentativi di sfruttamento e
interruzioni precauzionali. I tentativi segnalati non provano da soli che ogni
sistema sia stato compromesso. Lo slug dell'URL parla di attesa di una
correzione, ma il testo aggiornato dice che le patch sono disponibili dal
21 ottobre: per decidere conta l'avviso del produttore.

| Vulnerabilità | Meccanismo, in sintesi | Gravità ufficiale |
| --- | --- | --- |
| CVE-2026-109618 | Un errore di memoria esaurita può lasciare dati interni della richiesta in uno stato non valido, poi usato durante la pulizia. | CVSS v4.0 9.2 |
| CVE-2026-109619 | Stato globale che sopravvive alla memoria della richiesta può essere riutilizzato da una richiesta successiva. | CVSS v4.0 9.2 |

PHP conferma la possibile esecuzione di codice senza autenticazione e considera
particolarmente esposto Apache con mod_php; l'inventario deve includere tutte
le modalità con cui PHP serve richieste web. Il problema riguarda l'interprete:
aggiornare soltanto un CMS non basta. Le versioni correttive pubblicate sono:

| Ramo | Versione correttiva minima indicata il 21 ottobre |
| --- | --- |
| 8.5 | 8.5.12 |
| 8.4 | 8.4.27 |
| 8.3 | 8.3.36 |
| 8.2 | 8.2.35 |

Per eventuali altri siti PHP, verificare la versione del processo web e gli
avvisi del distributore, non soltanto `php -v`; applicare la patch appropriata
e riavviare tutti i worker. Per rami fuori supporto, migrare o verificare un
backport mantenuto dal fornitore. Le mitigazioni temporanee sono parziali:
non equivalgono alla correzione. Se non si riesce ad aggiornare subito, isolare
i servizi vulnerabili secondo il rischio operativo. Non sono stati scaricati
né eseguiti exploit o scanner PHP sul sito.

Fonti consultate:

- [Rai News, articolo condiviso](https://www.rainews.it/articoli/2026/10/internet-siti-offline-in-europa-in-attesa-di-correzione-php-d239176a-9ccc-41ec-8ec9-0203416c84fa.html).
- [PHP, security advisory del 21 ottobre](https://www.php.net/archive/2026.php#2026-10-21-5).
- [CERT-AGID, avviso e verifiche operative](https://cert-agid.gov.it/news/due-vulnerabilita-critiche-in-php-consentono-lesecuzione-di-codice-da-remoto-rilasciati-aggiornamenti-di-sicurezza/).
- [NHS England, CC-4875](https://digital.nhs.uk/cyber-alerts/2026/cc-4875).
- [GitHub, natura statica di Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

## Rilievi e interventi

Le carenze sotto non sono prove di una compromissione già avvenuta.

| Osservazione iniziale | Intervento o stato residuo |
| --- | --- |
| Nessuna CSP nelle cinque pagine | CSP esplicita prima delle risorse; script/CSS locali; vietati inline, oggetti, frame, form e connessioni applicative |
| JavaScript inline, `onclick`, `onsubmit` e 31 stili inline | Estratti script e stili; eventi con `addEventListener`; nomi descrittivi per le varianti |
| Font caricati da Google a ogni visita | Cinzel, Playfair Display e Inter ospitati nel repository con OFL; nessuna richiesta a font/CDN di terze parti |
| Link del dossier aperti con `_blank` senza `rel` esplicito | `noopener noreferrer` uniformi; protezione aggiuntiva anche se i browser moderni applicano già implicitamente noopener in molti casi |
| Newsletter finta: conferma di successo senza registrazione | Rimossi input, form e pulsante; titolo “Newsletter in arrivo”, nessuna email raccolta |
| Link `#` a categorie e contenuti in arrivo | Categorie collegate a sezioni reali; anticipazioni non cliccabili |
| Banner con rotazione automatica e indicatori non utilizzabili da tastiera | Pulsanti, stato accessibile e navigazione manuale; tutti i pannelli leggibili senza JS |
| CSS di testata, palette e footer duplicati | Componenti comuni e CSS separato per pagina; home e manifesto riorganizzati |
| Nessun controllo di regressione nel repository | Controllo offline di link, policy e impronte editoriali; workflow con permessi minimi |
| Configurazione amministrativa separata dal codice | Checklist in `SECURITY.md`; nessuna impostazione di account o hosting modificata |

La home presenta prima i due articoli e identifica l'archivio di aprile. Colori,
immagini, riferimenti romani, orientamento e collegamenti social sono preservati.
Il testo informativo della newsletter è stato corretto; articoli e manifesto
non sono stati riscritti, aggiornati o sottoposti a
fact-checking editoriale. Le loro affermazioni, date e fonti restano quelle
originali, compresa la vecchia dicitura sul tempo reale nel dossier petrolio.

## Correzioni dopo la revisione indipendente

Il secondo intervento prosegue sopra `a52ff7e`, senza amend, merge o riscrittura
della cronologia. `tests/content-baseline.json` rimane invariato.

- Workflow: push limitati a `main` e trigger PR; `fetch-depth: 0`; controllo
  whitespace contro la base effettiva della PR o il commit precedente del push.
- Font: nove varianti richieste, otto WOFF2 per i sottoinsiemi Latin/Latin Extended,
  268.864 byte complessivi, `font-display: swap` e licenze OFL originali. Le famiglie
  sono di nuovo distinte tra testate romane, testo editoriale e interfaccia.
  Origini ufficiali e SHA-256 sono in `assets/fonts/sources.json`.
- CSP: `font-src 'self'` in tutte le pagine; controllo offline dei font, dei
  preload esterni, dei file e delle licenze; test di caricamento nel browser.
- Rimosso `Apri_Trading_in_the_Zone.pdf` dal nuovo albero del ramo, su richiesta
  del proprietario. La rimozione non cancella le copie nella cronologia né
  modifica `main` o il sito pubblico prima di un eventuale merge.
- Sitemap: `lastmod` al 22 ottobre 2026 per le cinque pagine effettivamente
  modificate. Le date di pubblicazione degli articoli restano quelle originali.
- Newsletter: presentata come servizio in arrivo, senza invito a iscriversi
  e senza pulsante inutilizzabile.

Il piano editoriale e `wyckoff_wti_v2.pdf` restano nel repository pubblico.
Il ticker e i riepiloghi della home conservano le formulazioni originali:
l'etichetta archivio non equivale a una verifica dei dati di aprile.

## PDF allegato

Il PDF `cybersecuirty_sb_factsheets_all(1).pdf` contiene 24 pagine della serie
FTC *Cybersecurity for Small Business*. I metadati riportano autore FTC e
creazione/modifica del 16 ottobre 2018. Le pagine 1-2 suggeriscono aggiornamenti,
backup e MFA; le pagine 19-20 accessi limitati e verifica dei fornitori; le
pagine 21-22 TLS e responsabilità dell'hosting. Questi principi sono pertinenti
al progetto. Il documento non è un bollettino aggiornato sulle CVE del 2026.
Le indicazioni statunitensi di denuncia e assicurazione non sono state
trasposte automaticamente al contesto italiano.

## Connettori, skill e dipendenze

È stato utilizzato il connettore GitHub già scelto dall'utente. Il controllo dei
permessi ChatGPT ha restituito l'impostazione predefinita “Allow low-risk actions”;
questa è una regola di approvazione delle operazioni, non un audit del codice
del connettore né una misura degli scope OAuth. La connessione ha consentito
lettura e preparazione di modifiche al repository. Non sono stati installati
nuovi plugin, MCP server, scanner, estensioni CMS o pacchetti di produzione.

Le skill PDF e gestione plugin forniscono procedure di lettura e controllo,
non una certificazione di sicurezza. Per il rendering locale si è usato
Playwright già presente nell'ambiente e Chrome Headless Shell dal canale
ufficiale Chrome for Testing, fuori dal repository e dal sito distribuito.
La provenienza ufficiale non equivale a una garanzia di assenza di vulnerabilità.

L'unica Action proposta è `actions/checkout` del produttore GitHub, fissata a
`d23441a48e516b6c34aea4fa41551a30e30af803` (tag v6 risolto il 22 ottobre).
Nessun segreto è richiesto. Non vengono eseguiti installatori o pacchetti npm
nella pipeline. Dependabot può proporre aggiornamenti della Action.

## Validazione e limiti

- Controllo statico su tutte le cinque pagine, asset e collegamenti interni.
- Testo normalizzato del `main` dei due articoli e del manifesto identico alla
  base Git, con confronto SHA-256; stessa sequenza delle fonti/social esterni.
- Controllo nel browser su quattro pagine a 320, 390, 768 e 1440 px: 16 combinazioni,
  senza overflow della pagina, errori JavaScript o risorse mancanti; nove varianti
  dei font caricate con successo, compresi corsivo e caratteri Latin Extended.
- Redirect, banner da tastiera, fallback senza JS e newsletter inattiva verificati.
- Prova locale di inserimento di script, gestore inline e font esterno: bloccati dalla CSP.
- Controllo mirato nel codice tracciato di pattern di chiavi private e token GitHub/AWS:
  nessuna corrispondenza; non è una scansione completa dei segreti nella cronologia.
- Nessuna prova di intrusione, esfiltrazione, exploit, invio di email o modifica
  dei post Instagram. Le modifiche sono preparate su ramo separato.

La CSP via meta non imposta una protezione anti-framing. Gli header mancanti
richiedono un livello hosting che li supporti. Nessuna impostazione di account,
MFA, DNS, recupero o pubblicazione è stata certificata tramite il controllo del
codice. Verificare questi aspetti prima di considerare concluso il lavoro
operativo di sicurezza.

## Prossime azioni del proprietario

1. Proteggere account GitHub e Instagram con MFA/passkey; rivedere autorizzazioni
   e token. Verificare la protezione del ramo `main` secondo `SECURITY.md`.
2. Esaminare la PR e il controllo `Site checks`; controllare Pages/HTTPS prima
   dell'integrazione e verificare nuovamente le pagine dopo la pubblicazione.
3. Conservare una copia indipendente e provare il ripristino.
4. Verificare che sia intenzionale rendere pubblici anche i PDF e gli appunti
   presenti nel repository: `robots.txt` non è un controllo degli accessi e
   non rende privato un file. Il PDF indicato sopra è stato rimosso dal ramo;
   non è stata riscritta la cronologia.
5. Prima di introdurre newsletter, CMS, analytics o nuove integrazioni,
   documentare utilità, permessi, dati e processo di aggiornamento.

Ulteriori riferimenti tecnici:
[OWASP CSP](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html),
[W3C WAI, carousel accessibili](https://www.w3.org/WAI/tutorials/carousels/),
[GitHub, sicurezza delle Actions](https://docs.github.com/en/actions/reference/security/secure-use),
[Google Fonts, utilizzo e stili](https://developers.google.com/fonts/docs/getting_started),
[Sitemaps, significato di lastmod](https://www.sitemaps.org/protocol.html),
[Refactoring Guru, tecniche](https://refactoring.guru/refactoring/techniques),
[Refactoring Guru, code smells](https://refactoring.guru/refactoring/smells).
