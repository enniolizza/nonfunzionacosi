# Sicurezza

## Superficie esposta

Questo repository serve file statici su GitHub Pages. Non contiene interpreti
PHP, API applicative, autenticazione del lettore, database, moduli attivi o
script remoti. I rischi principali sono compromissione dell'account GitHub,
modifiche non autorizzate ai contenuti, configurazione di pubblicazione e
future dipendenze. La Content Security Policy riduce l'esecuzione di codice
iniettato; non protegge un repository sul quale un attaccante ha già ottenuto
permessi di scrittura e può modificare anche la policy.

## Controlli nel codice

- Risorse eseguibili, immagini e font WOFF2 locali; nessuna chiamata a CDN.
- Font Cinzel, Playfair Display e Inter con licenze OFL, provenienza e SHA-256
  registrati; `font-src 'self'` e controllo delle risorse esterne.
- CSP prima delle risorse: script e CSS locali, blocco di script/stili inline,
  connessioni, form, oggetti, frame e worker.
- `base-uri 'none'` e politica del referrer.
- `noopener noreferrer` sui collegamenti aperti in nuove schede.
- Controlli offline di policy, contenuti, font e collegamenti su ogni PR e push a `main`.
- Controllo della cronologia completa per impedire la reintroduzione del PDF
  rimosso attraverso un vecchio ramo; percorso escluso anche da `.gitignore`.
- Action ufficiale fissata a SHA, token `contents: read`, nessun segreto usato.

## Controlli dell'account e dell'hosting

Da eseguire nelle impostazioni GitHub, separatamente dalle modifiche al codice:

1. Usare passkey o autenticazione a più fattori, custodire i codici di recupero
   offline e verificare sessioni, token, deploy key e applicazioni autorizzate.
2. Proteggere `main`: passaggio da pull request, controlli obbligatori, divieto
   di force push e cancellazione. Per un progetto individuale non imporre una
   revisione impossibile da ottenere; aggiungere un revisore indipendente quando disponibile.
3. Controllare sorgente Pages, **Enforce HTTPS**, eventuale dominio personalizzato
   e relative impostazioni DNS. Conservare una copia indipendente del repository
   e provare il ripristino; la cronologia remota da sola non è un backup separato.
4. Limitare ogni nuova integrazione al repository e ai permessi necessari;
   controllare produttore, manutenzione, advisory e provenienza delle versioni.
   Un badge, una skill o il nome del produttore non certificano l'assenza di vulnerabilità.

## Limiti degli header

La CSP è distribuita con un tag `meta` per essere utilizzabile nella configurazione
statica attuale. `frame-ancestors` non funziona in un tag meta. Anche
`X-Content-Type-Options`, `Permissions-Policy` e `X-Frame-Options` richiedono
header HTTP: non aggiungere falsi tag meta o un file `_headers` confidando che
GitHub Pages li applichi.

Una futura infrastruttura con controllo degli header può aggiungere una CSP
HTTP con `frame-ancestors 'none'`, `X-Content-Type-Options: nosniff` e una
Permissions Policy restrittiva. Valutarla solo se necessaria; non è richiesta
una migrazione per leggere gli articoli in sicurezza. HSTS va verificato sulla
risposta dell'hosting. La revisione del 22 ottobre lo ha osservato sulla home
pubblica, ma non ha verificato tutte le impostazioni amministrative.

## Segnalazioni

Non pubblicare credenziali o dettagli sfruttabili in un'issue pubblica.
Usare la segnalazione privata delle vulnerabilità di GitHub, se attivata dal
proprietario, oppure concordare un canale privato con il manutentore.
Non eseguire test invasivi contro infrastrutture condivise GitHub Pages.

La revisione documentata in `docs/revisione-sicurezza-2026-10-22.md` è una
valutazione circoscritta del codice e delle risposte osservate, non una
certificazione, un penetration test completo o una garanzia di inviolabilità.
