-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: nya_secondary
-- ------------------------------------------------------
-- Server version	8.0.13

 SET NAMES utf8 ;

--
-- Table structure for table `qna`
--

DROP TABLE IF EXISTS `qna`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `qna` (
  `server_id` bigint(18) NOT NULL,
  `stream_id` int(10) NOT NULL,
  `question_id` bigint(18) NOT NULL,
  `timestamp` char(8) NOT NULL,
  PRIMARY KEY (`server_id`,`stream_id`),
  KEY `qna_stream_id_idx` (`stream_id`),
  CONSTRAINT `qna_server_id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`),
  CONSTRAINT `qna_stream_id` FOREIGN KEY (`stream_id`) REFERENCES `stream_schedule` (`stream_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `selfassign_role`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `selfassign_role` (
  `server_id` bigint(18) NOT NULL,
  `role_id` bigint(18) NOT NULL,
  `channel_id` bigint(18) DEFAULT NULL,
  `description` char(248) NOT NULL,
  PRIMARY KEY (`server_id`,`role_id`),
  KEY `id_idx` (`server_id`),
  CONSTRAINT `id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `stream_schedule`
--

DROP TABLE IF EXISTS `stream_schedule`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `stream_schedule` (
  `stream_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` bigint(18) NOT NULL,
  `stream_title` varchar(120) NOT NULL,
  `stream_date` datetime NOT NULL,
  PRIMARY KEY (`stream_id`),
  UNIQUE KEY `id_UNIQUE` (`stream_id`),
  KEY `id_idx` (`server_id`),
  CONSTRAINT `server_stream_id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `tags` (
  `server_id` bigint(18) NOT NULL,
  `tag_owner_id` bigint(18) NOT NULL,
  `tag_name` varchar(48) NOT NULL,
  `tag_description` text NOT NULL,
  `tag_created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`server_id`,`tag_name`),
  KEY `tag_server_id_idx` (`server_id`),
  CONSTRAINT `tag_server_id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table will hold replies for preset tag words. Use in discord will be `<server_prefix>tag <tag_name>` and will return `tag_description`';

--
-- Table structure for table `user_profiles`
--

DROP TABLE IF EXISTS `user_profiles`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `user_profiles` (
  `user_id` bigint(18) NOT NULL,
  `timezone` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `giveaway`
--

DROP TABLE IF EXISTS `giveaway`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `giveaway` (
  `giveaway_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` bigint(18) NOT NULL,
  `giveaway_name` varchar(100) NOT NULL,
  PRIMARY KEY (`giveaway_id`),
  UNIQUE KEY `giveaway_id_UNIQUE` (`giveaway_id`),
  KEY `giveaway_server_id_idx` (`server_id`),
  CONSTRAINT `giveaway_server_id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `giveaway_roles`
--

DROP TABLE IF EXISTS `giveaway_roles`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `giveaway_roles` (
  `giveaway_id` int(11) NOT NULL,
  `role_id` bigint(18) NOT NULL,
  KEY `giveaway_roles_id_idx` (`giveaway_id`),
  CONSTRAINT `giveaway_roles_id` FOREIGN KEY (`giveaway_id`) REFERENCES `giveaway` (`giveaway_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump completed on 2019-03-12 21:10:25

