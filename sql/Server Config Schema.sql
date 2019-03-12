-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: nya_secondary
-- ------------------------------------------------------
-- Server version	8.0.13

SET NAMES utf8 ;

--
-- Table structure for table `server_base_config`
--

DROP TABLE IF EXISTS `server_base_config`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `server_base_config` (
  `server_id` bigint(18) NOT NULL,
  `prefix` char(5) NOT NULL,
  `welcome_message` text,
  PRIMARY KEY (`server_id`),
  UNIQUE KEY `id_UNIQUE` (`server_id`),
  CONSTRAINT `config_server_id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `server_cogs_disabled`
--

DROP TABLE IF EXISTS `server_cogs_disabled`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `server_cogs_disabled` (
  `server_id` bigint(18) NOT NULL,
  `cog_name` char(24) NOT NULL,
  PRIMARY KEY (`cog_name`,`server_id`),
  KEY `cogs_disabled_server_id_idx` (`server_id`),
  CONSTRAINT `cogs_disabled_server_id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
--
-- Table structure for table `server_event_logs`
--

DROP TABLE IF EXISTS `server_event_logs`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `server_event_logs` (
  `server_id` bigint(18) NOT NULL,
  `user_id` bigint(18) NOT NULL,
  `date_utc` datetime NOT NULL,
  `event_type` varchar(15) NOT NULL,
  PRIMARY KEY (`server_id`,`user_id`),
  CONSTRAINT `event_server_id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `server_list`
--

DROP TABLE IF EXISTS `server_list`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `server_list` (
  `server_id` bigint(18) NOT NULL,
  `name` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `members` int(4) GENERATED ALWAYS AS ((`human_members` + `bot_members`)) STORED,
  `human_members` int(4) NOT NULL,
  `bot_members` int(4) NOT NULL,
  PRIMARY KEY (`server_id`),
  UNIQUE KEY `server_id_UNIQUE` (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `server_user_stats`
--

DROP TABLE IF EXISTS `server_user_stats`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `server_user_stats` (
  `server_id` bigint(18) NOT NULL,
  `channel_id` bigint(18) NOT NULL,
  `user_id` bigint(18) NOT NULL,
  `msg_count` bigint(20) NOT NULL,
  PRIMARY KEY (`server_id`,`channel_id`,`user_id`),
  KEY `stats_server_id_idx` (`server_id`),
  CONSTRAINT `stats_server_id` FOREIGN KEY (`server_id`) REFERENCES `server_list` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dump completed on 2019-03-08 19:52:48
