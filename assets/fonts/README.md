# Font locali

File WOFF2 originali, scaricati il 22 ottobre 2026 dal servizio ufficiale Google
Fonts, senza modificare i binari. Nessuna richiesta a Google avviene durante
la visita al sito: `shared.css` carica esclusivamente i file di questa cartella.

| Famiglia | Stile e pesi dichiarati | Licenza |
| --- | --- | --- |
| Cinzel | normale 500, 700 | `cinzel-OFL.txt` |
| Playfair Display | normale 400, 700; corsivo 400 | `playfair-display-OFL.txt` |
| Inter | normale 400, 500, 600, 700 | `inter-OFL.txt` |

Sono inclusi i sottoinsiemi `latin` e `latin-ext`, con gli intervalli Unicode
forniti dal servizio. I pesi della stessa variante condividono il file variabile:
il browser lo scarica una sola volta. `font-display: swap` mantiene leggibile il
testo durante il caricamento. Per altri alfabeti resta disponibile il fallback
locale dichiarato nel CSS.

`sources.json` registra URL di origine, dimensioni e SHA-256 dei file. Le licenze
SIL OFL 1.1 provengono dal repository ufficiale
[`google/fonts`](https://github.com/google/fonts/tree/45e3d5269e4a17d823f6d84470bc084dc5ae46f6/ofl),
fissato al commit indicato. I WOFF2 provengono dagli URL versionati di
`fonts.gstatic.com` registrati nel manifest; non si presume che corrispondano
alla stessa revisione dei TTF nel repository.
Nei soli file di licenza sono stati rimossi gli spazi a fine riga per il controllo
whitespace: il testo è identico e `source_sha256` conserva l'impronta del download
originale, distinta da quella del file locale.

`scripts/check_site.py` verifica impronte, licenze e riferimenti locali. Questi
controlli rilevano cambiamenti rispetto ai file acquisiti, non certificano
l'assenza di vulnerabilità. Per un aggiornamento, controllare le fonti ufficiali,
aggiornare insieme file, manifest e CSS, e rieseguire anche il test browser.
