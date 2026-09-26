import os
import json
import requests
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

# Variable global que defineix el nom/ruta del fitxer de configuració predefinit
CONFIG_FILE_PATH = "ollama_config.json"


class OllamaClient:
    """
    Classe d'abstracció per interaccionar amb un contenidor d'Ollama.
    Carrega la configuració d'un fitxer definit a la variable global CONFIG_FILE_PATH
    i gestiona 3 contexts de dades per generar un resultat i guardar-lo en disc.
    """

    def __init__(self, config_path: str = CONFIG_FILE_PATH):
        self.config_path = Path(config_path)
        self.host: str = ""
        self.model: str = ""
        self.connect_timeout: int = 10
        self.read_timeout: int = 600
        self.keep_alive: str = "30m"
        self.options: Dict[str, Any] = {}

        # Variables per als 3 textos de context/dades
        self.purpose_context: Optional[str] = None  # Context 1: Propòsit / Instruccions
        self.data_1: Optional[str] = None          # Context 2: Primera dada
        self.data_2: Optional[str] = None          # Context 3: Segona dada

        # Carregar configuració inicial
        self._load_config()

    def _load_config(self) -> None:
        """Carrega la configuració des del fitxer JSON o en genera un de defecte complet."""
        default_config = {
            "host": "http://localhost:11434",
            "model": "laguna-xs-2.1",
            "connect_timeout": 10,
            "read_timeout": 600,
            "keep_alive": "30m",
            "options": {
                "num_ctx": 8192,
                "temperature": 0.2
            }
        }

        if not self.config_path.exists():
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
            config = default_config
        else:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except Exception as e:
                raise RuntimeError(f"Error llegint el fitxer {self.config_path}: {e}")

        self.host = config.get("host", "http://localhost:11434").rstrip("/")
        self.model = config.get("model", "laguna-xs-2.1")
        self.connect_timeout = config.get("connect_timeout", 10)
        self.read_timeout = config.get("read_timeout", 600)
        self.keep_alive = config.get("keep_alive", "30m")
        self.options = config.get("options", {"num_ctx": 8192, "temperature": 0.2})

    def test_connection(self) -> Tuple[bool, str]:
        """Comprova si el servidor Ollama respon i si té el model carregat."""
        try:
            response = requests.get(
                f"{self.host}/api/tags",
                timeout=(self.connect_timeout, 10)
            )
            if response.status_code == 200:
                models_data = response.json().get("models", [])
                available_models = [m.get("name") for m in models_data]

                if any(self.model in m for m in available_models):
                    return True, f"Connexió OK. Model '{self.model}' trobat al servidor."
                else:
                    return False, f"Servidor actiu, però el model '{self.model}' no està instal·lat."
            else:
                return False, f"Servidor Ollama va retornar codi d'error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"No s'ha pogut connectar a Ollama ({self.host}): {e}"


    # --- Carrega de contextos i dades ---
    def _read_text_or_file(self, content_or_path: str) -> str:
        """Helper per llegir directament un text o bé el contingut d'un fitxer si existeix la ruta."""
        try:
            path = Path(content_or_path)
            if path.exists() and path.is_file():
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
        except (OSError, ValueError):
            pass
        return content_or_path


    def set_purpose(self, text_or_filepath: str) -> None:
        """Estableix el context 1: Propòsit o instrucció principal de la tasca."""
        self.purpose_context = self._read_text_or_file(text_or_filepath)

    def set_data_1(self, text_or_filepath: str) -> None:
        """Estableix el context 2: Primera font de dades."""
        self.data_1 = self._read_text_or_file(text_or_filepath)

    def set_data_2(self, text_or_filepath: str) -> None:
        """Estableix el context 3: Segona font de dades."""
        self.data_2 = self._read_text_or_file(text_or_filepath)

    # --- Execució i Desat de Resultats ---

    def generate_and_save(self, relative_path: str, filename: str) -> Tuple[bool, str]:
        """Uneix els 3 textos, crida a Ollama amb les opcions del JSON i ho guarda al fitxer indicat."""
        # Validació de dades d'entrada
        if not self.purpose_context:
            return False, "Error: Falta el context de propòsit (set_purpose)."
        if not self.data_1:
            return False, "Error: Falta el primer bloc de dades (set_data_1)."
        if not self.data_2:
            return False, "Error: Falta el segon bloc de dades (set_data_2)."

        # Construcció del prompt combinat
        full_prompt = (
            f"=== PROPÒSIT / INSTRUCCIONS ===\n{self.purpose_context}\n\n"
            f"=== DADES DE ENTRADA 1 ===\n{self.data_1}\n\n"
            f"=== DADES DE ENTRADA 2 ===\n{self.data_2}\n\n"
            f"Si us plau, executa la transformació requerida seguint les instruccions anteriors."
        )

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "keep_alive": self.keep_alive,
            "options": self.options
        }

        try:
            # Enviem la petició amb el tuple de timeouts (connect_timeout, read_timeout)
            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=(self.connect_timeout, self.read_timeout)
            )

            if response.status_code == 200:
                result_json = response.json()
                output_text = result_json.get("response", "")

                # Gestió de la ruta i del fitxer de sortida (multiplataforma Mint/Windows)
                target_dir = Path(relative_path)
                target_dir.mkdir(parents=True, exist_ok=True)
                output_file_path = target_dir / filename

                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(output_text)

                return True, str(output_file_path.resolve())
            else:
                return False, f"Error d'Ollama (HTTP {response.status_code}): {response.text}"

        except requests.exceptions.Timeout:
            return False, f"Error: Temps d'espera esgotat (Timeout: {self.read_timeout}s)."
        except requests.exceptions.RequestException as e:
            return False, f"Error de xarxa/connexió amb Ollama: {str(e)}"


