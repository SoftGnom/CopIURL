import os
import sys
import threading
import time

try:
    import pyperclip
except ImportError:
    print(
        "[!] Falta la llibreria 'pyperclip'. Executa l'instal·lador o: pip install pyperclip"
    )
    sys.exit(1)

FITXER_ORIGEN = 'origen.txt'


def comptar_linies(fitxer):
    if not os.path.exists(fitxer):
        return 0
    with open(fitxer, 'r', encoding='utf-8') as f:
        return sum(1 for linia in f if linia.strip())


def esperar_enter(estat):
    input()
    estat['en_execucio'] = False


def main():
    mode = 'a'

    if os.path.exists(FITXER_ORIGEN) and os.path.getsize(FITXER_ORIGEN) > 0:
        print(f"\n[i] El fitxer '{FITXER_ORIGEN}' ja existeix.")
        print("1) Continuar afegint línies al final (Append)")
        print("2) Esborrar el fitxer i començar de nou (Reescriure)")
        opcio = input("Tria una opció [1-2] (Per defecte: 1): ").strip()

        if opcio == '2':
            mode = 'w'
            open(FITXER_ORIGEN, 'w', encoding='utf-8').close()
            print(f"[+] S'ha reiniciat el fitxer '{FITXER_ORIGEN}'.")

    total_linies = comptar_linies(FITXER_ORIGEN)

    print('\n==================================================')
    print('       CAPTURA AUTOMÀTICA DE PORTA-RETALLS        ')
    print('==================================================')
    print('• Fes Ctrl+C a qualsevol lloc per afegir text al fitxer.')
    print('• Prem [ENTER] AQUÍ a la terminal per ATURAR el programa.')
    print('--------------------------------------------------')
    print(f'Línies guardades actualment: {total_linies}', end='', flush=True)

    ultim_text = pyperclip.paste()
    estat = {'en_execucio': True}

    # Inicia l'escolta de la tecla ENTER en un fil independent
    hilo_input = threading.Thread(
        target=esperar_enter, args=(estat,), daemon=True
    )
    hilo_input.start()

    try:
        with open(FITXER_ORIGEN, mode, encoding='utf-8') as f:
            while estat['en_execucio']:
                time.sleep(0.4)
                text_actual = pyperclip.paste()

                if text_actual and text_actual != ultim_text:
                    ultim_text = text_actual
                    linia_neta = ' '.join(text_actual.split())

                    if linia_neta:
                        f.write(linia_neta + '\n')
                        f.flush()
                        total_linies += 1
                        print(
                            f'\rLínies guardades actualment: {total_linies} | ÚLTIMA: {linia_neta[:35]}...',
                            end='',
                            flush=True,
                        )
    except KeyboardInterrupt:
        pass

    print(
        f"\n\n[+] Captura aturada correctament. Total: {total_linies} línies a '{FITXER_ORIGEN}'."
    )


if __name__ == '__main__':
    main()
