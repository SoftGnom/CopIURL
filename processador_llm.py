import os
import json
import csv
import glob
from pathlib import Path
from typing import Dict, Any, List, Callable

# Importem la teva classe d'Ollama (assumint que s'ha guardat amb aquest nom)
try:
    from abstraccio_ollama import OllamaClient
except ImportError:
    print("[!] Avís: No s'ha trobat 'abstraccio_ollama.py'. El codi no funcionarà sense aquest fitxer.")

# ==============================================================================
# VARIABLES GLOBALS
# ==============================================================================
CARPETA_CONFIGURACIONS = "tasques_llm"
FITXER_REGISTRE_CSV = "registre_descarregues.csv"

# ==============================================================================
# FUNCIONS DE CÀRREGA (EL "SWITCH")
# Cada funció defineix una forma diferent d'obtenir la informació.
# ==============================================================================

def carregar_text_directe(valor: str, context_fila: Dict[str, str] = None) -> str:
    """Retorna el text tal qual s'ha definit al JSON."""
    return str(valor)

def carregar_des_de_fitxer(ruta: str, context_fila: Dict[str, str] = None) -> str:
    """Llegeix un fitxer de text genèric (no depèn de l'HTML actual)."""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[Error llegint {ruta}: {e}]"

def carregar_ruta_des_de_csv(columna: str, context_fila: Dict[str, str]) -> str:
    """
    Retorna el valor d'una columna del CSV per a la fila actual. 
    Molt útil per retornar 'RUTA_FITXER' i que OllamaClient llegeixi l'HTML.
    """
    if context_fila and columna in context_fila:
        return context_fila[columna]
    return f"[Error: Columna {columna} no trobada al CSV]"

def carregar_resultat_anterior(clau_anterior: str, context_fila: Dict[str, str] = None) -> str:
    """
    (Per al futur) Llegeix la sortida d'una execució LLM anterior.
    Requereix implementar on es desen aquests resultats temporals en memòria.
    """
    # Ex: retornar cache_resultats.get(context_fila['ID'], {}).get(clau_anterior, "")
    return "[Pendent d'implementar: Càrrega de resultats anteriors]"

# Aquest és el "switch" que mapeja els identificadors de tipus del JSON amb les funcions.
METODES_CARREGA: Dict[str, Callable] = {
    "directe": carregar_text_directe,
    "fitxer_static": carregar_des_de_fitxer,
    "columna_csv": carregar_ruta_des_de_csv,
    "resultat_anterior": carregar_resultat_anterior
    # Aquí podràs afegir noves funcions en el futur...
}


