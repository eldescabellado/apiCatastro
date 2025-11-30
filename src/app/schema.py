from typing import List, Optional, Literal
from decimal import Decimal
from datetime import date, datetime
from pydantic import BaseModel, Field, root_validator, validator


# Modelo: fichas_catastrales
class FichaCatastral(BaseModel):
    id: Optional[int] = None
    codigo_catastral: str = Field(..., max_length=50)
    fecha_registro: Optional[date] = Field(default_factory=date.today)
    tipo_predio: Literal['urbano', 'rural']
    area_terreno: Decimal = Field(..., gt=0)
    area_construida: Optional[Decimal] = Field(None, ge=0)
    avaluo_catastral: Optional[Decimal] = Field(None, ge=0)

    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    @root_validator
    def check_area_construida_le_area_terreno(cls, values):
        area_terreno = values.get('area_terreno')
        area_construida = values.get('area_construida')
        if area_construida is not None and area_terreno is not None:
            if area_construida > area_terreno:
                raise ValueError('area_construida no puede ser mayor que area_terreno')
        return values

    class Config:
        orm_mode = True


# Modelo: propietarios
class Propietario(BaseModel):
    id: Optional[int] = None
    ficha_id: Optional[int] = None
    nombre_completo: str = Field(..., max_length=200)
    tipo_documento: Literal['CC', 'NIT', 'CE', 'TI', 'PAS']
    numero_documento: str = Field(..., max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)

    class Config:
        orm_mode = True


# Modelo: direcciones_predios
class DireccionPredio(BaseModel):
    id: Optional[int] = None
    ficha_id: Optional[int] = None
    departamento: str = Field(..., max_length=100)
    municipio: str = Field(..., max_length=100)
    barrio: Optional[str] = Field(None, max_length=100)
    direccion: str = Field(..., max_length=200)
    coordenadas_norte: Optional[Decimal] = None  # latitud en grados decimales
    coordenadas_este: Optional[Decimal] = None   # longitud en grados decimales

    class Config:
        orm_mode = True


# Modelo: servicios_publicos
class ServiciosPublicos(BaseModel):
    id: Optional[int] = None
    ficha_id: Optional[int] = None
    acueducto: bool = False
    alcantarillado: bool = False
    energia: bool = False
    gas: bool = False
    telefono: bool = False
    internet: bool = False
    recoleccion_basuras: bool = False

    class Config:
        orm_mode = True


# Modelo: caracteristicas_construccion
class CaracteristicaConstruccion(BaseModel):
    id: Optional[int] = None
    ficha_id: Optional[int] = None
    tipo_construccion: str = Field(..., max_length=50)
    numero_pisos: int = Field(..., ge=1, le=50)
    estado_conservacion: Literal['excelente', 'bueno', 'regular', 'malo']
    anio_construccion: Optional[int] = Field(None, alias='año_construccion')

    @validator('anio_construccion')
    def validar_anio_construccion(cls, v):
        if v is None:
            return v
        if v < 1800 or v > 2100:
            raise ValueError('año_construccion debe estar entre 1800 y 2100')
        return v

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# Modelo: linderos
class Lindero(BaseModel):
    id: Optional[int] = None
    ficha_id: int
    orientacion: Literal['norte', 'sur', 'este', 'oeste']
    descripcion: str
    longitud: Optional[Decimal] = Field(None, ge=0)

    class Config:
        orm_mode = True

class SchemaGuardarFichaCatastral(BaseModel):
    ficha: FichaCatastral
    propietario: Propietario
    direccion: DireccionPredio
    servicios_publicos: ServiciosPublicos
    caracteristicas_construccion: Optional[CaracteristicaConstruccion] = None
    linderos: Optional[List[Lindero]] = None

    class Config:
        orm_mode = True