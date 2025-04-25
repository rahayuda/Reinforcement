-- Membuat database db_a dan db_b
CREATE DATABASE db_a;
CREATE DATABASE db_b;

-- Menggunakan db_a
USE db_a;

-- Membuat tabel data_storage di db_a
CREATE TABLE `data_storage` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,  -- Menambahkan AUTO_INCREMENT untuk id
  `page` VARCHAR(100) DEFAULT NULL,
  `view` INT(11) DEFAULT 0,
  `size` INT(11) DEFAULT 0,
  PRIMARY KEY (`id`)  -- Menambahkan PRIMARY KEY pada kolom id
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Menggunakan db_b
USE db_b;

-- Membuat tabel data_storage di db_b
CREATE TABLE `data_storage` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,  -- Menambahkan AUTO_INCREMENT untuk id
  `page` VARCHAR(100) DEFAULT NULL,
  `view` INT(11) DEFAULT 0,
  `size` INT(11) DEFAULT 0,
  PRIMARY KEY (`id`)  -- Menambahkan PRIMARY KEY pada kolom id
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