# --- MODE INTERACTIU MANUAL ---
if __name__ == "__main__":
    import sys

    print("==================================================")
    print("    Ollama Client - Mode Interactiu Manual        ")
    print("==================================================\n")

    
    # 2. Bucle de verificació de connexió amb opció de reintent
    while True:
        # 1. Instanciar la classe (carrega automàticament la configuració del JSON)
        ollama = OllamaClient()
        
        print("Verificant connexió amb el contenidor Ollama...")
        conn_ok, msg = ollama.test_connection()

        print(f"Estat de la connexió: {'[ OK ]' if conn_ok else '[ ERROR ]'}")
        print(f"Detall: {msg}\n")

        if conn_ok:
            break  # Connexió correcta, sortim del bucle de verificació i continuem

        print("Impossible connectar amb el contenidor d'Ollama.")
        print("Revisa el fitxer 'ollama_config.json' o comprova que el contenidor estigui actiu.")

        # (S/n) indica que prémer Enter reintenta automàticament
        reintentar = input("\nVols tornar a intentar la connexió? (-/N): ").strip().lower()
        if reintentar in ["n", "no", "not"]:
            print("Surtint del programa...")
            sys.exit(1)
        
        print("\n--------------------------------------------------\n")

    # 3. Bucle interactiu per introduir dades a mà
    while True:
        print("--------------------------------------------------")
        print(" Nova transformació de dades")
        print(" (Pots introduir text directe o la ruta a un fitxer)")
        print("--------------------------------------------------")

        # Demanar Propòsit / Context 1
        purpose_input = input("\n1. Introdueix el PROPÒSIT / INSTRUCCIONS: ").strip()
        while not purpose_input:
            purpose_input = input("   [!] El propòsit és obligatori. Torna-ho a intentar: ").strip()
        ollama.set_purpose(purpose_input)

        # Demanar Dada 1 / Context 2
        data1_input = input("\n2. Introdueix la DADA 1 (text o ruta de fitxer): ").strip()
        while not data1_input:
            data1_input = input("   [!] La Dada 1 és obligatòria. Torna-ho a intentar: ").strip()
        ollama.set_data_1(data1_input)

        # Demanar Dada 2 / Context 3
        data2_input = input("\n3. Introdueix la DADA 2 (text o ruta de fitxer): ").strip()
        while not data2_input:
            data2_input = input("   [!] La Dada 2 és obligatòria. Torna-ho a intentar: ").strip()
        ollama.set_data_2(data2_input)

        # Demanar Ruta Relativa de Sortida
        rel_path = input("\n4. Ruta relativa on guardar [Per defecte: output/reports]: ").strip()
        if not rel_path:
            rel_path = "output/reports"

        # Demanar Nom del Fitxer de Sortida
        file_name = input("5. Nom del fitxer de sortida [Per defecte: informe_generat.txt]: ").strip()
        if not file_name:
            file_name = "informe_generat.txt"

        print("\nEnviant petició a Ollama... (Això pot trigar segons la mida del model)")

        # 4. Generar el resultat i guardar-lo
        success, result_msg = ollama.generate_and_save(
            relative_path=rel_path,
            filename=file_name
        )

        print("\n================ RESULTAT ================")
        if success:
            print(" ✔ PROCESSET AMB ÈXIT!")
            print(f" Fitxer generat a: {result_msg}")
        else:
            print(" ❌ ERROR DURANT LA GENERACIÓ:")
            print(f" {result_msg}")
        print("==========================================")

        # Preguntar si vol continuar el bucle o sortir
        continuar = input("\nVols fer una altra transformació? (s/N): ").strip().lower()
        if continuar not in ["s", "si", "sí", "y", "yes"]:
            print("\nSurtint del programa. Adeu!")
            break
