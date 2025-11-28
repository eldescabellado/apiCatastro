-- ============================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Fichas Catastrales Urbanas
-- PostgreSQL 12+
-- ============================================================

-- Crear base de datos (ejecutar como superusuario)
-- CREATE DATABASE catastro_db;
-- \c catastro_db;

-- ============================================================
-- TABLA PRINCIPAL: FICHAS CATASTRALES
-- ============================================================

CREATE TABLE IF NOT EXISTS fichas_catastrales (
    id SERIAL PRIMARY KEY,
    codigo_catastral VARCHAR(50) UNIQUE NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    tipo_predio VARCHAR(20) NOT NULL CHECK (tipo_predio IN ('urbano', 'rural')),
    area_terreno NUMERIC(10, 2) NOT NULL CHECK (area_terreno > 0),
    area_construida NUMERIC(10, 2) CHECK (area_construida >= 0),
    avaluo_catastral NUMERIC(15, 2) CHECK (avaluo_catastral >= 0),
    
    -- Auditoría
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    -- Índices
    CONSTRAINT chk_area_construida CHECK (area_construida IS NULL OR area_construida <= area_terreno)
);

-- Índices para optimización de consultas
CREATE INDEX idx_fichas_codigo ON fichas_catastrales(codigo_catastral);
CREATE INDEX idx_fichas_tipo ON fichas_catastrales(tipo_predio);
CREATE INDEX idx_fichas_deleted ON fichas_catastrales(deleted_at);

-- Comentarios
COMMENT ON TABLE fichas_catastrales IS 'Tabla principal de fichas catastrales';
COMMENT ON COLUMN fichas_catastrales.codigo_catastral IS 'Código único de identificación catastral';
COMMENT ON COLUMN fichas_catastrales.tipo_predio IS 'Tipo de predio: urbano o rural';
COMMENT ON COLUMN fichas_catastrales.deleted_at IS 'Fecha de eliminación lógica (soft delete)';


-- ============================================================
-- TABLA: PROPIETARIOS
-- ============================================================

