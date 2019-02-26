CREATE TABLE tb_userdata (
	id_userdata INT NOT NULL DEFAULT unique_rowid(),
	sso_id STRING NOT NULL,
	first_name STRING NULL,
	last_name STRING NULL,
	location STRING NULL,
	email STRING NOT NULL,
	picture STRING NULL,
	CONSTRAINT tb_userdata_pk PRIMARY KEY (id_userdata DESC),
	UNIQUE INDEX tb_userdata_un (email DESC),
	UNIQUE INDEX tb_userdata_sso (sso_id DESC),
	FAMILY "primary" (id_userdata, sso_id, first_name, last_name, location, email, picture)
);

CREATE TABLE tb_user (
	id_user INT NOT NULL DEFAULT unique_rowid(),
	id_userdata INT NOT NULL,
	username VARCHAR NOT NULL,
	password VARCHAR NOT NULL,
	CONSTRAINT tb_user_pk PRIMARY KEY (id_user ASC),
	UNIQUE INDEX tb_user_un (id_userdata ASC),
	FAMILY "primary" (id_user, id_userdata, username, password)
);

CREATE VIEW v_widget (id_widget, id_channels, nm_widget, nm_channels, channels_key, id_userboard, id_userdata, id_board, email) AS SELECT a1.id_widget, a1.id_channels, a1.nm_widget, a2.nm_channels, a2.channels_key, a3.id_userboard, a3.id_userdata, a3.id_board, a4.email FROM iot_adrini.public.tb_widget AS a1 JOIN iot_adrini.public.tb_channels AS a2 ON a1.id_channels = a2.id_channels JOIN iot_adrini.public.tb_userboard AS a3 ON a2.id_userboard = a3.id_userboard JOIN iot_adrini.public.tb_userdata AS a4 ON a3.id_userdata = a4.id_userdata;

INSERT INTO tb_userdata (id_userdata, sso_id, first_name, last_name, location, email, picture) VALUES
	(429520543461146625, '111307412920325935077', 'meong', 'bego', '', 'meongbego@gmail.com', 'https://lh4.googleusercontent.com/-egNEmgFlfvs/AAAAAAAAAAI/AAAAAAAADhc/lu-iH-962kk/photo.jpg');

ALTER TABLE tb_user ADD CONSTRAINT tb_user_tb_userdata_fk FOREIGN KEY (id_userdata) REFERENCES tb_userdata (id_userdata) ON DELETE CASCADE ON UPDATE CASCADE;

-- Validate foreign key constraints. These can fail if there was unvalidated data during the dump.
ALTER TABLE tb_user VALIDATE CONSTRAINT tb_user_tb_userdata_fk;
