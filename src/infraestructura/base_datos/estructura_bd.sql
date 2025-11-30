-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: informatica
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_departamentos`
--

DROP TABLE IF EXISTS `tb_departamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_departamentos` (
  `departamento_id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_departamento` varchar(120) NOT NULL,
  PRIMARY KEY (`departamento_id`),
  UNIQUE KEY `nombre_departamento` (`nombre_departamento`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_roles`
--

DROP TABLE IF EXISTS `tb_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_roles` (
  `rol_id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_rol` varchar(15) NOT NULL,
  PRIMARY KEY (`rol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_servicios`
--

DROP TABLE IF EXISTS `tb_servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_servicios` (
  `servicio_id` int(11) NOT NULL AUTO_INCREMENT,
  `departamento_id` int(11) NOT NULL,
  `fecha_servicio` date DEFAULT curdate(),
  `falla_presenta` varchar(150) NOT NULL,
  `tipo_servicio_id` int(11) NOT NULL,
  `nombres_tecnicos` varchar(250) NOT NULL,
  `observaciones_adicionales` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`servicio_id`),
  KEY `departamento_id` (`departamento_id`),
  KEY `tipo_servicio_id` (`tipo_servicio_id`),
  CONSTRAINT `tb_servicios_ibfk_1` FOREIGN KEY (`departamento_id`) REFERENCES `tb_departamentos` (`departamento_id`) ON UPDATE CASCADE,
  CONSTRAINT `tb_servicios_ibfk_2` FOREIGN KEY (`tipo_servicio_id`) REFERENCES `tb_tipos_servicio` (`tipo_servicio_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_tipos_servicio`
--

DROP TABLE IF EXISTS `tb_tipos_servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_tipos_servicio` (
  `tipo_servicio_id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_servicio_prestado` varchar(120) NOT NULL,
  PRIMARY KEY (`tipo_servicio_id`),
  UNIQUE KEY `tipo_servicio_prestado` (`tipo_servicio_prestado`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_usuarios`
--

DROP TABLE IF EXISTS `tb_usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_usuarios` (
  `usuario_id` int(11) NOT NULL AUTO_INCREMENT,
  `rol_id` int(11) NOT NULL,
  `nombre_usuario` varchar(12) NOT NULL,
  `clave_usuario` text DEFAULT NULL,
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `tb_usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `tb_roles` (`rol_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `vw_servicios_prestados`
--

DROP TABLE IF EXISTS `vw_servicios_prestados`;
/*!50001 DROP VIEW IF EXISTS `vw_servicios_prestados`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_servicios_prestados` AS SELECT 
 1 AS `servicio_id`,
 1 AS `departamento_id`,
 1 AS `tipo_servicio_id`,
 1 AS `nombre_departamento`,
 1 AS `fecha_servicio`,
 1 AS `falla_presenta`,
 1 AS `tipo_servicio_prestado`,
 1 AS `nombres_tecnicos`,
 1 AS `observaciones_adicionales`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vw_servicios_prestados`
--

/*!50001 DROP VIEW IF EXISTS `vw_servicios_prestados`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`dgtic`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_servicios_prestados` AS select `servicios`.`servicio_id` AS `servicio_id`,`departamentos`.`departamento_id` AS `departamento_id`,`tipos_servicio`.`tipo_servicio_id` AS `tipo_servicio_id`,`departamentos`.`nombre_departamento` AS `nombre_departamento`,`servicios`.`fecha_servicio` AS `fecha_servicio`,`servicios`.`falla_presenta` AS `falla_presenta`,`tipos_servicio`.`tipo_servicio_prestado` AS `tipo_servicio_prestado`,`servicios`.`nombres_tecnicos` AS `nombres_tecnicos`,`servicios`.`observaciones_adicionales` AS `observaciones_adicionales` from ((`tb_servicios` `servicios` join `tb_departamentos` `departamentos` on(`servicios`.`departamento_id` = `departamentos`.`departamento_id`)) join `tb_tipos_servicio` `tipos_servicio` on(`servicios`.`tipo_servicio_id` = `tipos_servicio`.`tipo_servicio_id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-30 14:04:55
