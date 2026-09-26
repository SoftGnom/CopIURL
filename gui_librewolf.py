import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import shutil
import csv
from dataclasses import dataclass

# Canviem el fitxer d'origen i afegim la carpeta per defecte
FITXER_REGISTRE = 'registre_descarregues.csv'
CARPETA_SORTIDA = 'html_descarregats'


# --- ESTRUCTURA I GESTIÓ DELS REGISTRES CSV ---
@dataclass
class ItemRegistre:
    id: str
    url: str
    correcte: str
    ruta_fitxer: str
    motiu_error: str


def carregar_registres_csv(ruta_csv):
    """Llegeix el CSV i retorna una llista d'objectes ItemRegistre."""
    if not os.path.exists(ruta_csv):
        return []
    registres = []
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            registres.append(
                ItemRegistre(
                    id=row.get('ID', ''),
                    url=row.get('URL', ''),
                    correcte=row.get('CORRECTE', 'False'),
                    ruta_fitxer=row.get('RUTA_FITXER', ''),
                    motiu_error=row.get('MOTIU_ERROR', ''),
                )
            )
    return registres


def guardar_registres_csv(ruta_csv, registres):
    """Guarda la llista d'objectes ItemRegistre de nou al CSV."""
    with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:
        f.write('ID;URL;CORRECTE;RUTA_FITXER;MOTIU_ERROR\n')
        for r in registres:
            f.write(
                f'{r.id};{r.url};{r.correcte};{r.ruta_fitxer};{r.motiu_error}\n'
            )




# --- ESTRUCTURA I GESTIÓ DELS REGISTRES CSV ---

