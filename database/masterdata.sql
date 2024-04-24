-- phpMyAdmin SQL Dump
-- version 5.0.4deb2+deb11u1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 23-03-2024 a las 14:56:48
-- Versión del servidor: 10.5.19-MariaDB-0+deb11u2
-- Versión de PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `DomoServer`
--

CREATE DATABASE DomoServer;

USE DomoServer;
--
-- Estructura de tabla para la tabla `home_bedroom`
--

CREATE TABLE `home_bedroom` (
  `ID` int(11) NOT NULL,
  `MEANING` varchar(128) NOT NULL,
  `VALUE` varchar(128) NOT NULL,
  `UNIT` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `home_bedroom`
--

INSERT INTO `home_bedroom` (`ID`, `MEANING`, `VALUE`, `UNIT`) VALUES
(1, 'R', 'OFF', 'NULL'),
(2, 'T', '28.5', 'ºC'),
(3, 'P', 'OFF', 'NULL'),
(4, 'H', '49.0', '%'),
(5, 'L', 'ON', 'OFF'),
(6, 'C', 'OFF', 'NULL\r\n');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `home_external`
--

CREATE TABLE `home_external` (
  `ID` int(11) NOT NULL,
  `MEANING` varchar(128) NOT NULL,
  `VALUE` varchar(32) NOT NULL,
  `UNIT` varchar(32) NOT NULL,
  `DATETIME` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `home_external`
--

INSERT INTO `home_external` (`ID`, `MEANING`, `VALUE`, `UNIT`, `DATETIME`) VALUES
(1, 'Temperature', '23', 'ºC', '2024-03-23 14:44:40'),
(2, 'Sunset', '19:37', 'Hour', '2024-03-22 18:54:01'),
(3, 'Sunrise', '7:23', 'Hour', '2024-03-22 18:54:04');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `home_general`
--

CREATE TABLE `home_general` (
  `ID` int(11) NOT NULL,
  `MEANING` varchar(128) NOT NULL,
  `VA` varchar(32) NOT NULL,
  `UNIT` varchar(32) NOT NULL,
  `DATETIME` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `home_living_room`
--

CREATE TABLE `home_living_room` (
  `ID` int(11) NOT NULL,
  `MEANING` varchar(128) NOT NULL,
  `VALUE` varchar(128) NOT NULL,
  `UNIT` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `home_living_room`
--

INSERT INTO `home_living_room` (`ID`, `MEANING`, `VALUE`, `UNIT`) VALUES
(2, 'T', '26.0', 'ºC'),
(4, 'H', '49.0', '%');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mqtt_historic`
--

CREATE TABLE `mqtt_historic` (
  `ID` int(11) NOT NULL,
  `DATETIME` varchar(20) NOT NULL,
  `TOPIC` varchar(128) NOT NULL,
  `VALUE` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mqtt_historic`
--

INSERT INTO `mqtt_historic` (`ID`, `DATETIME`, `TOPIC`, `VALUE`) VALUES
(1, '2024-03-23 14:52:01', 'home/living_room/T', '26.0'),
(2, '2024-03-23 14:52:01', 'home/living_room/H', '49.0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programed_commands`
--

CREATE TABLE `programed_commands` (
  `ID` int(11) NOT NULL,
  `COMMAND` varchar(256) NOT NULL,
  `DATETIME` varchar(20) NOT NULL,
  `WEEKDAY` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `programed_commands`
--

INSERT INTO `programed_commands` (`ID`, `COMMAND`, `DATETIME`, `WEEKDAY`) VALUES
(1, 'python mqtt_send_to_topic_and_ddbb.py home/bedroom/R OFF', '****-**-** 09:00:00', 127),
(2, 'python mqtt_send_to_topic_and_ddbb.py home/bedroom/R OFF', '****-**-** 14:00:00', 127),
(3, 'python mqtt_send_to_topic_and_ddbb.py home/bedroom/R OFF', '****-**-** 18:00:00', 127),
(4, 'python mqtt_send_to_topic_and_ddbb.py home/bedroom/R OFF', '****-**-** 01:00:00', 127),
(10, 'python mqtt_send_to_topic_and_ddbb.py home/bedroom/R ON', '****-**-** 08:00:00', 0),
(11, 'python mqtt_send_to_topic_and_ddbb.py home/bedroom/R ON', '****-**-** 07:00:00', 0),
(20, 'python mqtt_send_to_topic_and_ddbb.py home/bedroom/L OFF', '****-**-** 09:00:00', 31),
(21, 'python mqtt_send_to_topic_and_ddbb.py home/bedroom/L OFF', '****-**-** 00:00:00', 31),
(100, 'python send_email.py \"Domotic Raspbian Service wish you a good day\" \"/var/www/html/Domo/files/test_file.txt\"', '****-**-** 08:00:00', 127),
(200, 'python protocol_mqtt_sunset_send_to_topic.py home/bedroom/L 1', '****-**-** 23:40:00', 127);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `home_bedroom`
--
ALTER TABLE `home_bedroom`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `home_external`
--
ALTER TABLE `home_external`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `home_general`
--
ALTER TABLE `home_general`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `home_living_room`
--
ALTER TABLE `home_living_room`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `mqtt_historic`
--
ALTER TABLE `mqtt_historic`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `programed_commands`
--
ALTER TABLE `programed_commands`
  ADD PRIMARY KEY (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
