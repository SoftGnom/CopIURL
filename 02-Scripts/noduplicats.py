import os

# ==============================================================================
# CONFIGURACIÓ DE FITXERS (Pots canviar els noms si ho necessites)
# ==============================================================================
FITXER_ORIGEN = 'origen.txt'
FITXER_DESTI = 'desti.txt'
FITXER_VISITATS = 'visitats.txt'  # Fitxer d'historial amb les URLs ja processades


# ==============================================================================
# FUNCIONS AUXILIARS
# ==============================================================================
def normalitzar_linia(linia):
    """
    Elimina espais en blanc, tabuladors i salts de línia.
    S'utilitza com a clau única per detectar duplicats exactes.
    """
    return "".join(linia.split())


def carregar_urls_visitades(ruta_fitxer):
    """Carrega les URLs de l'historial en un conjunt (set) per a una cerca ultra ràpida."""
    visitades = set()
    if os.path.exists(ruta_fitxer):
        with open(ruta_fitxer, 'r', encoding='utf-8') as f:
            for linia in f:
                clau = normalitzar_linia(linia)
                if clau:
                    visitades.add(clau)
    return visitades


def processar_urls(fitxer_origen, fitxer_desti, historial_set):
    """
    Llegeix origen.txt, descarta duplicats interns i URLs que ja estan a l'historial,
    i escriu el resultat a desti.txt.
    """
    if not os.path.exists(fitxer_origen):
        print(f"[!] Error: El fitxer '{fitxer_origen}' no existeix.")
        return []

    # Fem una còpia del conjunt per anar-hi afegint les d'aquesta execució
    vistes_actuals = set(historial_set)
    noves_linies = []

    with open(fitxer_origen, 'r', encoding='utf-8') as f_in, \
         open(fitxer_desti, 'w', encoding='utf-8') as f_out:
        
        for linia in f_in:
            clau = normalitzar_linia(linia)
            
            if not clau:
                continue  # Salta línies buides
                
            # Només s'inclou si NO està a l'historial ni s'ha vist abans en aquest fitxer
            if clau not in vistes_actuals:
                vistes_actuals.add(clau)
                f_out.write(linia)
                noves_linies.append(linia)

    return noves_linies


def actualitzar_historial(fitxer_visitats, noves_linies):
    """Afegeix les noves URLs al final del fitxer d'historial (mode 'a')."""
    with open(fitxer_visitats, 'a', encoding='utf-8') as f:
        for linia in noves_linies:
            # Assegura que la línia acabi amb un salt de línia
            f.write(linia if linia.endswith('\n') else linia + '\n')


# ==============================================================================
# FLUX PRINCIPAL
# ==============================================================================
def main():
    print("==================================================")
    print("       NETEJA DE DUPLICATS I FILTRAT D'HISTORIAL  ")
    print("==================================================")

    # 1. Carregar historial de visitats
    visitades = carregar_urls_visitades(FITXER_VISITATS)
    print(f"[+] URLs carregades des de l'historial ('{FITXER_VISITATS}'): {len(visitades)}")

    # 2. Processar origen.txt -> desti.txt
    noves_urls = processar_urls(FITXER_ORIGEN, FITXER_DESTI, visitades)
    total_noves = len(noves_urls)

    print(f"[+] S'han guardat {total_noves} URLs noves a '{FITXER_DESTI}'.")

    # 3. Preguntar si es volen afegir a l'historial de visitades
    if total_noves > 0:
        print("--------------------------------------------------")
        resposta = input(
            f"Vols afegir aquestes {total_noves} URLs al fitxer d'historial ('{FITXER_VISITATS}')? [s/N]: "
        ).strip().lower()

        if resposta in ['s', 'si', 'sí', 'y', 'yes']:
            actualitzar_historial(FITXER_VISITATS, noves_urls)
            print(f"[+] S'ha actualitzat '{FITXER_VISITATS}' correctament.")
        else:
            print(f"[i] No s'ha modificat '{FITXER_VISITATS}'.")
    else:
        print("[i] No hi ha cap URL nova per afegir a l'historial.")


if __name__ == '__main__':
    main()
