
def copiar_linies_duplicades(fitxer_origen, fitxer_desti):
    vistes = set()
    
    with open('origen.txt', 'r', encoding='utf-8') as f_in, \
         open('desti.txt', 'w', encoding='utf-8') as f_out:
        
        for linia in f_in:
            clau = "".join(linia.split())  # Ignora espais, tabuladors i salts per comparar
            
            if not clau:
                continue  # Salta les línies buides
                
            if clau not in vistes:
                vistes.add(clau)
                f_out.write(linia)  # Escriu la línia original a desti.txt
    


copiar_linies_duplicades('origen.txt', 'desti.txt')
