# gen-lyrics

Generador de textos a partir de canciones y archivos pdf.

# Preparación de datos para la generación de texto utilizando [aitextgen](https://docs.aitextgen.io/)

La idea es generar un dataset para la generación de texto a partir de una recopilación de canciones de un artista, por ejemplo las del Flaco Spinetta.

## Sobre el dataset

Vamos a recopilar todos los textos en un archivo de al menos 500KB, el mismo debería estar filtrado de carácteres innecesarios como números de páginas o títulos, símbolos, etc.

Vamos a iniciar recopilando las canciones según artísta/banda del sitio letras.com.

## Requerimientos

Se sugiere la utilización de un virtualenv.

Ejemplo de uso

`virtualenv --python=python3 text-spinetta`
`source text-spinetta/bin/activate`

Una vez activado el `virtualenv` vamos a instalar las siguientes librerias:

transformers==2.9.1
pytorch-lightning==0.8.4
aitextgen
BeautifulSoup4
pdfminer3k

Éstas librerias están en el archivo `requirements.txt`, para instalarlas corremos el comando `pip install -r requirements.txt`

Las siguientes son librerias relacionadas al entrenamiento. En particular aitextgen es la libreria que vamos a utilizar para la generación de texto con IA que utiliza [GPT-2](https://openai.com/blog/better-language-models/)
```
transformers==2.9.1
pytorch-lightning==0.8.4
aitextgen
```

Por otro lado `BeautifulSoup4` y `pdfminer3k` las vamos a utilizar en los scripts para recopilar texto de una página de letras de canciones o de archivos pdf.

## Recopilar las letras de un mismo artista

Utilizamos el script `songs2txt.py` donde los argumento serán `luis-alberto-spinetta` ó la banda que elijamos.

Para utilizar el script podemos hacer `python songs2txt.py luis-alberto-spinetta`. Eso va a crear una carpeta llamada `luis-alberto-spinetta` con todos los archivos .txt con sus letras.

Siguiente el ejemplo podemos utilizar todas las letras de las bandas en las que participó el flaco.
*Se hace una selección de todas las bandas para que el dataset resultante tenga más datos, con lo cual el resultado no será sólo de las letras escritas por el flaco.*

Letras de bandas utilizadas para el entrenamiento: luis-alberto-spinetta, pescado-rabioso, almendra, invisible, spinetta-jade.

## Extracción de texto a partir de PDF

Por otro lado se puede extraer el texto a partir de un archivo .pdf.

Para la extración podemos utilizar el script `pdf2txt.py` corriendo el comando `python pdf2txt.py guitarra-negra.pdf algo.txt`

Ejemplo con el libro de poemas de Spinetta titulado *Guitarra Negra*.

## Recopilación de textos en uno solo

Para juntar todos los textos podemos utilizar el script `merge-texts.py`. Le vamos a pasar como argumento el path de la carpeta donde van a estar situados los textos, y el nombre del archivo txt resultante.

`python merge-texts.py "./luis-alberto-spinetta" luis-alberto-spinetta.txt`

Este script lo vamos a utilizar para juntar todos los textos, de todas las formaciones en conjunto con los txt de los pdf. Finalmente tendremos un solo archivo que debe pesar 500 kb maso.

## Filtrado con regex

Para el filtrado con expresiones regulares no hay nada definido ya que depende de los textos que estemos utilizando, pero se pueden utilizar [regex101](https://regex101.com/) que es una herramienta para evaluar las regex y testearlas en el sitio. 

Acá un ejemplo

```python
import re
import sys

text_name = sys.argv[1] # Ejemplo "some_text.txt"
res_text_name = sys.argv[2] # Ejemplo "res_text.txt"

with open(text_name,'r') as f:
  texto = f.read()

texto_modificado = re.sub(r'.+ - ', '', texto) ## acá hay que modificar el regex

with open(res_text_name,'w') as f:
  f.write(texto_modificado)
```

## Otras procesamientos

Una posibilidad es que necesitemos hacer una traducción, en ese caso podemos utilizar [googletrans](https://pypi.org/project/googletrans/) tirando en la consola `pip install googletrans`

# Entrenamiento

Una vez que tengamos un lindo dataset, podemos avanzar con el entrenamiento. 

## Entrenamiento con colab

Éste es un ejemplo en el que se utiliza `aitextgen` en una máquina de [colab](https://colab.research.google.com/notebooks/intro.ipynb) lo que nos permite tomar el entrenamiento previo que utiliza la herramienta.
La máquina se puede configurar para hacer uso de GPU y basicamente nos permite tirar lineas de codigo bash (utilizando !)o python y dejar notas en markdown.

*La alternativa libre a colab es [Jupyter](https://jupyter.org/)*

En principio vamos a instalar las mismas librerias que en local

```bash
pip install transformers==2.9.1
pip install pytorch-lightning==0.8.4
pip install aitextgen
```
Además es necesario subir el dataset a la máquina, se puede utilizar drive o directamente subir el archivo .txt desde la
herramienta. 

Para conectar colab con drive: 

```python
from google.colab import drive
drive.mount('/content/drive')
```
Y luego ponemos a entrenar la IA:

```python
from aitextgen import aitextgen

ai = aitextgen(tf_gpt2="124M", to_gpu=True) #se puede setear con GPU o no.

file_path = "/content/spinetta.txt" # Ruta de nuestro dataset
ai.train(file_path,
         line_by_line=False,
         num_steps=5000,
         generate_every=1000,
         save_every=1000,
         save_gdrive=False,
         learning_rate=1e-4,
         batch_size=1,
         )
# ai.generate_to_file(n=10, prompt="Río salvaje", max_length=100, temperature=1.2)
```

## Entrenamiento en entorno local

En este caso, definimos el script `generator-training` que utilizamos para el entrenamiento de la red de manera local. Podemos configurar el uso de CPU o GPU y algunas variables más especificas para la IA y el entrenamiento.

El dataset utilizado en el TokenDataset será la recopilación de los textos normalizados y compilados en un archivo txt. Como ejemplo utilizamos spinetta.txt. 

Al ejecutar el script va a comenzar el entrenamiento de la red que va a durar minutos +/- tiempo según los recursos de nuestra compu. Si tenés GPU mandale true nomás en la config ;)

Durante el entrenamiento, vamos a ir observando la generación de textos intermedios según la configuración de nuestro entrenamiento. 

Como resultado esperamos obtener el modelo entrenado en la carpeta `trained_model` y algunos archivos como `aitextgen-merges` y `aitextgen-vocab` que serán útiles para volver a utilizar nuestro modelo.
Además se va a crear un archivo `ATG_FECHA_OTROSNUMERITOS.txt` con la generación de un texto que comience así: "Río salvaje".

Ésta primer generación de texto la configuramos en la siguiente línea del script:

`ai.generate_to_file(n=10, prompt="En la neblina sus huellas", max_length=100, temperature=1.2)`

donde 10 es el número de generaciones y prompt indica el texto con la que se iniciará la generación, max_length será la extensión en cant de caracteres y la *temperature* será el nivel de repetición o creatividad que tenga la máquina al momento de generar nuevos textos.

*The higher the temperature, the more creative* (Higher temperatures work better (e.g. 0.7 - 1.0) to generate more interesting text, while other frameworks work better between 0.2 - 0.5)

## Generación de texto

Una vez que tenemos un modelo entrenado, ya podemos utilizarlo para generar texto sin hacer el entrenamiento nuevamente.

Utilizamos el script `generator-with-trained-model` que toma el modelo `pytorch_model.bin` de la carpeta trained_model junto con otros archivos y una configuración para generar el texto que le pasemos como argumento.

desde la consola corremos:  `python generator-with-trained-model.py 'Una frase falopa que comience la canción'`

lo que nos va a generar 10 textos de 140 caracteres. 

Si queremos otra definición la podemos cambiar desde el script directamente.


:sparkles: :sparkles: :sparkles: