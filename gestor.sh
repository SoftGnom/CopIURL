#!/usr/bin/env bash

VENV_DIR="venv"

# Funció per mostrar l'estat actual de l'entorn virtual
mostrar_estat_venv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo -e " [ESTAT ENTORN: \033[32mACTIVAT\033[0m -> $VIRTUAL_ENV]"
    else
        echo -e " [ESTAT ENTORN: \033[31mDESACTIVAT\033[0m]"
    fi
}

# Funció per activar el venv
activar_venv() {
    if [ -d "$VENV_DIR" ]; then
        if [ -z "$VIRTUAL_ENV" ]; then
            source "$VENV_DIR/bin/activate"
            echo "[+] Entorn virtual '$VENV_DIR' activat correctament."
        fi
    else
        echo "[!] L'entorn virtual no existeix. Fes servir l'opció 3 per instal·lar-lo."
    fi
}

# Funció per desconnectar netament
desconnectar_i_sortir() {
    echo ""
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
        echo "[+] Entorn virtual desactivat."
    fi
    mostrar_estat_venv
    echo "Fins la propera!"
    exit 0
}

# Captura Ctrl+C per tancar l'entorn si s'interromp
trap desconnectar_i_sortir INT

# Activa l'entorn automàticament a l'inici si ja està creat
activar_venv

# Menú principal
while true; do
    echo ""
    echo "========================================"
    echo "       GESTOR DE PROCESSOS PYTHON       "
    mostrar_estat_venv
    echo "========================================"
    echo "1) Capturar text del porta-retalls -> origen.txt"
    echo "2) Executar noduplicats.py (Netejar línies)"
    echo "3) Descarregar HTMLs nets (Text offline) -> html_descarregats/"
    echo "4) Executar gui_librewolf.py (Interfície URLs)"
    echo "5) Instal·lar / Recrear entorn virtual i dependències"
    echo "0) Sortir (i desactivar entorn)"
    echo "========================================"
    read -p "Tria una opció [0-5]: " opcio

    case $opcio in
        0)
            desconnectar_i_sortir
            ;;

        1)
            activar_venv
            echo -e "\n--> Executant captura_clipboard.py..."
            python3 captura_clipboard.py
            ;;

        2)
            rm desti.txt
            activar_venv
            echo -e "\n--> Executant noduplicats.py..."
            python3 noduplicats.py
            ;;
        3)
            activar_venv
            echo -e "\n--> Executant descarregar_html.py..."
            python3 descarregar_html.py
            ;;
        4)
            activar_venv
            echo -e "\n--> Executant gui_librewolf.py..."
            python3 gui_librewolf.py
            ;;
        5)
            echo -e "\n--> Iniciant procés d'instal·lació..."
            
            # Desactivem l'entorn si està en marxa per poder-lo reinstal·lar net
            if [ -n "$VIRTUAL_ENV" ]; then
                deactivate
            fi

            # Si existeix el fitxer instalar.sh, l'executem directament com a única font
            if [ -f "./instalar.sh" ]; then
                chmod +x ./instalar.sh
                ./instalar.sh
            else
               echo "[!] Error: Et falta el paquet 'instalar.sh' al software."
            fi

            # Re-activem l'entorn per continuar usant el gestor
            activar_venv
            ;;
        *)
            echo "Opció no vàlida. Intenta-ho de nou."
            ;;
    esac
done
