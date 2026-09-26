# CopIURL
CopIURL AI és una eina modular dissenyada per automatitzar la recollida, neteja, organització i anàlisi de contingut web de manera 100% privada i offline.


---



```python
readme_content = """# Netejador i Llançador de URLs amb LibreWolf

Aquest projecte ofereix una solució completa en Python i Bash per processar fitxers de text (com ara llistes de URLs), eliminar-ne les línies duplicades (ignorant espais i salts de línia) i obrir-les d'una manera fàcil i visual mitjançant una interfície gràfica en **LibreWolf**.

Tot el flux de travail està dissenyat per executar-se en un **entorn virtual aïllat (`venv`)** gestionat automàticament per scripts de terminal.

---

## 📁 Estructura del Projecte

```text
.
├── gestor.sh          # Script principal amb menú interactiu
├── instalar.sh        # Script per crear i configurar l'entorn virtual (venv)
├── noduplicats.py     # Neteja línies duplicades d'origen.txt -> desti.txt
├── gui_librewolf.py   # Interfície gràfica Tkinter per obrir les URLs de desti.txt
├── origen.txt         # Fitxer d'entrada amb les URLs/línies originals
├── desti.txt          # Fitxer de sortida amb les línies úniques
└── requirements.txt   # (Opcional) Dependències de Python

```

---

## 🚀 Inici Ràpid

### 1. Donar permisos d'execució

Abans de començar, dona permisos d'execució als scripts Bash:

```bash
chmod +x gestor.sh instalar.sh

```

### 2. Executar el Gestor Principal

Només cal executar el script `gestor.sh`:

```bash
./gestor.sh

```

Aquest gestor:

* Activa automàticament l'entorn virtual `venv` si ja existeix.
* Et mostra un menú interactiu per triar quina acció realitzar.
* Desactiva l'entorn virtual `venv` de manera neta quan surts.

---

## 🛠️ Descripció dels components

### 1. `gestor.sh` (Menú Interactiu)

Proporciona una interfície de línia de comandes (CLI) intuïtiva amb suport de colors per mostrar si l'entorn virtual està **ACTIVAT** o **DESACTIVAT**.

**Opcions del menú:**

1. **Executar noduplicats.py**: Processa el fitxer d'origen i genera el fitxer net.
2. **Executar gui_librewolf.py**: Obre la interfície gràfica per gestionar i llançar les URLs.
3. **Instal·lar / Recrear entorn virtual**: Prepara l'entorn aïllat i les dependències.
4. **Sortir**: Tanca el gestor i desactiva l'entorn `venv`.

### 2. `instalar.sh` (Configuració de l'entorn)

Un script Bash autònom que:

* Comprova que `python3` i `python3-venv` estiguin instal·lats al sistema.
* Crea el directori `venv/`.
* Actualitza `pip`, `setuptools` i `wheel`.
* Instal·la les dependències indicades a `requirements.txt` (si existeix).

Pots executar-lo directament amb `./instalar.sh` o des de l'opció 3 de `gestor.sh`.

### 3. `noduplicats.py` (Processament de text)

Llegeix el fitxer `origen.txt` i guarda a `desti.txt` només les línies úniques.

* **Normalització ràpida:** Utilitza un conjunt (`set`) de Python per a una comparació O(1) hiperràpida.
* **Ignora espais:** Elimina tots els espais en blanc, tabuladors i salts de línia a l'hora de comparar, garantint que `"https://example.com "` i `"  https://example.com"` es detectin com la mateixa URL.
* **Respecta l'original:** Manté el text i el format original de la primera aparició de cada línia.

### 4. `gui_librewolf.py` (Llançador de URLs)

Aplicació d'escriptori desenvolupada amb **Tkinter**:

* Carrega automàticament la llista de URLs de `desti.txt`.
* Permet obrir una URL fent **doble clic** sobre ella o seleccionant-la i prement el botó **Obrir Seleccionada**.
* Inclou el botó **Obrir Totes** per obrir tot el llistat en pestanyes de LibreWolf.
* **Fallback automàtic:** Si no es troba la comanda `librewolf` al PATH del sistema, utilitza el navegador per defecte.

---

## ⚙️ Requisits del Sistema

* **Sistema Operatiu:** Linux (Ubuntu, Debian, Arch, Fedora, etc.)
* **Python:** 3.6 o superior.
* **Paquets del sistema:** `python3-venv` i `python3-tk` (normalment inclosos o instal·lables via `apt` / paquetitzador del sistema).
* **Navegador (Opcional):** [LibreWolf](https://librewolf.net/) instal·lat i disponible al PATH.

Si utilitzes Debian/Ubuntu i et falta algun paquet:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk librewolf

```

---

## 📝 Exemple d'Ús

1. Posa la teva llista de URLs (amb espais, duplicats o línies buides) a `origen.txt`:
```text
[https://github.com](https://github.com)
  [https://github.com](https://github.com)
[https://wikipedia.org](https://wikipedia.org)

```


2. Executa `./gestor.sh` i tria l'opció **1** (`noduplicats.py`).
3. El fitxer `desti.txt` ara contindrà:
```text
[https://github.com](https://github.com)
[https://wikipedia.org](https://wikipedia.org)

```


4. Des del menú de `./gestor.sh`, tria l'opció **2** (`gui_librewolf.py`) per obrir la interfície i navegar per les teves URLs!
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("README.md creat correctament.")

