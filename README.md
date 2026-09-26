# CopIURL
CopIURL AI és una eina modular dissenyada per automatitzar la recollida, neteja, organització i anàlisi de contingut web de manera 100% privada i offline.


---

```markdown
# 🔗 Gestor de URLs i Captura de Porta-retalls amb LibreWolf

Aquesta aplicació ofereix una solució completa en **Python** i **Bash** per a la captura automàtica de text del porta-retalls, la filtració de línies duplicades i la gestió/obertura còmoda de URLs mitjançant una interfície gràfica (GUI) integrada amb **LibreWolf** (o el navegador del sistema).

Tot el flux de treball s'executa en un entorn virtual aïllat (`venv`) gestionat automàticament des d'un menú principal a la terminal.

---

## 📁 Estructura del Projecte

```text
.
├── gestor.sh              # Script principal amb menú interactiu
├── instalar.sh            # Script per configurar l'entorn virtual i instal·lar dependències
├── captura_clipboard.py   # Script de captura contínua del porta-retalls
├── noduplicats.py         # Filtre per eliminar línies duplicades
├── gui_librewolf.py       # Interfície gràfica (Tkinter) per gestionar i obrir URLs
├── requirements.txt       # Dependències de Python (pyperclip)
├── origen.txt             # (Generat) Text i URLs capturades del porta-retalls
└── desti.txt              # (Generat) URLs i línies úniques netes

```

---

## ⚙️ Requisits del Sistema

* **Sistema Operatiu:** Linux (Ubuntu, Debian, Linux Mint, Arch, Fedora, etc.)
* **Python:** 3.6 o superior.
* **Paquets del sistema recomanats/necessaris:**
* `python3-venv` (per a l'entorn virtual)
* `python3-tk` (per a la interfície gràfica)
* `xclip` (recomanat a Linux per al funcionament del porta-retalls)


* **Navegador:** LibreWolf (suporta instal·lació nativa, Flatpak o Snap). Si no es troba, s'obrirà el navegador per defecte del sistema.

### Instal·lació de paquets bàsics (Debian/Ubuntu/Mint):

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk xclip

```

---

## 🚀 Inici Ràpid

### 1. Assignar permisos d'execució

Dona permisos d'execució als scripts Bash:

```bash
chmod +x gestor.sh instalar.sh

```

### 2. Preparar l'entorn virtual

Executa l'instal·lador per crear el `venv` i instal·lar les dependències de Python (`pyperclip`):

```bash
./instalar.sh

```

*(També pots fer-ho des de l'opció 4 del menú de `gestor.sh`)*.

### 3. Executar el Gestor Principal

```bash
./gestor.sh

```

---

## 🛠️ Menú i Funcionament dels Components

El script `gestor.sh` ofereix un menú centralitzat que activa automàticament l'entorn virtual al comença i el desactiva en sortir.

```text
========================================
       GESTOR DE PROCESSOS PYTHON       
 [ESTAT ENTORN: ACTIVAT -> /ruta/al/venv]
========================================
1) Capturar text del porta-retalls -> origen.txt
2) Executar noduplicats.py (Netejar línies)
3) Executar gui_librewolf.py (Interfície URLs)
4) Instal·lar / Recrear entorn virtual i dependències
0) Sortir (i desactivar entorn)
========================================

```

---

### 📋 Descripció dels Mòduls

#### 1. `captura_clipboard.py` (Opció 1)

* Monitoritza el porta-retalls en segon pla. Cada cop que fas **Ctrl+C** a qualsevol text o URL, s'afegeix automàticament a `origen.txt`.
* Normalitza els espais múltiples en una sola línia.
* Si `origen.txt` ja existeix, permet escollir entre **afegir noves línies al final (Append)** o **reiniciar el fitxer (Reescriure)**.
* Prem **[ENTER]** a la terminal per aturar la captura netament.

#### 2. `noduplicats.py` (Opció 2)

* Llegeix `origen.txt` i genera `desti.txt`.
* Elimina totes les línies duplicades ignora espais en blanc, tabuladors i salts de línia a l'hora de comparar (per exemple, `" https://example.com "` i `"https://example.com"` es tractaran com la mateixa URL).
* Salta automàticament les línies buides i preserva el format de la primera aparició.

#### 3. `gui_librewolf.py` (Opció 3)

* Interfície gràfica desenvolupada en **Tkinter** que mostra les URLs de `desti.txt`.
* **Obrir URL:** Fes **doble clic** sobre qualsevol URL o selecciona-la i prem **"Obrir Seleccionada"**.
* **Obrir Totes:** Obre totes les URLs de la llista en pestanyes diferents de LibreWolf (demana confirmació prèvia).
* **Esborrar URL:** Selecciona una URL i prem el botó **"Esborrar Seleccionada"** o la tecla **`[Supr] / [Delete]`**. S'actualitza automàticament la llista, el comptador i el fitxer `desti.txt`.
* **Detecció Intel·ligent de LibreWolf:**
1. Cerca executables natius (`librewolf`, `/usr/bin/librewolf`, etc.).
2. Comprova si està instal·lat via **Flatpak** (`io.gitlab.librewolf-community` o `com.librewolf.LibreWolf`).
3. Comprova si està instal·lat via **Snap** (`librewolf`).
4. Si no es troba cap versió de LibreWolf, utilitza `xdg-open` o el navegador predeterminat del sistema.



#### 4. `instalar.sh` (Opció 4)

* Comprova que Python 3, `python3-tk` i `xclip` estiguin instal·lats.
* Crea la carpeta `venv/` si no existeix o la regenera si està corrompuda.
* Actualitza `pip`, `setuptools` i `wheel`.
* Instal·la automàticament les llibraries indicades a `requirements.txt`.

---

## 📝 Flux de Treball Típic

1. Executa `./gestor.sh` i tria l'opció **1**.
2. Navega per la xarxa o documents fent **Ctrl+C** a les URLs o textos que vulguis desar.
3. Quan hagis acabat, prem **ENTER** a la terminal.
4. Tria l'opció **2** per eliminar duplicats i generar la llista neta a `desti.txt`.
5. Tria l'opció **3** per obrir la interfície gràfica, revisar les URLs i obrir-les a LibreWolf!

```

```
