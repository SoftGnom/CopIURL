import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser

FITXER_DESTI = 'desti.txt'


import shutil

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



def obrir_amb_librewolf_no2(url):
    url = url.strip()
    if not url:
        return

    # Assegurem el protocol per evitar errors de navegació
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # 1. Intenta obrir la comanda nativa 'librewolf' si existeix al PATH
    if shutil.which('librewolf'):
        subprocess.Popen(['librewolf', url])
        return

    # 2. Si utilitzes Linux Mint / Flatpak, intenta executar el paquet com.librewolf.LibreWolf
    if shutil.which('flatpak'):
        comprovacio = subprocess.run(
            ['flatpak', 'info', 'com.librewolf.LibreWolf'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if comprovacio.returncode == 0:
            subprocess.Popen(['flatpak', 'run', 'com.librewolf.LibreWolf', url])
            return

    # 3. Si no es troba cap executable de LibreWolf, utilitza el navegador per defecte
    messagebox.showwarning(
        'Avís',
        "No s'ha trobat LibreWolf (ni natiu ni Flatpak). S'obrirà amb el navegador per defecte.",
    )
    webbrowser.open(url)



def obrir_amb_librewolf_no(url):
    url = url.strip()
    if not url:
        return

    # Assegurem el protocol per evitar errors de navegació
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        # Intenta obrir la URL directament amb l'executable de LibreWolf
        subprocess.Popen(['librewolf', url])
    except FileNotFoundError:
        # Si 'librewolf' no està al PATH del sistema, utilitza el navegador per defecte
        messagebox.showwarning(
            'Avís',
            "No s'ha trobat la comanda 'librewolf'. S'obrirà amb el navegador per defecte.",
        )
        webbrowser.open(url)


class AplicacioURLs:

    def __init__(self, root):
        self.root = root
        self.root.title('Llançador de URLs - LibreWolf')
        self.root.geometry('650x450')

        self.urls = []
        self.carregar_urls()

        # --- Panell de la llista ---
        frame_llista = ttk.Frame(root, padding=10)
        frame_llista.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(frame_llista)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            frame_llista,
            yscrollcommand=self.scrollbar.set,
            selectmode=tk.SINGLE,
            font=('Consolas', 10),
            bg='#f0f0f0',
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)


        # Inserim les URL a la llista
        for url in self.urls:
            self.listbox.insert(tk.END, url)

        # Doble clic per obrir la URL seleccionada
        self.listbox.bind(
            '<Double-1>', lambda event: self.obrir_seleccionada()
        )

        # Permet esborrar directament prement la tecla Supr / Delete
        self.listbox.bind('<Delete>', lambda event: self.esborrar_seleccionada())

        # --- Panell de botons ---
        frame_botons = ttk.Frame(root, padding=10)
        frame_botons.pack(fill=tk.X)

        btn_obrir = ttk.Button(
            frame_botons,
            text='Obrir Seleccionada',
            command=self.obrir_seleccionada,
        )
        btn_obrir.pack(side=tk.LEFT, padx=5)

        btn_totes = ttk.Button(
            frame_botons, text='Obrir Totes', command=self.obrir_totes
        )
        btn_totes.pack(side=tk.LEFT, padx=5)

        btn_esborrar = ttk.Button(
            frame_botons,
            text='Esborrar Seleccionada',
            command=self.esborrar_seleccionada,
        )
        btn_esborrar.pack(side=tk.LEFT, padx=5)


        self.lbl_estat = ttk.Label(
            frame_botons, text=f'Total: {len(self.urls)} URLs'
        )
        self.lbl_estat.pack(side=tk.RIGHT, padx=5)

    def carregar_urls(self):
        if os.path.exists(FITXER_DESTI):
            with open(FITXER_DESTI, 'r', encoding='utf-8') as f:
                self.urls = [linia.strip() for linia in f if linia.strip()]
        else:
            messagebox.showerror(
                'Error', f"No s'ha trobat el fitxer '{FITXER_DESTI}'."
            )

    def obrir_seleccionada(self):
        seleccio = self.listbox.curselection()
        if seleccio:
            url = self.listbox.get(seleccio[0])
            obrir_amb_librewolf(url)
        else:
            messagebox.showinfo('Atenció', 'Selecciona una URL de la llista.')

    def obrir_totes(self):
        if not self.urls:
            return
        if messagebox.askyesno(
            'Confirmació',
            f'Vols obrir les {len(self.urls)} URLs en pestanyes de LibreWolf?',
        ):
            for url in self.urls:
                obrir_amb_librewolf(url)

    def esborrar_seleccionada(self):
        seleccio = self.listbox.curselection()
        if not seleccio:
            messagebox.showinfo('Atenció', 'Selecciona una URL per esborrar.')
            return

        idx = seleccio[0]

        # 1. Eliminar de la llista de Python i del desplegable
        self.listbox.delete(idx)
        del self.urls[idx]

        # 2. Actualitzar el fitxer desti.txt amb la llista actualitzada
        with open(FITXER_DESTI, 'w', encoding='utf-8') as f:
            for url in self.urls:
                f.write(url + '\n')

        # 3. Actualitzar el comptador de la interfície
        self.lbl_estat.config(text=f'Total: {len(self.urls)} URLs')

        # 4. Seleccionar la següent línia (o la darrera si era l'última)
        if self.urls:
            nou_idx = min(idx, len(self.urls) - 1)
            self.listbox.selection_set(nou_idx)
            self.listbox.activate(nou_idx)


if __name__ == '__main__':
    root = tk.Tk()
    app = AplicacioURLs(root)
    root.mainloop()