```

```text?code_stdout&code_event_index=1
README.md creat correctament.


```

S'ha generat el fitxer **README.md** per al projecte:

---

### Contingut del `README.md`:

```markdown
# Netejador i Llançador de URLs amb LibreWolf

Aquest projecte ofereix una solució completa en Python i Bash per processar fitxers de text (com ara llistes de URLs), eliminar-ne les línies duplicades (ignorant espais i salts de línia) i obrir-les d'una manera fàcil i visual mitjançant una interfície gràfica en **LibreWolf**.

Tot el flux de treball està dissenyat per executar-se en un **entorn virtual aïllat (`venv`)** gestionat automàticament per scripts de terminal.

---

## 📁 Estructura del Projecte

```text
.
├── gestor.sh          # Script principal amb menú interactiu
├── instalar.sh        # Script per crear i configurar l'entorn virtual (venv)
├── noduplicats.py     # Neteja línies duplicades d'origen.txt -> desti.txt
├── gui_librewolf.py   # Interfície gràfica Tkinter per obrir les URLs de desti.txt
├── origen.txt         # Fitxer d'entrada amb les URLs/línies originals
├── desti.txt          # Fitxer de sortida amb les línies úniques
└── requirements.txt   # (Opcional) Dependències de Python

```

---

## 🚀 Inici Ràpid

### 1. Donar permisos d'execució

Abans de començar, dona permisos d'execució als scripts Bash:

```bash
chmod +x gestor.sh instalar.sh

```

### 2. Executar el Gestor Principal

Només cal executar el script `gestor.sh`:

```bash
./gestor.sh

```

Aquest gestor:

* Activa automàticament l'entorn virtual `venv` si ja existeix.
* Et mostra un menú interactiu per triar quina acció realitzar.
* Desactiva l'entorn virtual `venv` de manera neta quan surts.

---

## 🛠️ Descripció dels components

### 1. `gestor.sh` (Menú Interactiu)

Proporciona una interfície de línia de comandes (CLI) intuïtiva amb suport de colors per mostrar si l'entorn virtual està **ACTIVAT** o **DESACTIVAT**.

**Opcions del menú:**

1. **Executar noduplicats.py**: Processa el fitxer d'origen i genera el fitxer net.
2. **Executar gui_librewolf.py**: Obre la interfície gràfica per gestionar i llançar les URLs.
3. **Instal·lar / Recrear entorn virtual**: Prepara l'entorn aïllat i les dependències.
4. **Sortir**: Tanca el gestor i desactiva l'entorn `venv`.

### 2. `instalar.sh` (Configuració de l'entorn)

Un script Bash autònom que:

* Comprova que `python3` i `python3-venv` estiguin instal·lats al sistema.
* Crea el directori `venv/`.
* Actualitza `pip`, `setuptools` i `wheel`.
* Instal·la les dependències indicades a `requirements.txt` (si existeix).

Pots executar-lo directament amb `./instalar.sh` o des de l'opció 3 de `gestor.sh`.

### 3. `noduplicats.py` (Processament de text)

Llegeix el fitxer `origen.txt` i guarda a `desti.txt` només les línies úniques.

* **Normalització ràpida:** Utilitza un conjunt (`set`) de Python per a una comparació O(1) hiperràpida.
* **Ignora espais:** Elimina tots els espais en blanc, tabuladors i salts de línia a l'hora de comparar, garantint que `"https://example.com "` i `"  https://example.com"` es detectin com la mateixa URL.
* **Respecta l'original:** Manté el text i el format original de la primera aparició de cada línia.

### 4. `gui_librewolf.py` (Llançador de URLs)

Aplicació d'escriptori desenvolupada amb **Tkinter**:

* Carrega automàticament la llista de URLs de `desti.txt`.
* Permet obrir una URL fent **doble clic** sobre ella o seleccionant-la i prement el botó **Obrir Seleccionada**.
* Inclou el botó **Obrir Totes** per obrir tot el llistat en pestanyes de LibreWolf.
* **Fallback automàtic:** Si no es troba la comanda `librewolf` al PATH del sistema, utilitza el navegador per defecte.

---

## ⚙️ Requisits del Sistema

* **Sistema Operatiu:** Linux (Ubuntu, Debian, Arch, Fedora, etc.)
* **Python:** 3.6 o superior.
* **Paquets del sistema:** `python3-venv` i `python3-tk` (normalment inclosos o instal·lables via `apt` / paquetitzador del sistema).
* **Navegador (Opcional):** [LibreWolf](https://librewolf.net/) instal·lat i disponible al PATH.

Si utilitzes Debian/Ubuntu i et falta algun paquet:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk librewolf

```

---

## 📝 Exemple d'Ús

1. Posa la teva llista de URLs (amb espais, duplicats o línies buides) a `origen.txt`:
```text
[https://github.com](https://github.com)
  [https://github.com](https://github.com)
[https://wikipedia.org](https://wikipedia.org)

```


2. Executa `./gestor.sh` i tria l'opció **1** (`noduplicats.py`).
3. El fitxer `desti.txt` ara contindrà:
```text
[https://github.com](https://github.com)
[https://wikipedia.org](https://wikipedia.org)

```


4. Des del menú de `./gestor.sh`, tria l'opció **2** (`gui_librewolf.py`) per obrir la interfície i navegar per les teves URLs!

```

```
