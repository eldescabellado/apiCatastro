from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from services import engine
from typing import Union
from sqlalchemy.sql import text
from sqlalchemy.orm import  joinedload


import math

import os
from dotenv import load_dotenv

load_dotenv('.env')


app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URI_SERVIDOR'])

origins = [
    
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = engine.connect()


@app.get("/")
async def root():
    return {"message": "API Catastro"}

# ...existing code...
from fastapi import FastAPI, HTTPException, BackgroundTasks, Path
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from services import engine
from typing import Union, List
from sqlalchemy.sql import text
from sqlalchemy.orm import  joinedload

import math

import os
from dotenv import load_dotenv

# nuevos imports para modelos
from models import (
    FichaCatastral as FichaORM,
    Propietario as PropietarioORM,
    DireccionPredio as DireccionORM,
    ServiciosPublicos as ServiciosORM,
    CaracteristicaConstruccion as CaracteristicaORM,
    Lindero as LinderoORM,
)
from schema import (
    FichaCatastral as FichaSchema,
    Propietario as PropietarioSchema,
    DireccionPredio as DireccionSchema,
    ServiciosPublicos as ServiciosSchema,
    CaracteristicaConstruccion as CaracteristicaSchema,
    Lindero as LinderoSchema,
)
from schema import SchemaGuardarFichaCatastral

load_dotenv('.env')


app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URI_SERVIDOR'])

origins = [
    
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = engine.connect()


@app.get("/")
async def root():
    return {"message": "API Catastro"}


# --------------------
# CRUD: fichas_catastrales
# --------------------
@app.get("/fichas/", response_model=List[FichaSchema])
def list_fichas():
    items = db.session.query(FichaORM).filter(FichaORM.deleted_at == None).all()
    return items

@app.get("/fichas/{ficha_id}", response_model=FichaSchema)
def get_ficha(ficha_id: int = Path(..., ge=1)):
    item = db.session.get(FichaORM, ficha_id)
    if not item or item.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Ficha no encontrada")
    return item

@app.post("/fichas/", response_model=FichaSchema, status_code=201)
def create_ficha(payload: FichaSchema):
    obj = FichaORM(**payload.dict(exclude_unset=True, exclude={"id","created_at","updated_at","deleted_at"}))
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.put("/fichas/{ficha_id}", response_model=FichaSchema)
def update_ficha(ficha_id: int, payload: FichaSchema):
    obj = db.session.get(FichaORM, ficha_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Ficha no encontrada")
    data = payload.dict(exclude_unset=True, exclude={"id","created_at","updated_at","deleted_at"})
    for k, v in data.items():
        setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.delete("/fichas/{ficha_id}", status_code=204)
def delete_ficha(ficha_id: int):
    obj = db.session.get(FichaORM, ficha_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Ficha no encontrada")
    # soft delete
    obj.deleted_at = datetime.utcnow()
    db.session.commit()
    return {}


# --------------------
# CRUD: propietarios
# --------------------
@app.get("/propietarios/", response_model=List[PropietarioSchema])
def list_propietarios():
    return db.session.query(PropietarioORM).all()

@app.get("/propietarios/{prop_id}", response_model=PropietarioSchema)
def get_propietario(prop_id: int = Path(..., ge=1)):
    obj = db.session.get(PropietarioORM, prop_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return obj

@app.post("/propietarios/", response_model=PropietarioSchema, status_code=201)
def create_propietario(payload: PropietarioSchema):
    obj = PropietarioORM(**payload.dict(exclude_unset=True, exclude={"id"}))
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.put("/propietarios/{prop_id}", response_model=PropietarioSchema)
def update_propietario(prop_id: int, payload: PropietarioSchema):
    obj = db.session.get(PropietarioORM, prop_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    data = payload.dict(exclude_unset=True, exclude={"id"})
    for k, v in data.items():
        setattr(obj, k, v)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.delete("/propietarios/{prop_id}", status_code=204)
def delete_propietario(prop_id: int):
    obj = db.session.get(PropietarioORM, prop_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    db.session.delete(obj)
    db.session.commit()
    return {}


# --------------------
# CRUD: direcciones_predios
# --------------------
@app.get("/direcciones/", response_model=List[DireccionSchema])
def list_direcciones():
    return db.session.query(DireccionORM).all()

@app.get("/direcciones/{dir_id}", response_model=DireccionSchema)
def get_direccion(dir_id: int = Path(..., ge=1)):
    obj = db.session.get(DireccionORM, dir_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return obj

@app.post("/direcciones/", response_model=DireccionSchema, status_code=201)
def create_direccion(payload: DireccionSchema):
    obj = DireccionORM(**payload.dict(exclude_unset=True, exclude={"id"}))
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.put("/direcciones/{dir_id}", response_model=DireccionSchema)
def update_direccion(dir_id: int, payload: DireccionSchema):
    obj = db.session.get(DireccionORM, dir_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    data = payload.dict(exclude_unset=True, exclude={"id"})
    for k, v in data.items():
        setattr(obj, k, v)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.delete("/direcciones/{dir_id}", status_code=204)
def delete_direccion(dir_id: int):
    obj = db.session.get(DireccionORM, dir_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    db.session.delete(obj)
    db.session.commit()
    return {}


# --------------------
# CRUD: servicios_publicos
# --------------------
@app.get("/servicios/", response_model=List[ServiciosSchema])
def list_servicios():
    return db.session.query(ServiciosORM).all()

@app.get("/servicios/{srv_id}", response_model=ServiciosSchema)
def get_servicio(srv_id: int = Path(..., ge=1)):
    obj = db.session.get(ServiciosORM, srv_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return obj

@app.post("/servicios/", response_model=ServiciosSchema, status_code=201)
def create_servicio(payload: ServiciosSchema):
    obj = ServiciosORM(**payload.dict(exclude_unset=True, exclude={"id"}))
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.put("/servicios/{srv_id}", response_model=ServiciosSchema)
def update_servicio(srv_id: int, payload: ServiciosSchema):
    obj = db.session.get(ServiciosORM, srv_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    data = payload.dict(exclude_unset=True, exclude={"id"})
    for k, v in data.items():
        setattr(obj, k, v)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.delete("/servicios/{srv_id}", status_code=204)
def delete_servicio(srv_id: int):
    obj = db.session.get(ServiciosORM, srv_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.session.delete(obj)
    db.session.commit()
    return {}


# --------------------
# CRUD: caracteristicas_construccion
# --------------------
@app.get("/caracteristicas/", response_model=List[CaracteristicaSchema])
def list_caracteristicas():
    return db.session.query(CaracteristicaORM).all()

@app.get("/caracteristicas/{c_id}", response_model=CaracteristicaSchema)
def get_caracteristica(c_id: int = Path(..., ge=1)):
    obj = db.session.get(CaracteristicaORM, c_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Característica no encontrada")
    return obj

@app.post("/caracteristicas/", response_model=CaracteristicaSchema, status_code=201)
def create_caracteristica(payload: CaracteristicaSchema):
    obj = CaracteristicaORM(**payload.dict(exclude_unset=True, exclude={"id"}))
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.put("/caracteristicas/{c_id}", response_model=CaracteristicaSchema)
def update_caracteristica(c_id: int, payload: CaracteristicaSchema):
    obj = db.session.get(CaracteristicaORM, c_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Característica no encontrada")
    data = payload.dict(exclude_unset=True, exclude={"id"})
    for k, v in data.items():
        setattr(obj, k, v)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.delete("/caracteristicas/{c_id}", status_code=204)
def delete_caracteristica(c_id: int):
    obj = db.session.get(CaracteristicaORM, c_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Característica no encontrada")
    db.session.delete(obj)
    db.session.commit()
    return {}


# --------------------
# CRUD: linderos
# --------------------
@app.get("/linderos/", response_model=List[LinderoSchema])
def list_linderos():
    return db.session.query(LinderoORM).all()

@app.get("/linderos/{l_id}", response_model=LinderoSchema)
def get_lindero(l_id: int = Path(..., ge=1)):
    obj = db.session.get(LinderoORM, l_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lindero no encontrado")
    return obj

@app.post("/linderos/", response_model=LinderoSchema, status_code=201)
def create_lindero(payload: LinderoSchema):
    obj = LinderoORM(**payload.dict(exclude_unset=True, exclude={"id"}))
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.put("/linderos/{l_id}", response_model=LinderoSchema)
def update_lindero(l_id: int, payload: LinderoSchema):
    obj = db.session.get(LinderoORM, l_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lindero no encontrado")
    data = payload.dict(exclude_unset=True, exclude={"id"})
    for k, v in data.items():
        setattr(obj, k, v)
    db.session.commit()
    db.session.refresh(obj)
    return obj

@app.delete("/linderos/{l_id}", status_code=204)
def delete_lindero(l_id: int):
    obj = db.session.get(LinderoORM, l_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lindero no encontrado")
    db.session.delete(obj)
    db.session.commit()
    return {}

# --------------------
# CRUD: Ficha Catastral Completa
# --------------------
@app.post("/fichas_completas/", response_model=List[FichaSchema])
def create_ficha_completa(payload: List[SchemaGuardarFichaCatastral]):
    created_fichas = []
    try:
        for item in payload:
            # Crear ficha catastral
            ficha_data = item.ficha.dict(exclude_unset=True, exclude={"id","created_at","updated_at","deleted_at"})
            ficha_obj = FichaORM(**ficha_data)
            db.session.add(ficha_obj)
            db.session.flush()  # asigna id sin hacer commit

            # Crear propietario
            if getattr(item, "propietario", None):
                prop_data = item.propietario.dict(exclude_unset=True, exclude={"id"})
                prop_data['ficha_id'] = ficha_obj.id
                prop_obj = PropietarioORM(**prop_data)
                db.session.add(prop_obj)

            # Crear dirección predio
            if getattr(item, "direccion", None):
                dir_data = item.direccion.dict(exclude_unset=True, exclude={"id"})
                dir_data['ficha_id'] = ficha_obj.id
                dir_obj = DireccionORM(**dir_data)
                db.session.add(dir_obj)

            # Crear servicios públicos
            if getattr(item, "servicios_publicos", None):
                srv_data = item.servicios_publicos.dict(exclude_unset=True, exclude={"id"})
                srv_data['ficha_id'] = ficha_obj.id
                srv_obj = ServiciosORM(**srv_data)
                db.session.add(srv_obj)

            # Crear característica de construcción (si viene una)
            if getattr(item, "caracteristicas_construccion", None):
                car_data = item.caracteristicas_construccion.dict(exclude_unset=True, exclude={"id"})
                car_data['ficha_id'] = ficha_obj.id
                car_obj = CaracteristicaORM(**car_data)
                db.session.add(car_obj)

            # Crear linderos (si vienen como lista)
            if getattr(item, "linderos", None):
                for lindero in item.linderos:
                    lind_data = lindero.dict(exclude_unset=True, exclude={"id"})
                    lind_data['ficha_id'] = ficha_obj.id
                    lind_obj = LinderoORM(**lind_data)
                    db.session.add(lind_obj)

            created_fichas.append(ficha_obj)

        db.session.commit()

        # refrescar instancias para devolver datos completos
        for obj in created_fichas:
            db.session.refresh(obj)

        return created_fichas

    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/fichas_completas/", response_model=SchemaGuardarFichaCatastral)
def get_ficha_completa(codigo: str ):
    """
    Obtener una ficha completa filtrando por codigo_catastral.
    Parámetro query required: ?codigo=001-2023-URB-001
    """
    if not codigo:
        raise HTTPException(status_code=400, detail="Parámetro 'codigo' requerido")

    ficha = (
        db.session.query(FichaORM)
        .options(
            joinedload(FichaORM.propietario),
            joinedload(FichaORM.direccion),
            joinedload(FichaORM.servicios_publicos),
            joinedload(FichaORM.caracteristicas),
            joinedload(FichaORM.linderos),
        )
        .filter(FichaORM.codigo_catastral == codigo, FichaORM.deleted_at == None)
        .one_or_none()
    )

    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha no encontrada")

    # Construir respuesta usando los schemas Pydantic (deben tener orm_mode = True)
    response = SchemaGuardarFichaCatastral(
        ficha=FichaSchema.from_orm(ficha),
        propietario=PropietarioSchema.from_orm(ficha.propietario) if getattr(ficha, "propietario", None) else None,
        direccion=DireccionSchema.from_orm(ficha.direccion) if getattr(ficha, "direccion", None) else None,
        servicios_publicos=ServiciosSchema.from_orm(ficha.servicios_publicos) if getattr(ficha, "servicios_publicos", None) else None,
        caracteristicas_construccion=[CaracteristicaSchema.from_orm(c) for c in (ficha.caracteristicas or [])],
        linderos=[LinderoSchema.from_orm(l) for l in (ficha.linderos or [])],
    )

    return response

@app.put("/fichas_completas/{codigo}", response_model=SchemaGuardarFichaCatastral)
def update_ficha_completa(codigo: str, payload: SchemaGuardarFichaCatastral):
    """
    Actualiza una ficha completa identificada por codigo_catastral.
    Actualiza ficha y entidades anidadas (propietario, direccion, servicios, caracteristicas y linderos).
    Si una sub-entidad viene como null se elimina; las listas (caracteristicas, linderos) se reemplazan.
    """
    ficha = (
        db.session.query(FichaORM)
        .options(
            joinedload(FichaORM.propietario),
            joinedload(FichaORM.direccion),
            joinedload(FichaORM.servicios_publicos),
            joinedload(FichaORM.caracteristicas),
            joinedload(FichaORM.linderos),
        )
        .filter(FichaORM.codigo_catastral == codigo, FichaORM.deleted_at == None)
        .one_or_none()
    )

    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha no encontrada")

    try:
        # ---- actualizar campos de la ficha principal ----
        ficha_data = payload.ficha.dict(exclude_unset=True, exclude={"id", "created_at", "updated_at", "deleted_at"})
        for k, v in ficha_data.items():
            setattr(ficha, k, v)
        ficha.updated_at = datetime.utcnow()

        # ---- propietario: actualizar / crear / eliminar ----
        if getattr(payload, "propietario", None) is None:
            if getattr(ficha, "propietario", None):
                db.session.delete(ficha.propietario)
        else:
            prop_data = payload.propietario.dict(exclude_unset=True, exclude={"id"})
            if getattr(ficha, "propietario", None):
                for k, v in prop_data.items():
                    setattr(ficha.propietario, k, v)
            else:
                prop_data["ficha_id"] = ficha.id
                db.session.add(PropietarioORM(**prop_data))

        # ---- direccion: actualizar / crear / eliminar ----
        if getattr(payload, "direccion", None) is None:
            if getattr(ficha, "direccion", None):
                db.session.delete(ficha.direccion)
        else:
            dir_data = payload.direccion.dict(exclude_unset=True, exclude={"id"})
            if getattr(ficha, "direccion", None):
                for k, v in dir_data.items():
                    setattr(ficha.direccion, k, v)
            else:
                dir_data["ficha_id"] = ficha.id
                db.session.add(DireccionORM(**dir_data))

        # ---- servicios_publicos: actualizar / crear / eliminar ----
        if getattr(payload, "servicios_publicos", None) is None:
            if getattr(ficha, "servicios_publicos", None):
                db.session.delete(ficha.servicios_publicos)
        else:
            srv_data = payload.servicios_publicos.dict(exclude_unset=True, exclude={"id"})
            if getattr(ficha, "servicios_publicos", None):
                for k, v in srv_data.items():
                    setattr(ficha.servicios_publicos, k, v)
            else:
                srv_data["ficha_id"] = ficha.id
                db.session.add(ServiciosORM(**srv_data))

        # ---- caracteristicas_construccion: reemplazar lista ----
        if getattr(payload, "caracteristicas_construccion", None) is None:
            # si viene explícitamente None, eliminar todas las caracteristicas existentes
            db.session.query(CaracteristicaORM).filter(CaracteristicaORM.ficha_id == ficha.id).delete(synchronize_session=False)
        else:
            # eliminar existentes y crear nuevas
            db.session.query(CaracteristicaORM).filter(CaracteristicaORM.ficha_id == ficha.id).delete(synchronize_session=False)
            for car in payload.caracteristicas_construccion or []:
                car_data = car.dict(exclude_unset=True, exclude={"id"})
                car_data["ficha_id"] = ficha.id
                db.session.add(CaracteristicaORM(**car_data))

        # ---- linderos: reemplazar lista ----
        if getattr(payload, "linderos", None) is None:
            db.session.query(LinderoORM).filter(LinderoORM.ficha_id == ficha.id).delete(synchronize_session=False)
        else:
            db.session.query(LinderoORM).filter(LinderoORM.ficha_id == ficha.id).delete(synchronize_session=False)
            for l in payload.linderos or []:
                l_data = l.dict(exclude_unset=True, exclude={"id"})
                l_data["ficha_id"] = ficha.id
                db.session.add(LinderoORM(**l_data))

        db.session.commit()
        # refrescar para devolver estado actual
        db.session.refresh(ficha)

        response = SchemaGuardarFichaCatastral(
            ficha=FichaSchema.from_orm(ficha),
            propietario=PropietarioSchema.from_orm(ficha.propietario) if getattr(ficha, "propietario", None) else None,
            direccion=DireccionSchema.from_orm(ficha.direccion) if getattr(ficha, "direccion", None) else None,
            servicios_publicos=ServiciosSchema.from_orm(ficha.servicios_publicos) if getattr(ficha, "servicios_publicos", None) else None,
            caracteristicas_construccion=[CaracteristicaSchema.from_orm(c) for c in (ficha.caracteristicas or [])],
            linderos=[LinderoSchema.from_orm(l) for l in (ficha.linderos or [])],
        )

        return response

    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/fichas_completas/{codigo}", status_code=204)
def delete_ficha_completa(codigo: str):
    """
    Elimina (soft-delete) la ficha identificada por codigo_catastral y elimina físicamente las entidades
    relacionadas (propietario, dirección, servicios, caracteristicas y linderos).
    """
    ficha = (
        db.session.query(FichaORM)
        .filter(FichaORM.codigo_catastral == codigo, FichaORM.deleted_at == None)
        .one_or_none()
    )

    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha no encontrada")

    try:
        # Soft-delete en la ficha principal
        ficha.deleted_at = datetime.utcnow()

        # Eliminar filas relacionadas (uso delete físico para liberar consistencia)
        db.session.query(PropietarioORM).filter(PropietarioORM.ficha_id == ficha.id).delete(synchronize_session=False)
        db.session.query(DireccionORM).filter(DireccionORM.ficha_id == ficha.id).delete(synchronize_session=False)
        db.session.query(ServiciosORM).filter(ServiciosORM.ficha_id == ficha.id).delete(synchronize_session=False)
        db.session.query(CaracteristicaORM).filter(CaracteristicaORM.ficha_id == ficha.id).delete(synchronize_session=False)
        db.session.query(LinderoORM).filter(LinderoORM.ficha_id == ficha.id).delete(synchronize_session=False)

        db.session.commit()
        return {}
    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
