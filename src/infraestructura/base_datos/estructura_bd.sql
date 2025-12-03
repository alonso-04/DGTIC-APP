CREATE TABLE tb_departamentos (
	departamento_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	nombre_departamento VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE tb_tipos_servicio (
	tipo_servicio_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	tipo_servicio_prestado VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE tb_servicios (
	servicio_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	departamento_id INTEGER NOT NULL,
	fecha_servicio DATE DEFAULT (CURDATE()),
	falla_presenta VARCHAR(150) NOT NULL,
	tipo_servicio_id INTEGER NOT NULL,
	nombres_tecnicos VARCHAR(250) NOT NULL,
    observaciones_adicionales VARCHAR(255),
	FOREIGN KEY (departamento_id)
		REFERENCES tb_departamentos(departamento_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	FOREIGN KEY (tipo_servicio_id)
		REFERENCES tb_tipos_servicio(tipo_servicio_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
);

CREATE TABLE tb_roles (
	rol_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	tipo_rol VARCHAR(15) NOT NULL
);

CREATE TABLE tb_usuarios(
	usuario_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	rol_id INTEGER NOT NULL,
	nombre_usuario VARCHAR(12) UNIQUE NOT NULL,
	clave_usuario TEXT,
	FOREIGN KEY (rol_id)
		REFERENCES tb_roles(rol_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
);


CREATE VIEW vw_servicios_prestados as
	SELECT
		servicios.servicio_id,
		departamentos.departamento_id,
		tipos_servicio.tipo_servicio_id,
		departamentos.nombre_departamento,
		servicios.fecha_servicio,
		servicios.falla_presenta,
		tipos_servicio.tipo_servicio_prestado,
		servicios.nombres_tecnicos,
        servicios.observaciones_adicionales
	FROM tb_servicios AS servicios
	INNER JOIN tb_departamentos AS departamentos ON servicios.departamento_id = departamentos.departamento_id
	INNER JOIN tb_tipos_servicio AS tipos_servicio ON servicios.tipo_servicio_id = tipos_servicio.tipo_servicio_id;


INSERT INTO tb_roles (tipo_rol)
VALUES ('ADMINISTRADOR');

INSERT INTO tb_roles(tipo_rol)
VALUES ('ESTANDAR');