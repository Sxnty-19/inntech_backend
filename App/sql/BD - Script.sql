-- ========================================================
-- INNTECH - BASE DE DATOS
-- Versión: Parcial - COM11_2025-3 (Corte N°1)
-- ========================================================

-- 1. Tabla: rol
CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Tabla: usuario
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_rol INT NOT NULL,
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

-- 3. Tabla: modulo
CREATE TABLE modulo (
    id_modulo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ruta VARCHAR(255) UNIQUE,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. Tabla: modulo_rol
CREATE TABLE modulo_rol (
    id_mxr INT AUTO_INCREMENT PRIMARY KEY,
    id_modulo INT NOT NULL,
    id_rol INT NOT NULL,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_modulo) REFERENCES modulo(id_modulo),
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

-- 5. Tabla: atributo
CREATE TABLE atributo (
    id_atributo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 6. Tabla: usuario_atributo
CREATE TABLE usuario_atributo (
    id_uxa INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_atributo INT NOT NULL,
    valor VARCHAR(255),
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_atributo) REFERENCES atributo(id_atributo)
);

-- 7. Tabla: tipo_documento
CREATE TABLE tipo_documento (
    id_tdocumento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 8. Tabla: documento
CREATE TABLE documento (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,
    id_tdocumento INT NOT NULL,
    id_usuario INT NOT NULL,
    numero_documento VARCHAR(50) UNIQUE NOT NULL,
    lugar_expedicion VARCHAR(150),
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tdocumento) REFERENCES tipo_documento(id_tdocumento),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- 9. Tabla: tipo_habitacion
CREATE TABLE tipo_habitacion (
    id_thabitacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    capacidad_max INT NOT NULL,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 10. Tabla: habitacion
CREATE TABLE habitacion (
    id_habitacion INT AUTO_INCREMENT PRIMARY KEY,
    id_thabitacion INT NOT NULL,
    numero VARCHAR(10) UNIQUE NOT NULL,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    limpieza TINYINT(1) DEFAULT 1,
    FOREIGN KEY (id_thabitacion) REFERENCES tipo_habitacion(id_thabitacion)
);

-- 11. Tabla: reserva
CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    date_start DATETIME NOT NULL,
    date_end DATETIME NOT NULL,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- 12. Tabla: reserva_habitacion
CREATE TABLE reserva_habitacion (
    id_rxh INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_habitacion INT NOT NULL,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva),
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id_habitacion)
);

-- 13. Tabla: usuario_habitacion
CREATE TABLE usuario_habitacion (
    id_uxh INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_habitacion INT NOT NULL,
    id_reserva INT NOT NULL,
    date_check_in DATETIME,
    date_check_out DATETIME,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id_habitacion),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- 14. Tabla: notificacion
CREATE TABLE notificacion (
    id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_habitacion INT NOT NULL,
    descripcion TEXT NOT NULL,
    estado TINYINT(1) DEFAULT 1,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id_habitacion)
);