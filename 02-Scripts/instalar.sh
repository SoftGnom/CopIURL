#!/usr/bin/env bash

VENV_DIR="venv"

echo "========================================="
echo "   INSTAL·LADOR D'ENTORN VIRTUAL (VENV)  "
echo "========================================="

# 1. Comprovar si python3 està instal·lat
if ! command -v python3 &> /dev/null; then
    echo "[!] Error: Python 3 no està instal·lat al sistema."
    exit 1
fi

# Comprovar si Tkinter està instal·lat al sistema
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "[!] Error: Falta el paquet 'python3-tk' del sistema."
    echo "    Instal·la'l executant: sudo apt install python3-tk"
    exit 1
fi


# Comprovar si xclip està instal·lat (necessari per al porta-retalls en Linux)
if ! command -v xclip &> /dev/null; then
    echo "[!] Avís: Es recomana instal·lar 'xclip' per a la captura de porta-retalls."
    echo "    Pots instal·lar-lo amb: sudo apt install xclip"
fi



# 2. Si la carpeta existeix però està corrompuda (sense activate), l'esborrem
if [ -d "$VENV_DIR" ] && [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "[!] S'ha detectat un entorn incomplet. Netejant..."
    rm -rf "$VENV_DIR"
fi

# 3. Crear l'entorn virtual si no existeix
if [ ! -d "$VENV_DIR" ]; then
    echo "[+] Creant l'entorn virtual a la carpeta '$VENV_DIR'..."
    if ! python3 -m venv "$VENV_DIR"; then
        echo "[!] Error creant el venv. Assegura't de tenir 'python3-venv' instal·lat."
        exit 1
    fi
else
    echo "[i] La carpeta '$VENV_DIR' ja existeix i és vàlida."
fi

# 4. Activar l'entorn
echo "[+] Activant l'entorn virtual..."
source "$VENV_DIR/bin/activate" || { echo "[!] Error en activar l'entorn"; exit 1; }

echo "[+] Actualitzant pip i eines de construcció..."
pip install --upgrade pip setuptools wheel

# 5. Instal·lar dependències
if [ -f "requirements.txt" ] && [ -s "requirements.txt" ]; then
    echo "[+] Instal·lant paquets des de 'requirements.txt'..."
    pip install -r requirements.txt
else
    echo "[i] No s'han trobat dependències externes a 'requirements.txt'."
fi

echo ""
echo "========================================="
echo "  [✓] ENTORN VIRTUAL INSTAL·LAT AMB ÈXIT "
echo "========================================="
