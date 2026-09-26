import os
import re
import shutil
from urllib.parse import urlparse
import bs4
import requests
from dataclasses import dataclass

FITXER_DESTI = 'desti.txt'
CARPETA_SORTIDA = 'html_descarregats'
FITXER_REGISTRE = 'registre_descarregues.csv'

def netejar_directori(directori):
    """Esborra el contingut de la carpeta i la torna a crear."""
    if os.path.exists(directori):
        shutil.rmtree(directori)
    os.makedirs(directori)


def generar_nom_fitxer_segur(url, index):
    """Genera un nom de fitxer vàlid a partir de la URL."""
    parsed = urlparse(url)
    domini_i_ruta = parsed.netloc + parsed.path
    # Substitueix caràcters no alfanumèrics per guions baixos
    nom_segur = re.sub(r'[^\w\-]', '_', domini_i_ruta).strip('_')
    if not nom_segur:
        nom_segur = f'pagina_{index}'
    # Limita la longitud del nom i afegeix l'índex per evitar col·lisions
    return f'{index:03d}_{nom_segur[:50]}.html'


def purgar_html(html_raw):
    """Purga l'HTML eliminant qualsevol element que pugui fer peticions externes o executar scripts."""
    soup = bs4.BeautifulSoup(html_raw, 'html.parser')

    # 1. Eliminar etiquetes de recursos externs, executables o multimèdia
    etiquetes_a_esborrar = [
        'script',
        'style',
        'link',
        'img',
        'iframe',
        'frame',
        'embed',
        'object',
        'video',
        'audio',
        'source',
        'picture',
        'svg',
        'noscript',
        'canvas',
        'map',
        'area',
        'track',
        'base',
    ]

    for nom_etiqueta in etiquetes_a_esborrar:
        for etiqueta in soup.find_all(nom_etiqueta):
            etiqueta.decompose()

    # 2. Eliminar etiquetes <meta> de redirecció automàtica (http-equiv="refresh")
    for meta in soup.find_all('meta'):
        http_equiv = meta.get('http-equiv', '')
        if (
            isinstance(http_equiv, str)
            and http_equiv.lower() == 'refresh'
        ):
            meta.decompose()

    # 3. Netejar atributs perillosos en TOTS els elements restants (estils en línia i esdeveniments JS)
    for element in soup.find_all(True):
        attrs_a_eliminar = []
        for attr in element.attrs:
            attr_lower = attr.lower()
            # Elimina esdeveniments Javascript (ex: onload, onclick, onerror) i atributs d'estil o fons
            if (
                attr_lower.startswith('on')
                or attr_lower in ['style', 'srcset', 'background']
            ):
                attrs_a_eliminar.append(attr)

        for attr in attrs_a_eliminar:
            del element.attrs[attr]

        # Netejar enllaços amb Javascript (href="javascript:...")
        if element.name == 'a' and 'href' in element.attrs:
            href_val = element['href']
            if (
                isinstance(href_val, str)
                and href_val.lower().startswith('javascript:')
            ):
                del element['href']

    return str(soup)


# --- ESTRUCTURA DE DADES EXTENSIBLE ---
@dataclass
class RegistreURL:
    id: int
    url: str
    correcte: bool          # Columna booleana (True / False)
    ruta_fitxer: str = ""   # Guardarà la ruta relativa (p. ex. "html_descarregats/001_pagina.html")
    motiu_error: str = ""   # Descripció de l'error (buit si ha anat bé)
    # En el futur es poden afegir noves columnes / métriques fàcilment aquí:
    # temps_execucio: float = 0.0
    # mida_bytes: int = 0


# --- FUNCIONS DELEGADES (SUB-RESPONSABILITATS) ---

def carregar_urls(ruta_fitxer):
    """Llegeix i retorna les URLs del fitxer desti.txt."""
    if not os.path.exists(ruta_fitxer):
        return []
    with open(ruta_fitxer, 'r', encoding='utf-8') as f:
        return [linia.strip() for linia in f if linia.strip()]


def processar_single_url(index, url, carpeta_sortida, headers):
    """S'encarrega exclusivament de descarregar, purgar i desar una sola URL."""
    target_url = url if url.startswith(('http://', 'https://')) else 'https://' + url
    nom_fitxer = generar_nom_fitxer_segur(target_url, index)
    ruta_fitxer = os.path.join(carpeta_sortida, nom_fitxer)

    try:
        resposta = requests.get(target_url, headers=headers, timeout=10)
        resposta.raise_for_status()

        resposta.encoding = resposta.apparent_encoding or 'utf-8'
        html_net = purgar_html(resposta.text)

        with open(ruta_fitxer, 'w', encoding='utf-8') as f_out:
            f_out.write(html_net)

        return RegistreURL(
            id=index,
            url=target_url,
            correcte=True,
            ruta_fitxer=ruta_fitxer,
            motiu_error=""
        )

    except Exception as e:
        msg_error = str(e).replace(';', ',')  # Netegem per no trencar el CSV
        return RegistreURL(
            id=index, 
            url=target_url, 
            correcte=False, 
            ruta_fitxer="",
            motiu_error=msg_error
        )


def guardar_registre_csv(fitxer_csv, llista_registres):
    """Genera el fitxer de taula CSV a partir dels registres recol·lectats."""
    with open(fitxer_csv, 'w', encoding='utf-8') as f_log:
        f_log.write("ID;URL;CORRECTE;RUTA_FITXER;MOTIU_ERROR\n")
        for reg in llista_registres:
            f_log.write(f"{reg.id};{reg.url};{reg.correcte};{reg.ruta_fitxer};{reg.motiu_error}\n")





def main():
    urls = carregar_urls(FITXER_DESTI)
    if not urls:
        print(f"[!] Error: No s'han trobat URLs a '{FITXER_DESTI}'.")
        return

    print(f"[+] Reiniciant carpeta '{CARPETA_SORTIDA}' i preparant descàrregues...")
    netejar_directori(CARPETA_SORTIDA)

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'Chrome/115.0.0.0 Safari/537.36'
        )
    }

    registres = []
    print(f"[+] Processant {len(urls)} URLs...\n")

    # Bucle principal de descàrregues
    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] Processant: {url}")
        registre = processar_single_url(i, url, CARPETA_SORTIDA, headers)
        registres.append(registre)
        
        if not registre.correcte:
            print(f"    [!] Error: {registre.motiu_error}")

    # Guardem la taula de registre
    guardar_registre_csv(FITXER_REGISTRE, registres)

    exits = sum(1 for r in registres if r.correcte)
    errors = len(registres) - exits

    print('\n==================================================')
    print(f" Descàrrega finalitzada a '{CARPETA_SORTIDA}/'")
    print(f" Fitxer de registre generat: '{FITXER_REGISTRE}'")
    print(f"  - Correctes: {exits}")
    print(f"  - Errors:    {errors}")
    print('==================================================')

if __name__ == '__main__':
    main()
