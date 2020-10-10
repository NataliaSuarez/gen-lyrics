import os
import sys

carpeta_con_los_txts = sys.argv[1]
file_res = sys.argv[2]

lista_de_txts = os.listdir(carpeta_con_los_txts)

texto_final = ""

for nombre_del_txt in lista_de_txts:
    if nombre_del_txt.endswith(".txt"):
        ruta_al_archivo = carpeta_con_los_txts + "/" + nombre_del_txt 

        with open(ruta_al_archivo,'r') as f:
            texto_del_proximo_txt = f.read()
            texto_final = texto_final + "\n\n" + texto_del_proximo_txt

with open(file_res,'w') as f:
    f.write(texto_final)
