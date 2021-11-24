# IEDX Backend

## Instalación 

Crear virtual env
```
$ python3 -m venv venv 
```

Activar virtual env
```
$ . venv/bin/activate
```

Instalar dependencias
```
$ pip install -r requirements.txt 
```

### Comandos comunes

Ejecutar proyecto

```
$ cd iedx 
$ python manage.py runserver
```

Ejecutar migración

```
$ python manage.py migrate
```

Crear migración con los cambios en los archivos models
```
$ python manage.py makemigrations
```
Nota: después de esto es necesario $ python manage.py migrate para que se apliquen los cambios en la BD


### Usuario root de la base de datos

- username: root
- email: root@iedx.com
### - pass: unDiaViUnaVacaSinColaVestidaDeUniforme no more!
- pass: 123





