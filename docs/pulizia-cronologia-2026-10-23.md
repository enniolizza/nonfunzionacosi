# Cronologia e archivio — 23 ottobre 2026

## Rimozione del PDF

Su richiesta esplicita del proprietario è stata riscritta la parte della storia
che conteneva `Apri_Trading_in_the_Zone.pdf`. L'inventario completo comprendeva
40 commit: il file compariva in due alberi, senza altri percorsi per lo stesso
blob. Tre commit sono stati ricostruiti con le API Git di GitHub; i 37 precedenti
sono rimasti invariati. Non sono stati installati strumenti o plugin aggiuntivi.

| Commit precedente | Corrispondente ripulito |
| --- | --- |
| `230281e` | `01d97d2a2330ed73352e477d5f02a05345382a1e` |
| `a52ff7e` | `336b8e56ca434c26285ea4e6164cd2b003aeafae` |
| `abedef3` | `b17edbe614bf16363fd630535a047d9045552cbc` |

I primi due alberi differiscono esclusivamente per la rimozione del PDF.
L'albero del terzo è identico a quello già revisionato di `abedef3`. Le date dei
commit ricostruiti registrano la ricostruzione; non cambiano le date editoriali.
Prima di modificare i riferimenti remoti è stata verificata una copia di recupero
locale, esterna al repository pubblico. Gli aggiornamenti forzati dei soli due
rami interessati hanno usato gli SHA precedenti come condizione, per evitare
di sovrascrivere eventuali modifiche concorrenti.

La PR precedente è stata chiusa, dopo aver aggiornato anche il suo ramo alla
storia pulita. I riferimenti pubblicizzati sono stati ricontrollati: i tre
rami e `refs/pull/1/head` puntavano alla storia pulita; non erano presenti tag.
Il riferimento temporaneo `refs/pull/1/merge` non era più pubblicizzato dopo
la chiusura. Il lavoro prosegue su `codex/archivio-sicuro-2026-10-23`.

Questo intervento elimina il PDF dalla storia raggiungibile dei rami controllati.
Non certifica la cancellazione fisica degli oggetti Git conservati da GitHub,
delle viste memorizzate, dei vecchi URL di commit, dei fork o dei cloni altrui.
GitHub documenta questi limiti e precisa che il servizio di rimozione dei dati
sensibili non è garantito per contenuti non sensibili. Non è stata inviata una
segnalazione legale o una richiesta al supporto per conto del proprietario.

La verifica HTTP del 23 ottobre ha restituito 404 per il PDF sul ramo `main`
e sul sito Pages, ma 200 per il vecchio URL raw basato sul commit originario.
Quindi una copia residua era ancora scaricabile su GitHub dopo la riscrittura:
la pulizia dei riferimenti Git non va descritta come cancellazione completa.

Per evitare ricomparse, il percorso è escluso da `.gitignore` e la CI esegue
`scripts/check_history.py`: controlla il nome del file e il blob noto su tutti
i riferimenti Git locali, anche se il PDF è stato cancellato nell'ultimo commit.
I cloni superficiali vengono rifiutati. Un test sul vecchio ramo ha confermato
il fallimento; lo stesso controllo passa sulla storia ricostruita.

Chi possiede un clone precedente deve crearne uno nuovo, evitando merge o push
dei vecchi rami. Il piano editoriale e `wyckoff_wti_v2.pdf` restano pubblici:
non erano oggetto della richiesta di rimozione.

## Contesto storico degli articoli

Articoli e manifesto mantengono integralmente il testo principale e le fonti:
`tests/content-baseline.json` è invariato. Nei dossier è stata aggiunta una
nota di archivio esterna al `main`, che chiarisce la data e l'assenza di
aggiornamenti in tempo reale. La fascia del petrolio e la sua descrizione per
i motori di ricerca sono state rese esplicitamente storiche. Home e ticker
non presentano più prezzi e blocco navale di aprile come eventi attuali.

La cronologia del testo conferma gli ultimi cambiamenti editoriali dei dossier
al 15 aprile 2026. Il Superbonus conserva la data di pubblicazione dell'8 aprile;
il petrolio conserva quella del 15 aprile e l'orario dell'aggiornamento dati.
Non sono state aggiornate quotazioni, analisi, previsioni o conclusioni.

Per entrambi i dossier la sitemap omette i campi facoltativi `lastmod` e
`changefreq`: l'aggiornamento del frontend non viene presentato come una nuova
revisione dei dati. La home riporta `lastmod` al 23 ottobre, perché i suoi
riepiloghi sono stati effettivamente modificati. Le altre date restano invariate.

## Verifica visiva e controlli

La verifica a 390 px ha rilevato un titolo del dossier petrolio tagliato
verticalmente: l'overlay assoluto era più alto della copertina ad altezza fissa.
La copertina ora cresce con il contenuto, mantenendo un'altezza minima. Un nuovo
controllo browser verifica che badge, titolo e sottotitolo stiano interamente
nel contenitore a 320, 390, 768 e 1440 px. Questa verifica integra i precedenti
controlli dell'overflow orizzontale, che non rilevavano quel difetto.

Il runner della CI è fissato a `ubuntu-24.04`. Restano verificati cinque documenti
HTML, policy, font locali e relative licenze, collegamenti, sintassi JavaScript,
contenuti protetti, cronologia e differenze di whitespace. Le 16 combinazioni
pagina/larghezza sono testate localmente con Chromium e Playwright già presenti,
compresi font, tastiera, fallback senza JavaScript e blocchi CSP.

Le anteprime mobili sono in `anteprima-home-mobile.jpg` e
`anteprima-petrolio-mobile.jpg`. Il test browser resta esterno alla CI minimale.

Le impostazioni amministrative di ruleset, Pages, autenticazione e recupero
sono distinte da queste verifiche del codice. Il connettore usato non espone
le relative modifiche amministrative; il pannello web richiede l'accesso
all'account del proprietario.

Fonti:

- [GitHub: rimozione di dati dalla cronologia e limiti delle copie residue](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
- [Google Search Central: lastmod e aggiornamenti significativi](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
- [Protocollo Sitemap: campi facoltativi](https://www.sitemaps.org/protocol.html).