# ==============================================================================
# CLASSE PRINCIPAL DEL PROCESSADOR
# ==============================================================================
class ProcessadorTasquesLLM:
    def __init__(self):
        # Assegurem que la carpeta de configuracions existeix
        os.makedirs(CARPETA_CONFIGURACIONS, exist_ok=True)
        self.client_llm = None
        self.files_csv = self._llegir_csv_registre()

    def _llegir_csv_registre(self) -> List[Dict[str, str]]:
        """Carrega totes les files del CSV de registre."""
        files = []
        if not os.path.exists(FITXER_REGISTRE_CSV):
            print(f"[!] Error: No s'ha trobat el fitxer {FITXER_REGISTRE_CSV}")
            return files

        with open(FITXER_REGISTRE_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                # Només volem processar els que s'han descarregat correctament
                if row.get('CORRECTE', 'False').lower() == 'true':
                    files.append(row)
        return files

    def obtenir_llista_tasques(self) -> List[str]:
        """Obté i ordena els fitxers JSON per garantir l'ordre 001, 002, etc."""
        patro = os.path.join(CARPETA_CONFIGURACIONS, "*.json")
        fitxers = glob.glob(patro)
        fitxers.sort()  # L'ordre alfabètic ordenarà correctament els números (001-xxx, 002-xxx)
        return fitxers

    def _resoldre_input(self, definicio_input: Dict[str, str], context_fila: Dict[str, str] = None) -> str:
        """
        Donada la configuració d'un input des del JSON i la fila del CSV actual,
        executa la funció corresponent del switch i retorna les dades.
        """
        tipus = definicio_input.get("tipus")
        valor = definicio_input.get("valor")

        if tipus in METODES_CARREGA:
            funció_carrega = METODES_CARREGA[tipus]
            return funció_carrega(valor, context_fila)
        else:
            return f"[Error: Tipus de càrrega '{tipus}' desconegut]"

    def executar_totes_les_tasques(self):
        """Mètode principal que orquestra tot el procés."""
        if not self.files_csv:
            print("[i] No hi ha cap URL vàlida al registre per processar.")
            return

        tasques = self.obtenir_llista_tasques()
        if not tasques:
            print(f"[i] No s'han trobat fitxers de tasca JSON a '{CARPETA_CONFIGURACIONS}'.")
            return

        print(f"\n[+] Iniciant motor LLM. {len(tasques)} tasques detectades.")
        
        # Inicialitzem OllamaClient només un cop
        self.client_llm = OllamaClient()
        conn_ok, msg = self.client_llm.test_connection()
        if not conn_ok:
            print(f"[!] Error de connexió amb Ollama: {msg}")
            return
        
        print("[+] Connexió amb Ollama establerta correctament.\n")

        # Bucle 1: Per cada fitxer JSON (Tasques en ordre 001, 002...)
        for ruta_tasca in tasques:
            with open(ruta_tasca, 'r', encoding='utf-8') as f:
                config_tasca = json.load(f)

            nom_tasca = config_tasca.get("nom_tasca", os.path.basename(ruta_tasca))
            inputs_config = config_tasca.get("inputs", {})
            sortida_config = config_tasca.get("sortida", {})
            
            print(f"==================================================")
            print(f" Executant Tasca: {nom_tasca}")
            print(f"==================================================")

            # ESTRUCTURA INTEL·LIGENT:
            # 1. Carreguem en memòria les dades ESTÀTIQUES (les que no depenen del CSV actual)
            # per no haver de recarregar-les per cada fitxer HTML.
            inputs_estatics = {}
            for clau, config in inputs_config.items():
                if config.get("tipus") in ["directe", "fitxer_static"]:
                    inputs_estatics[clau] = self._resoldre_input(config)
            
            # Bucle 2: Iterem per cada URL/HTML descarregat
            for index, fila in enumerate(self.files_csv, start=1):
                id_html = fila.get("ID", str(index))
                
                print(f"  -> Processant ID {id_html} ({fila.get('URL', '')[:40]}...)")
                
                # 2. Resolem la part DINÀMICA i assignem tot al client Ollama
                # Utilitzem un mapping per cridar el mètode adequat de l'OllamaClient de forma flexible.
                mapa_metodes = {
                    "purpose_context": self.client_llm.set_purpose,
                    "data_1": self.client_llm.set_data_1,
                    "data_2": self.client_llm.set_data_2
                }

                inputs_complets = True
                
                for clau, metode_set in mapa_metodes.items():
                    if clau in inputs_config:
                        # Si és estàtic, ja el tenim a memòria
                        if clau in inputs_estatics:
                            dada_final = inputs_estatics[clau]
                        # Si és dinàmic (ex: columna del CSV per trobar la ruta de l'HTML)
                        else:
                            dada_final = self._resoldre_input(inputs_config[clau], fila)
                        
                        # Assignem la dada a l'Ollama
                        metode_set(dada_final)
                    else:
                        inputs_complets = False
                        print(f"     [!] Falta l'input '{clau}' al JSON.")

                if not inputs_complets:
                    print(f"     [!] Es salta l'ID {id_html} perquè falten paràmetres a la configuració.")
                    continue

                # 3. Executem l'Ollama i guardem
                carpeta_desti = sortida_config.get("carpeta_relativa", "output/llm")
                nom_arxiu = f"{sortida_config.get('prefix_fitxer', 'out_')}{id_html}.txt"

                exit_llm, msg = self.client_llm.generate_and_save(carpeta_desti, nom_arxiu)

                if exit_llm:
                    print(f"     [OK] Guardat a {nom_arxiu}")
                else:
                    print(f"     [ERROR] {msg}")


# ==============================================================================
# EXECUCIÓ PER DEFECTE
# ==============================================================================
if __name__ == "__main__":
    processador = ProcessadorTasquesLLM()
    processador.executar_totes_les_tasques()
