# La funcion principal de este programa es  para concatenar varios archivos pdf en uno solo



## Para este programa tener instalado python3
## Instala virtualenv

pip install virtualenv
### Una vez instalado, puedes crear un entorno virtual con virtualenv nombre_del_entorno y activarlo con .\nombre_del_entorno\Scripts\activate (en Windows) 

## Crea entorno virtual con 
virtualenv venv


## Activa entorno virtual de python
.\venv\Scripts\activate

## Instala requeriments con el comando

pip install -r requirements.txt

## Puedes ejecutar el programa con :
 
 python lmergepdf.py

## Tambien puedes generar un ejecutable con :

pyinstaller --onefile --windowed --icon=icono.ico lmergepdf.py

## Al generar el ejecutable se crean dos carpetas una llamada build y la otra llamada dist



## Después de ejecutarlo, tendrás dentro de la carpeta dist lo siguiente:


/dist/
└── lmergepdf.exe

ese es tu archivo ejecutable 