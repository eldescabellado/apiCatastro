se a creado el CRUD indibidual para cada tabla que se visualiza en schema.sql, ademas de hacer el CRUD para la ficha completa.
se a creado el archivo schema donde se encontrara el schema necesario para los diferentes metodos, de igual forma esta el 
archivo models el cual contiene los modelos de cada tabla involucrada, se a hecho un Dockerfile basico y su requierements.txt,
e colocado una base de datos de prueba loca (porfavor cambiarla para hacer alguna prueba)

*El crud para /fichas/ afecta solo a el models FichaORM el cual es la representacion de la tabla fichas_catastrales

FichaCatastral{
id	integer
title: Id
codigo_catastral*	string
title: Codigo Catastral
maxLength: 50
fecha_registro	string($date)
title: Fecha Registro
tipo_predio*	string
title: Tipo Predio
Enum:
[ urbano, rural ]
area_terreno*	number
title: Area Terreno
exclusiveMinimum: 0
area_construida	number
title: Area Construida
minimum: 0
avaluo_catastral	number
title: Avaluo Catastral
minimum: 0
created_at	string($date-time)
title: Created At
updated_at	string($date-time)
title: Updated At
deleted_at	string($date-time)
title: Deleted At
}

*El crud para /propietarios/ afecta solo a el models PropietarioORM el cual es la representacion de la tabla propietarios

Propietario{
id	integer
title: Id
ficha_id	integer
title: Ficha Id
nombre_completo*	string
title: Nombre Completo
maxLength: 200
tipo_documento*	string
title: Tipo Documento
Enum:
[ CC, NIT, CE, TI, PAS ]
numero_documento*	string
title: Numero Documento
maxLength: 20
telefono	string
title: Telefono
maxLength: 20
email	string
title: Email
maxLength: 100
}

*El crud para /direcciones/ afecta solo a el models DireccionORM el cual es la representacion de la tabla direcciones_predios

DireccionPredio{
id	integer
title: Id
ficha_id	integer
title: Ficha Id
departamento*	string
title: Departamento
maxLength: 100
municipio*	string
title: Municipio
maxLength: 100
barrio	string
title: Barrio
maxLength: 100
direccion*	string
title: Direccion
maxLength: 200
coordenadas_norte	number
title: Coordenadas Norte
coordenadas_este	number
title: Coordenadas Este
 
}

*El crud para /servicios/ afecta solo al models ServiciosORM el cual es la representacion de la tabla servicios_publicos

ServiciosPublicos{
id	integer
title: Id
ficha_id	integer
title: Ficha Id
acueducto	boolean
title: Acueducto
default: false
alcantarillado	boolean
title: Alcantarillado
default: false
energia	boolean
title: Energia
default: false
gas	boolean
title: Gas
default: false
telefono	boolean
title: Telefono
default: false
internet	boolean
title: Internet
default: false
recoleccion_basuras	boolean
title: Recoleccion Basuras
default: false
}

*El crud para /caracteristicas/ afecta solo al models CaracteristicaORM el cual es la representacion de la tabla caracteristicas_construccion

CaracteristicaConstruccion{
id	integer
title: Id
ficha_id	integer
title: Ficha Id
tipo_construccion*	string
title: Tipo Construccion
maxLength: 50
numero_pisos*	integer
title: Numero Pisos
maximum: 50
minimum: 1
estado_conservacion*	string
title: Estado Conservacion
Enum:
Array [ 4 ]
año_construccion	integer
title: Año Construccion
}

*El crud para /linderos/ afecta solo al models LinderoORM el cual es la representacion de la tabla linderos

Lindero{
id	integer
title: Id
ficha_id*	integer
title: Ficha Id
orientacion*	string
title: Orientacion
Enum:
[ norte, sur, este, oeste ]
descripcion*	string
title: Descripcion
longitud	number
title: Longitud
minimum: 0
 
}

todos los crud mencionados ateriormente tienen un get sin filtro y otro con un filtro por id.

el crud para /fichas_completas/ afecta a todas las tablas que se encuentran en el models, ademas este crud usa todos los esquemas unidos
en uno solo para guardar y responder, el filtro actuar es con el codigo_ficha para poder traer una ficha en especifico, modificarla o eliminarla.
el schema utilizado aqui es SchemaGuardarFichaCatastral el cual se detalla en el archivo schema.py

SchemaGuardarFichaCatastral{
ficha*	FichaCatastral{
id	integer
title: Id
codigo_catastral*	string
title: Codigo Catastral
maxLength: 50
fecha_registro	string($date)
title: Fecha Registro
tipo_predio*	string
title: Tipo Predio
Enum:
[ urbano, rural ]
area_terreno*	number
title: Area Terreno
exclusiveMinimum: 0
area_construida	number
title: Area Construida
minimum: 0
avaluo_catastral	number
title: Avaluo Catastral
minimum: 0
created_at	string($date-time)
title: Created At
updated_at	string($date-time)
title: Updated At
deleted_at	string($date-time)
title: Deleted At
 
}
propietario*	Propietario{
id	integer
title: Id
ficha_id	integer
title: Ficha Id
nombre_completo*	string
title: Nombre Completo
maxLength: 200
tipo_documento*	string
title: Tipo Documento
Enum:
Array [ 5 ]
numero_documento*	string
title: Numero Documento
maxLength: 20
telefono	string
title: Telefono
maxLength: 20
email	string
title: Email
maxLength: 100
 
}
direccion*	DireccionPredio{
id	integer
title: Id
ficha_id	integer
title: Ficha Id
departamento*	string
title: Departamento
maxLength: 100
municipio*	string
title: Municipio
maxLength: 100
barrio	string
title: Barrio
maxLength: 100
direccion*	string
title: Direccion
maxLength: 200
coordenadas_norte	number
title: Coordenadas Norte
coordenadas_este	number
title: Coordenadas Este
 
}
servicios_publicos*	ServiciosPublicos{
id	integer
title: Id
ficha_id	integer
title: Ficha Id
acueducto	boolean
title: Acueducto
default: false
alcantarillado	boolean
title: Alcantarillado
default: false
energia	boolean
title: Energia
default: false
gas	boolean
title: Gas
default: false
telefono	boolean
title: Telefono
default: false
internet	boolean
title: Internet
default: false
recoleccion_basuras	boolean
title: Recoleccion Basuras
default: false
 
}
caracteristicas_construccion	CaracteristicaConstruccion{
id	integer
title: Id
ficha_id	integer
title: Ficha Id
tipo_construccion*	string
title: Tipo Construccion
maxLength: 50
numero_pisos*	integer
title: Numero Pisos
maximum: 50
minimum: 1
estado_conservacion*	string
title: Estado Conservacion
Enum:
[ excelente, bueno, regular, malo ]
año_construccion	integer
title: Año Construccion
 
}
linderos	Linderos[
title: Linderos
Lindero{
id	integer
title: Id
ficha_id*	integer
title: Ficha Id
orientacion*	string
title: Orientacion
Enum:
[ norte, sur, este, oeste ]
descripcion*	string
title: Descripcion
longitud	number
title: Longitud
minimum: 0
 
}]
 
}