# Non Funziona Così

Sito editoriale statico pubblicato su GitHub Pages. HTML, CSS e JavaScript nativi: nessun PHP, database, CMS, framework o pacchetto npm di produzione.

## Struttura

| Percorso | Responsabilità |
| --- | --- |
| `index.html` | Ingresso con redirect HTML e link di riserva |
| `pagine/home.html` | Prima pagina e archivio degli articoli |
| `pagine/chi_siamo.html` | Manifesto originale |
| `articoli/` | Articoli, fonti e immagini originali |
| `assets/css/shared.css` | Colori, font locali, testata, footer, accessibilità |
| `assets/fonts/` | Cinzel, Playfair Display, Inter in WOFF2, licenze OFL e provenienza |
| `assets/css/home.css`, `manifesto.css` | Layout delle due pagine principali |
| `assets/css/petrolio.css`, `superbonus.css` | Componenti specifici dei dossier |
| `assets/js/carousel.js` | Navigazione manuale e accessibile dei banner |
| `scripts/check_site.py` | Verifiche offline senza dipendenze esterne |
| `tests/content-baseline.json` | Impronte del contenuto originale e collegamenti preservati |
| `docs/revisione-sicurezza-2026-10-22.md` | Analisi, fonti, limiti e interventi amministrativi |

## Anteprima locale

Dalla cartella del repository:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Aprire `http://127.0.0.1:8000/`. Il server è solo per l'anteprima locale.
La pubblicazione esistente su GitHub Pages non richiede compilazione.
Non modificare la sorgente Pages per provare il ramo di lavoro.

## Verifiche prima di pubblicare

```bash
python scripts/check_site.py
node --check assets/js/carousel.js
git diff --check
git diff --check origin/main...HEAD
```

Il primo controllo del diff riguarda le modifiche non ancora in stage; il
secondo confronta i commit del ramo con `origin/main` (aggiornare prima i ref).
La pipeline `Site checks` parte sulle PR e sui push a `main`, senza installare
pacchetti. Scarica la cronologia per controllare gli spazi nel diff tra la base
della PR e il commit verificato, oppure tra il commit precedente e quello del
push a `main`. Non usa il diff vuoto del checkout pulito.
La sola GitHub Action usata è `actions/checkout`, fissata al commit completo,
con token in sola lettura e credenziali non persistenti. Dependabot propone
aggiornamenti dell'Action: non li approva e non li integra automaticamente.

Il test browser opzionale richiede Playwright e Chromium già disponibili
nell'ambiente di sviluppo:

```bash
node tests/browser-smoke.cjs
```

Si può indicare un browser locale con `CHROME_PATH` e una cartella di screenshot
con `QA_OUTPUT`. Su PowerShell si impostano con `$env:CHROME_PATH` e
`$env:QA_OUTPUT`. Il test avvia e chiude un server locale, verifica quattro
larghezze da 320 a 1440 px, navigazione da tastiera, redirect anche senza
JavaScript, caricamento delle nove varianti dei font locali, newsletter in
arrivo e blocco reale degli script inline e dei font esterni da parte della
Content Security Policy. Questo test browser non viene installato né
eseguito dalla pipeline minimale.

## Modifiche editoriali

I testi di articoli e manifesto sono protetti da impronte del testo nel `main`
e dal confronto dei collegamenti esterni. Non rigenerare le impronte per
nascondere una regressione: aggiornarle solo dopo una modifica editoriale
intenzionale, controllando il diff rispetto alla versione precedente.
I dati degli articoli risalgono ad aprile 2026; il refactoring non costituisce
una verifica o un aggiornamento delle notizie.

Per una nuova pagina, mantenere la CSP all'inizio di `head`, utilizzare CSS e
JavaScript locali e registrare gli URL nella sitemap. Evitare stili e gestori
JavaScript inline. Non inserire chiavi, token, file privati o credenziali nel
repository: tutti i file del repository pubblico sono consultabili.
`lastmod` nella sitemap indica l'ultima modifica significativa della pagina,
anche tecnica; non sostituisce la data editoriale del testo. Le cinque pagine
sono state aggiornate il 22 ottobre 2026 per policy, stili e struttura.

I font si caricano esclusivamente dal sito con `font-src 'self'`. Provenienza,
licenze e impronte sono descritte in `assets/fonts/README.md`; il controllo
offline rifiuta font esterni e rileva modifiche ai file acquisiti.

La newsletter è esplicitamente inattiva e non raccoglie indirizzi. Attivarla
richiede una scelta separata del servizio, una verifica dei dati trattati e
una modifica mirata di `form-action` / `connect-src`; non allargare la CSP
con `*` o `unsafe-inline` per aggirare un blocco.

## Refactoring applicato

- **Extract Method**: selezione dei banner in `showSlide`, eventi registrati
  con `addEventListener`, stato confinato nel modulo.
- **Duplicate Code**: palette, testata, footer e social condivisi in un solo CSS.
- **Separazione delle responsabilità**: contenuto in HTML, presentazione in CSS,
  interazione in JavaScript. Classi descrittive sostituiscono gli stili inline.
- **Semplificazione**: rimosso il redirect JavaScript ridondante e il finto
  invio newsletter; navigazione dei banner senza timer automatico.
- **Conservazione del comportamento utile**: stessi URL degli articoli,
  immagini e fonti, lettura e collegamenti disponibili senza JavaScript.

Riferimenti: [tecniche](https://refactoring.guru/refactoring/techniques),
[code smells](https://refactoring.guru/refactoring/smells),
[Duplicate Code](https://refactoring.guru/smells/duplicate-code),
[Extract Method](https://refactoring.guru/extract-method).

## Rilascio e ripristino

Esaminare la pull request e i controlli prima di integrare in `main`.
L'integrazione potrebbe attivare la pubblicazione Pages già configurata.
Dopo il rilascio verificare home, manifesto, dossier e header HTTP dal sito
pubblico; le prove locali non attestano la configurazione remota.
Per annullare, creare una PR che esegua il revert del commit integrato:
non cancellare la cronologia e non eseguire un force push su `main`.