CREATE TABLE IF NOT EXISTS propietarios (
    id SERIAL PRIMARY KEY,
    ficha_id INTEGER NOT NULL UNIQUE,
    nombre_completo VARCHAR(200) NOT NULL,
    tipo_documento VARCHAR(10) NOT NULL CHECK (tipo_documento IN ('CC', 'NIT', 'CE', 'TI', 'PAS')),
    numero_documento VARCHAR(20) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    
    -- Clave foránea
    CONSTRAINT fk_propietario_ficha FOREIGN KEY (ficha_id) 
        REFERENCES fichas_catastrales(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_propietarios_documento ON propietarios(numero_documento);
CREATE INDEX idx_propietarios_ficha ON propietarios(ficha_id);

-- Comentarios
COMMENT ON TABLE propietarios IS 'Información de propietarios o administradores de predios';
COMMENT ON COLUMN propietarios.tipo_documento IS 'CC=Cédula, NIT=NIT, CE=Cédula Extranjería, TI=Tarjeta Identidad, PAS=Pasaporte';


-- ============================================================
-- TABLA: DIRECCIONES DE PREDIOS
-- ============================================================

CREATE TABLE IF NOT EXISTS direcciones_predios (
    id SERIAL PRIMARY KEY,
    ficha_id INTEGER NOT NULL UNIQUE,
    departamento VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    barrio VARCHAR(100),
    direccion VARCHAR(200) NOT NULL,
    coordenadas_norte NUMERIC(12, 6),
    coordenadas_este NUMERIC(12, 6),
    
    -- Clave foránea
    CONSTRAINT fk_direccion_ficha FOREIGN KEY (ficha_id) 
        REFERENCES fichas_catastrales(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_direcciones_municipio ON direcciones_predios(municipio);
CREATE INDEX idx_direcciones_ficha ON direcciones_predios(ficha_id);

-- Comentarios
COMMENT ON TABLE direcciones_predios IS 'Ubicación geográfica de los predios';
COMMENT ON COLUMN direcciones_predios.coordenadas_norte IS 'Latitud en grados decimales';
COMMENT ON COLUMN direcciones_predios.coordenadas_este IS 'Longitud en grados decimales';


-- ============================================================
-- TABLA: SERVICIOS PÚBLICOS
-- ============================================================

CREATE TABLE IF NOT EXISTS servicios_publicos (
    id SERIAL PRIMARY KEY,
    ficha_id INTEGER NOT NULL UNIQUE,
    acueducto BOOLEAN NOT NULL DEFAULT FALSE,
    alcantarillado BOOLEAN NOT NULL DEFAULT FALSE,
    energia BOOLEAN NOT NULL DEFAULT FALSE,
    gas BOOLEAN NOT NULL DEFAULT FALSE,
    telefono BOOLEAN NOT NULL DEFAULT FALSE,
    internet BOOLEAN NOT NULL DEFAULT FALSE,
    recoleccion_basuras BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Clave foránea
    CONSTRAINT fk_servicios_ficha FOREIGN KEY (ficha_id) 
        REFERENCES fichas_catastrales(id) ON DELETE CASCADE
);

-- Índice
CREATE INDEX idx_servicios_ficha ON servicios_publicos(ficha_id);

-- Comentarios
COMMENT ON TABLE servicios_publicos IS 'Servicios públicos disponibles en el predio';


-- ============================================================
-- TABLA: CARACTERÍSTICAS DE CONSTRUCCIÓN
-- ============================================================

CREATE TABLE IF NOT EXISTS caracteristicas_construccion (
    id SERIAL PRIMARY KEY,
    ficha_id INTEGER NOT NULL,
    tipo_construccion VARCHAR(50) NOT NULL,
    numero_pisos INTEGER NOT NULL CHECK (numero_pisos > 0 AND numero_pisos <= 50),
    estado_conservacion VARCHAR(20) NOT NULL CHECK (estado_conservacion IN ('excelente', 'bueno', 'regular', 'malo')),
    año_construccion INTEGER CHECK (año_construccion >= 1800 AND año_construccion <= 2100),
    
    -- Clave foránea
    CONSTRAINT fk_caracteristicas_ficha FOREIGN KEY (ficha_id) 
        REFERENCES fichas_catastrales(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_caracteristicas_ficha ON caracteristicas_construccion(ficha_id);
CREATE INDEX idx_caracteristicas_tipo ON caracteristicas_construccion(tipo_construccion);

-- Comentarios
COMMENT ON TABLE caracteristicas_construccion IS 'Características de las construcciones en el predio';
COMMENT ON COLUMN caracteristicas_construccion.tipo_construccion IS 'Ej: casa, apartamento, bodega, local comercial';


-- ============================================================
-- TABLA: LINDEROS
-- ============================================================

CREATE TABLE IF NOT EXISTS linderos (
    id SERIAL PRIMARY KEY,
    ficha_id INTEGER NOT NULL,
    orientacion VARCHAR(10) NOT NULL CHECK (orientacion IN ('norte', 'sur', 'este', 'oeste')),
    descripcion TEXT NOT NULL,
    longitud NUMERIC(10, 2) CHECK (longitud >= 0),
    
    -- Clave foránea
    CONSTRAINT fk_linderos_ficha FOREIGN KEY (ficha_id) 
        REFERENCES fichas_catastrales(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_linderos_ficha ON linderos(ficha_id);
CREATE INDEX idx_linderos_orientacion ON linderos(orientacion);

-- Comentarios
COMMENT ON TABLE linderos IS 'Linderos y colindancias del predio';
COMMENT ON COLUMN linderos.longitud IS 'Longitud del lindero en metros';


-- ============================================================
-- FUNCIÓN: ACTUALIZAR TIMESTAMP
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar automáticamente updated_at
CREATE TRIGGER update_fichas_updated_at 
    BEFORE UPDATE ON fichas_catastrales
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================
-- DATOS DE EJEMPLO (OPCIONAL)
-- ============================================================

-- Insertar una ficha de ejemplo
-- INSERT INTO fichas_catastrales (codigo_catastral, tipo_predio, area_terreno, area_construida, avaluo_catastral)
-- VALUES ('001-2023-URB-001', 'urbano', 250.50, 180.00, 150000000.00);

-- INSERT INTO propietarios (ficha_id, nombre_completo, tipo_documento, numero_documento, telefono, email)
-- VALUES (1, 'Juan Pérez García', 'CC', '1234567890', '3001234567', 'juan.perez@example.com');

-- INSERT INTO direcciones_predios (ficha_id, departamento, municipio, barrio, direccion)
-- VALUES (1, 'Cundinamarca', 'Bogotá', 'Chapinero', 'Calle 60 # 10-20');

-- INSERT INTO servicios_publicos (ficha_id, acueducto, alcantarillado, energia, gas, internet, recoleccion_basuras)
-- VALUES (1, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);


-- ============================================================
-- CONSULTAS ÚTILES
-- ============================================================

-- Ver todas las fichas con sus propietarios
-- SELECT f.codigo_catastral, f.tipo_predio, p.nombre_completo, d.municipio
-- FROM fichas_catastrales f
-- LEFT JOIN propietarios p ON p.ficha_id = f.id
-- LEFT JOIN direcciones_predios d ON d.ficha_id = f.id
-- WHERE f.deleted_at IS NULL;

-- Ver servicios disponibles por ficha
-- SELECT f.codigo_catastral, s.*
-- FROM fichas_catastrales f
-- JOIN servicios_publicos s ON s.ficha_id = f.id
-- WHERE f.deleted_at IS NULL;

-- Contar fichas por municipio
-- SELECT d.municipio, COUNT(*) as total_fichas
-- FROM direcciones_predios d
-- JOIN fichas_catastrales f ON f.id = d.ficha_id
-- WHERE f.deleted_at IS NULL
-- GROUP BY d.municipio
-- ORDER BY total_fichas DESC;


-- ============================================================
-- SCRIPT COMPLETADO
-- ============================================================

-- Verificar tablas creadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
