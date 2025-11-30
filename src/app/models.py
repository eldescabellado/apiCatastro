from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, Numeric, Date, DateTime, Boolean, Text,
    ForeignKey, CheckConstraint, Index, func
)
from sqlalchemy.orm import relationship

Base = declarative_base()


class FichaCatastral(Base):
    __tablename__ = "fichas_catastrales"
    __table_args__ = (
        CheckConstraint("tipo_predio IN ('urbano','rural')", name="chk_tipo_predio"),
        CheckConstraint("area_terreno > 0", name="chk_area_terreno_pos"),
        CheckConstraint("area_construida >= 0", name="chk_area_construida_no_neg"),
        CheckConstraint("avaluo_catastral >= 0", name="chk_avaluo_no_neg"),
        CheckConstraint("area_construida IS NULL OR area_construida <= area_terreno", name="chk_area_construida"),
        Index("idx_fichas_codigo", "codigo_catastral"),
        Index("idx_fichas_tipo", "tipo_predio"),
        Index("idx_fichas_deleted", "deleted_at"),
    )

    id = Column(Integer, primary_key=True)
    codigo_catastral = Column(String(50), unique=True, nullable=False)
    fecha_registro = Column(Date, nullable=False, server_default=func.current_date())
    tipo_predio = Column(String(20), nullable=False)
    area_terreno = Column(Numeric(10, 2), nullable=False)
    area_construida = Column(Numeric(10, 2), nullable=True)
    avaluo_catastral = Column(Numeric(15, 2), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Relaciones one-to-one
    propietario = relationship("Propietario", uselist=False, back_populates="ficha", cascade="all, delete-orphan")
    direccion = relationship("DireccionPredio", uselist=False, back_populates="ficha", cascade="all, delete-orphan")
    servicios_publicos = relationship("ServiciosPublicos", uselist=False, back_populates="ficha", cascade="all, delete-orphan")

    # Relaciones one-to-many
    caracteristicas = relationship("CaracteristicaConstruccion", back_populates="ficha", cascade="all, delete-orphan")
    linderos = relationship("Lindero", back_populates="ficha", cascade="all, delete-orphan")


class Propietario(Base):
    __tablename__ = "propietarios"
    __table_args__ = (
        CheckConstraint("tipo_documento IN ('CC','NIT','CE','TI','PAS')", name="chk_tipo_documento"),
        Index("idx_propietarios_documento", "numero_documento"),
        Index("idx_propietarios_ficha", "ficha_id"),
    )

    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_catastrales.id", ondelete="CASCADE"), nullable=False, unique=True)
    nombre_completo = Column(String(200), nullable=False)
    tipo_documento = Column(String(10), nullable=False)
    numero_documento = Column(String(20), nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    ficha = relationship("FichaCatastral", back_populates="propietario")


class DireccionPredio(Base):
    __tablename__ = "direcciones_predios"
    __table_args__ = (
        Index("idx_direcciones_municipio", "municipio"),
        Index("idx_direcciones_ficha", "ficha_id"),
    )

    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_catastrales.id", ondelete="CASCADE"), nullable=False, unique=True)
    departamento = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    barrio = Column(String(100), nullable=True)
    direccion = Column(String(200), nullable=False)
    coordenadas_norte = Column(Numeric(12, 6), nullable=True)
    coordenadas_este = Column(Numeric(12, 6), nullable=True)

    ficha = relationship("FichaCatastral", back_populates="direccion")


class ServiciosPublicos(Base):
    __tablename__ = "servicios_publicos"
    __table_args__ = (
        Index("idx_servicios_ficha", "ficha_id"),
    )

    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_catastrales.id", ondelete="CASCADE"), nullable=False, unique=True)
    acueducto = Column(Boolean, nullable=False, server_default="false")
    alcantarillado = Column(Boolean, nullable=False, server_default="false")
    energia = Column(Boolean, nullable=False, server_default="false")
    gas = Column(Boolean, nullable=False, server_default="false")
    telefono = Column(Boolean, nullable=False, server_default="false")
    internet = Column(Boolean, nullable=False, server_default="false")
    recoleccion_basuras = Column(Boolean, nullable=False, server_default="false")

    ficha = relationship("FichaCatastral", back_populates="servicios_publicos")


class CaracteristicaConstruccion(Base):
    __tablename__ = "caracteristicas_construccion"
    __table_args__ = (
        CheckConstraint("numero_pisos > 0 AND numero_pisos <= 50", name="chk_numero_pisos"),
        CheckConstraint("estado_conservacion IN ('excelente','bueno','regular','malo')", name="chk_estado_conservacion"),
        CheckConstraint("año_construccion IS NULL OR (año_construccion >= 1800 AND año_construccion <= 2100)", name="chk_ano_construccion"),
        Index("idx_caracteristicas_ficha", "ficha_id"),
        Index("idx_caracteristicas_tipo", "tipo_construccion"),
    )

    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_catastrales.id", ondelete="CASCADE"), nullable=False)
    tipo_construccion = Column(String(50), nullable=False)
    numero_pisos = Column(Integer, nullable=False)
    estado_conservacion = Column(String(20), nullable=False)
    # La columna en DB se llama 'año_construccion' (con ñ); usamos nombre de atributo 'ano_construccion'
    ano_construccion = Column("año_construccion", Integer, nullable=True)

    ficha = relationship("FichaCatastral", back_populates="caracteristicas")


class Lindero(Base):
    __tablename__ = "linderos"
    __table_args__ = (
        CheckConstraint("orientacion IN ('norte','sur','este','oeste')", name="chk_orientacion"),
        CheckConstraint("longitud >= 0", name="chk_longitud_no_neg"),
        Index("idx_linderos_ficha", "ficha_id"),
        Index("idx_linderos_orientacion", "orientacion"),
    )

    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_catastrales.id", ondelete="CASCADE"), nullable=False)
    orientacion = Column(String(10), nullable=False)
    descripcion = Column(Text, nullable=False)
    longitud = Column(Numeric(10, 2), nullable=True)

    ficha = relationship("FichaCatastral", back_populates="linderos")