def obrir_amb_librewolf(url):
    url = url.strip()
    if not url:
        return

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # 1. Intentar executables directes al PATH o rutes habituals de Linux
    rutes_posibles = [
        'librewolf',
        '/usr/bin/librewolf',
        '/usr/local/bin/librewolf',
        os.path.expanduser('~/.local/bin/librewolf'),
    ]
    for executant in rutes_posibles:
        if shutil.which(executant) or (
            os.path.isfile(executant) and os.access(executant, os.X_OK)
        ):
            subprocess.Popen([executant, url])
            return

    # 2. Intentar Flatpak (comprova els dos IDs existents de LibreWolf)
    if shutil.which('flatpak'):
        ids_flatpak = [
            'io.gitlab.librewolf-community',
            'com.librewolf.LibreWolf',
        ]
        for app_id in ids_flatpak:
            comprovacio = subprocess.run(
                ['flatpak', 'info', app_id],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if comprovacio.returncode == 0:
                subprocess.Popen(['flatpak', 'run', app_id, url])
                return

    # 3. Intentar Snap
    if shutil.which('snap'):
        comprovacio_snap = subprocess.run(
            ['snap', 'list', 'librewolf'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if comprovacio_snap.returncode == 0:
            subprocess.Popen(['snap', 'run', 'librewolf', url])
            return

    # 4. Fallback: Obrir amb el gestor del sistema (xdg-open) directament
    try:
        subprocess.Popen(['xdg-open', url])
    except Exception:
        webbrowser.open(url)

@dataclass
class ItemRegistre:
    id: str
    url: str
    correcte: str
    ruta_fitxer: str
    motiu_error: str


def carregar_registres_csv(ruta_csv):
    """Llegeix el CSV i retorna una llista d'objectes ItemRegistre."""
    if not os.path.exists(ruta_csv):
        return []
    registres = []
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            registres.append(
                ItemRegistre(
                    id=row.get('ID', ''),
                    url=row.get('URL', ''),
                    correcte=row.get('CORRECTE', 'False'),
                    ruta_fitxer=row.get('RUTA_FITXER', ''),
                    motiu_error=row.get('MOTIU_ERROR', ''),
                )
            )
    return registres


def guardar_registres_csv(ruta_csv, registres):
    """Guarda la llista d'objectes ItemRegistre de nou al CSV."""
    with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:
        f.write('ID;URL;CORRECTE;RUTA_FITXER;MOTIU_ERROR\n')
        for r in registres:
            f.write(
                f'{r.id};{r.url};{r.correcte};{r.ruta_fitxer};{r.motiu_error}\n'
            )


# --- INTERFÍCIE GRÀFICA REFACTORITZADA ---
class AplicacioURLs:


    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de URLs i HTMLs - LibreWolf")
        self.root.geometry("850x500")

        self.registres = carregar_registres_csv(FITXER_REGISTRE)

        # 1. PANELL DE BOTONS (Mogut a SOBRE de la taula)
        frame_botons = ttk.Frame(root, padding=10)
        frame_botons.pack(fill=tk.X, side=tk.TOP)  # <-- MODIFICAT: Ara es posiciona primer (a dalt)

        ttk.Button(frame_botons, text="Obrir URL", command=self.obrir_seleccionada).pack(side=tk.LEFT, padx=3)
        ttk.Button(frame_botons, text="Obrir Totes URLs", command=self.obrir_totes).pack(side=tk.LEFT, padx=3)
        ttk.Button(frame_botons, text="Obrir HTML", command=self.obrir_html_local).pack(side=tk.LEFT, padx=3)
        ttk.Button(frame_botons, text="Obrir Carpeta", command=self.obrir_carpeta_local).pack(side=tk.LEFT, padx=3)
        ttk.Button(frame_botons, text="Esborrar", command=self.esborrar_seleccionada).pack(side=tk.LEFT, padx=3)

        self.lbl_estat = ttk.Label(frame_botons, text="")
        self.lbl_estat.pack(side=tk.RIGHT, padx=5)

        # 2. PANELL DE LA TAULA (Posicionat a sota dels botons)
        frame_taula = ttk.Frame(root, padding=10)
        frame_taula.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

        # Scrollbar vertical (ja existent)
        scrollbar_y = ttk.Scrollbar(frame_taula, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horitzontal (NOU)
        scrollbar_x = ttk.Scrollbar(frame_taula, orient=tk.HORIZONTAL)  # <-- NOU
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)                      # <-- NOU

        columnes = ('ID', 'URL', 'ESTAT', 'RUTA')
        self.tree = ttk.Treeview(
            frame_taula,
            columns=columnes,
            show='headings',
            selectmode='browse',
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set  # <-- NOU: Vinculat a la barra horitzontal
        )
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)  # <-- NOU: Control de desplaçament X

        # Definició de capçaleres i amples
        self.tree.heading('ID', text='ID')
        self.tree.heading('URL', text='URL')
        self.tree.heading('ESTAT', text='Estat')
        self.tree.heading('RUTA', text='Ruta Fitxer HTML')

        self.tree.column('ID', width=50, minwidth=40, anchor='center')
        self.tree.column('URL', width=400, minwidth=200, anchor='w')
        self.tree.column('ESTAT', width=80, minwidth=60, anchor='center')
        self.tree.column('RUTA', width=350, minwidth=200, anchor='w')

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Detecció d'esdeveniments
        self.tree.bind('<Double-1>', lambda e: self.obrir_seleccionada())
        self.tree.bind('<Delete>', lambda e: self.esborrar_seleccionada())

        self.actualitzar_taula()


    def actualitzar_taula(self):
        """Refresca les files del Treeview amb la informació actual."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for reg in self.registres:
            estat_text = (
                'OK' if reg.correcte.strip().lower() == 'true' else 'ERROR'
            )
            self.tree.insert(
                '',
                tk.END,
                values=(reg.id, reg.url, estat_text, reg.ruta_fitxer),
            )

        self.lbl_estat.config(text=f'Total: {len(self.registres)} elements')

    def obtenir_item_seleccionat(self):
        """Retorna l'objecte ItemRegistre seleccionat o None."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('Atenció', 'Selecciona una línia de la taula.')
            return None
        index_tree = self.tree.index(selected[0])
        return self.registres[index_tree]

    def obrir_seleccionada(self):
        item = self.obtenir_item_seleccionat()
        if item:
            obrir_amb_librewolf(item.url)

    def obrir_totes(self):
        if not self.registres:
            return
        if messagebox.askyesno(
            'Confirmació',
            f'Vols obrir les {len(self.registres)} URLs a LibreWolf?',
        ):
            for reg in self.registres:
                obrir_amb_librewolf(reg.url)

    def obrir_html_local(self):
        item = self.obtenir_item_seleccionat()
        if item:
            obrir_fitxer_local(item.ruta_fitxer)

    def obrir_carpeta_local(self):
        item = self.obtenir_item_seleccionat()
        ruta = item.ruta_fitxer if item else ''
        obrir_carpeta_contenidora(ruta)

    def esborrar_seleccionada(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('Atenció', 'Selecciona un element per esborrar.')
            return

        idx = self.tree.index(selected[0])
        item = self.registres[idx]

        # Si existeix el fitxer HTML local, opcionalment l'esborrem del disc
        if item.ruta_fitxer and os.path.exists(item.ruta_fitxer):
            try:
                os.remove(item.ruta_fitxer)
            except Exception:
                pass

        del self.registres[idx]
        guardar_registres_csv(FITXER_REGISTRE, self.registres)
        self.actualitzar_taula()




if __name__ == '__main__':
    root = tk.Tk()
    app = AplicacioURLs(root)
    root.mainloop()
