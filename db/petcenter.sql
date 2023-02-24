-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: bd_petcenter
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `tb_consulta`
--

DROP TABLE IF EXISTS `tb_consulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_consulta` (
  `cod_consulta` int NOT NULL AUTO_INCREMENT,
  `cod_pet` int DEFAULT NULL,
  `data_consulta` datetime DEFAULT NULL,
  `status_consulta` int DEFAULT NULL,
  `obs_consulta` longtext,
  PRIMARY KEY (`cod_consulta`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_consulta`
--

LOCK TABLES `tb_consulta` WRITE;
/*!40000 ALTER TABLE `tb_consulta` DISABLE KEYS */;
INSERT INTO `tb_consulta` VALUES (1,1,'2023-02-01 11:30:00',1,'1'),(2,2,'2023-02-06 10:50:00',1,'sadasdsd'),(3,1,'2023-02-07 13:50:00',1,'rotina'),(4,2,'2023-02-16 16:00:00',0,'');
/*!40000 ALTER TABLE `tb_consulta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_pet`
--

DROP TABLE IF EXISTS `tb_pet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_pet` (
  `cod_pet` int NOT NULL AUTO_INCREMENT,
  `cod_tipopet` int DEFAULT NULL,
  `nome_pet` varchar(45) DEFAULT NULL,
  `datanasc_pet` date DEFAULT NULL,
  `raca_pet` varchar(45) DEFAULT NULL,
  `status_pet` int DEFAULT NULL,
  `obs_pet` longtext,
  `cod_tutor` int DEFAULT NULL,
  PRIMARY KEY (`cod_pet`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_pet`
--

LOCK TABLES `tb_pet` WRITE;
/*!40000 ALTER TABLE `tb_pet` DISABLE KEYS */;
INSERT INTO `tb_pet` VALUES (1,2,'Lila','2020-12-20','Vira Lata',0,'sadasdasdasd',1),(2,2,'Melvim','2021-03-11','Amarelo',0,'sadsdsad',1);
/*!40000 ALTER TABLE `tb_pet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_tipopet`
--

DROP TABLE IF EXISTS `tb_tipopet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_tipopet` (
  `cod_tipopet` int NOT NULL AUTO_INCREMENT,
  `desc_tipopet` varchar(45) DEFAULT NULL,
  `status_tipopet` int DEFAULT NULL,
  PRIMARY KEY (`cod_tipopet`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_tipopet`
--

LOCK TABLES `tb_tipopet` WRITE;
/*!40000 ALTER TABLE `tb_tipopet` DISABLE KEYS */;
INSERT INTO `tb_tipopet` VALUES (1,'Canino',0),(2,'Felino',0),(3,'Réptil',0),(4,'Pássaro',0),(5,'Anfíbio',0);
/*!40000 ALTER TABLE `tb_tipopet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_tutor`
--

DROP TABLE IF EXISTS `tb_tutor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_tutor` (
  `cod_tutor` int NOT NULL AUTO_INCREMENT,
  `nome_tutor` varchar(45) DEFAULT NULL,
  `end_tutor` varchar(90) DEFAULT NULL,
  `fone_tutor` varchar(45) DEFAULT NULL,
  `status_tutor` int DEFAULT NULL,
  `obs_tutor` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`cod_tutor`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_tutor`
--

LOCK TABLES `tb_tutor` WRITE;
/*!40000 ALTER TABLE `tb_tutor` DISABLE KEYS */;
INSERT INTO `tb_tutor` VALUES (1,'Francieli Silva','Rua 1, Cidade Sul','4199999999',0,'Tutor lila e melvim 1');
/*!40000 ALTER TABLE `tb_tutor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_usertype`
--

DROP TABLE IF EXISTS `tb_usertype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_usertype` (
  `cod_usertype` int DEFAULT NULL,
  `desc_usertype` text,
  `status_usertype` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_usertype`
--

LOCK TABLES `tb_usertype` WRITE;
/*!40000 ALTER TABLE `tb_usertype` DISABLE KEYS */;
INSERT INTO `tb_usertype` VALUES (1,'Administrador',0),(2,'Veterinário',0);
/*!40000 ALTER TABLE `tb_usertype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `cod_user` int DEFAULT NULL,
  `name_user` text,
  `password_user` text,
  `status_user` int DEFAULT NULL,
  `email_user` text,
  `lastlogin_user` text,
  `login_user` text,
  `cod_usertype` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Douglas','$2b$12$ZWrw9mT75lR3EQlpoVhICuyk8z4iB/9N/2nmO.jBL82/ZLGxTIkUu',0,'douglaxz@hotmail.com','','douglas',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-24  8:14:26
