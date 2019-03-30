-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-03-2019 a las 03:07:42
-- Versión del servidor: 10.1.26-MariaDB
-- Versión de PHP: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `supermercado`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logs`
--

CREATE TABLE `logs` (
  `id` int(2) NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `intentos` varchar(10) NOT NULL,
  `hora_ingreso` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `logs`
--

INSERT INTO `logs` (`id`, `fecha_ingreso`, `usuario`, `intentos`, `hora_ingreso`) VALUES
(39, '2019-03-27', 'cajero', 'ok', '19:23:46'),
(40, '2019-03-27', 'cajero', 'ok', '19:31:38'),
(41, '2019-03-27', 'cajero', 'ok', '19:35:28'),
(42, '2019-03-28', 'cajero1', 'ok', '00:41:52'),
(43, '2019-03-28', 'cajero1', 'ok', '00:45:48'),
(44, '2019-03-28', 'cajero1', 'ok', '01:01:43'),
(45, '2019-03-28', 'cajero1', 'ok', '01:09:28'),
(46, '2019-03-28', 'cajero1', 'ok', '01:30:56'),
(47, '2019-03-28', 'cajero1', 'ok', '01:33:05'),
(48, '2019-03-28', 'cajero1', 'ok', '01:47:06'),
(49, '2019-03-28', 'cajero1', 'ok', '01:48:33'),
(50, '2019-03-28', 'cajero1', 'ok', '01:49:30'),
(51, '2019-03-28', 'cajero1', 'ok', '01:53:00'),
(52, '2019-03-28', 'cajero1', 'ok', '01:53:57'),
(53, '2019-03-28', 'cajero1', 'ok', '01:55:49'),
(54, '2019-03-28', 'cajero1', 'ok', '01:56:53'),
(55, '2019-03-28', 'cajero1', 'ok', '02:06:05'),
(56, '2019-03-28', 'cajero1', 'ok', '02:08:04'),
(57, '2019-03-28', 'cajero1', 'ok', '02:08:54'),
(58, '2019-03-28', 'cajero1', 'ok', '02:10:01'),
(59, '2019-03-28', 'cajero1', 'ok', '02:11:07'),
(60, '2019-03-28', 'cajero1', 'ok', '02:12:26'),
(61, '2019-03-28', 'cajero1', 'ok', '02:14:45'),
(62, '2019-03-28', 'cajero1', 'ok', '02:16:16'),
(63, '2019-03-28', 'cajero1', 'ok', '02:19:11'),
(64, '2019-03-28', 'cajero1', 'ok', '02:21:01'),
(65, '2019-03-28', 'cajero1', 'ok', '03:08:48'),
(66, '2019-03-28', 'cajero1', 'ok', '03:12:01'),
(67, '2019-03-28', 'cajero1', 'ok', '03:13:20'),
(68, '2019-03-28', 'cajero1', 'ok', '03:16:50'),
(69, '2019-03-28', 'cajero1', 'ok', '03:18:14'),
(70, '2019-03-28', 'cajero1', 'ok', '03:19:49'),
(71, '2019-03-28', 'cajero1', 'ok', '03:22:49'),
(72, '2019-03-28', 'cajero1', 'ok', '03:39:16'),
(73, '2019-03-28', 'cajero1', 'ok', '03:40:28'),
(74, '2019-03-28', 'cajero1', 'ok', '03:43:06'),
(75, '2019-03-28', 'cajero1', 'ok', '03:46:12'),
(76, '2019-03-28', 'cajero1', 'ok', '03:49:51'),
(77, '2019-03-28', 'cajero1', 'ok', '03:52:33'),
(78, '2019-03-28', 'cajero1', 'ok', '04:04:45'),
(79, '2019-03-28', 'cajero1', 'ok', '04:09:25'),
(80, '2019-03-28', 'cajero1', 'ok', '04:11:30'),
(81, '2019-03-28', 'cajero1', 'ok', '04:20:56'),
(82, '2019-03-28', 'admin', 'ok', '04:25:09'),
(83, '2019-03-28', 'inventario', 'ok', '04:27:51'),
(84, '2019-03-28', 'cajero1', 'ok', '04:28:24'),
(85, '2019-03-28', 'cajero1', 'ok', '04:31:52'),
(86, '2019-03-28', 'cajero1', 'ok', '04:32:44'),
(87, '2019-03-28', 'cajero1', 'ok', '04:55:28'),
(88, '2019-03-28', 'cajero1', 'ok', '04:57:29'),
(89, '2019-03-28', 'cajero1', 'ok', '05:13:33'),
(90, '2019-03-28', 'cajero', 'ok', '05:30:28'),
(91, '2019-03-28', 'cajero', 'ok', '05:36:36'),
(92, '2019-03-28', 'cajero', 'ok', '05:39:03'),
(93, '2019-03-28', 'cajero', 'ok', '05:40:39'),
(94, '2019-03-28', 'cajero', 'ok', '05:44:51'),
(95, '2019-03-28', 'cajero', 'ok', '13:08:21'),
(96, '2019-03-28', 'cajero', 'ok', '13:09:17'),
(97, '2019-03-28', 'cajero', 'ok', '13:10:17'),
(98, '2019-03-28', 'cajero', 'ok', '13:20:04'),
(99, '2019-03-28', 'cajero', 'ok', '13:22:27'),
(100, '2019-03-28', 'cajero', 'ok', '13:27:53'),
(101, '2019-03-28', 'cajero', 'ok', '13:31:18'),
(102, '2019-03-28', 'cajero', 'Fallo', '13:33:59'),
(103, '2019-03-28', 'cajero', 'ok', '13:34:23'),
(104, '2019-03-28', 'cajero', 'ok', '14:39:01'),
(105, '2019-03-28', 'cajero', 'ok', '14:41:06'),
(106, '2019-03-28', 'cajero', 'ok', '14:43:41'),
(107, '2019-03-28', 'cajero', 'ok', '14:49:57'),
(108, '2019-03-28', 'cajero', 'ok', '14:53:33'),
(109, '2019-03-28', 'cajero', 'Fallo', '18:01:16'),
(110, '2019-03-28', 'cajero', 'ok', '18:01:22'),
(111, '2019-03-28', 'cajero', 'ok', '18:47:08'),
(112, '2019-03-28', 'cajero', 'ok', '18:48:42'),
(113, '2019-03-28', 'cajero', 'ok', '19:00:03'),
(114, '2019-03-28', 'cajero', 'ok', '19:12:23'),
(115, '2019-03-28', 'cajero', 'ok', '19:15:15'),
(116, '2019-03-28', 'cajero', 'ok', '19:33:04'),
(117, '2019-03-28', 'cajero', 'ok', '22:21:05'),
(118, '2019-03-28', 'cajero', 'ok', '22:22:25'),
(119, '2019-03-28', 'cajero', 'ok', '22:38:23'),
(120, '2019-03-28', 'cajero', 'ok', '22:41:07'),
(121, '2019-03-28', 'cajero', 'ok', '22:46:17'),
(122, '2019-03-28', 'cajero', 'ok', '22:48:02'),
(123, '2019-03-28', 'cajero', 'ok', '23:21:24'),
(124, '2019-03-28', 'cajero', 'ok', '23:23:05'),
(125, '2019-03-28', 'cajero', 'ok', '23:25:41'),
(126, '2019-03-29', 'cajero', 'ok', '00:15:06'),
(127, '2019-03-29', 'cajero', 'ok', '00:22:36'),
(128, '2019-03-29', 'cajero', 'ok', '00:26:09'),
(129, '2019-03-29', 'cajero', 'ok', '00:31:35'),
(130, '2019-03-29', 'cajero', 'ok', '00:33:04'),
(131, '2019-03-29', 'cajero', 'ok', '00:36:43'),
(132, '2019-03-29', 'cajero', 'ok', '00:49:52'),
(133, '2019-03-29', 'cajero', 'ok', '00:52:14'),
(134, '2019-03-29', 'cajero', 'ok', '00:57:22'),
(135, '2019-03-29', 'cajero', 'ok', '01:06:07'),
(136, '2019-03-29', 'cajero', 'ok', '01:08:52'),
(137, '2019-03-29', 'cajero', 'ok', '01:11:03'),
(138, '2019-03-29', 'cajero', 'ok', '01:39:41'),
(139, '2019-03-29', 'cajero', 'ok', '01:41:35'),
(140, '2019-03-29', 'cajero', 'ok', '01:43:50'),
(141, '2019-03-29', 'cajero', 'ok', '01:49:45'),
(142, '2019-03-29', 'cajero', 'ok', '02:17:10'),
(143, '2019-03-29', 'cajero', 'ok', '02:18:49'),
(144, '2019-03-29', 'cajero', 'ok', '02:30:03'),
(145, '2019-03-29', 'cajero', 'ok', '02:45:41'),
(146, '2019-03-29', 'cajero', 'ok', '02:47:16'),
(147, '2019-03-29', 'cajero', 'ok', '03:18:08'),
(148, '2019-03-29', 'cajero', 'ok', '03:23:07'),
(149, '2019-03-29', 'cajero', 'ok', '03:29:24'),
(150, '2019-03-29', 'cajero', 'ok', '03:41:11'),
(151, '2019-03-29', 'cajero', 'ok', '03:42:56'),
(152, '2019-03-29', 'cajero', 'ok', '03:46:24'),
(153, '2019-03-29', 'cajero', 'ok', '03:47:37'),
(154, '2019-03-29', 'cajero', 'ok', '03:55:14'),
(155, '2019-03-29', 'cajero', 'ok', '04:08:55'),
(156, '2019-03-29', 'cajero', 'ok', '04:16:21'),
(157, '2019-03-29', 'cajero', 'ok', '04:20:41'),
(158, '2019-03-29', 'cajero', 'ok', '04:37:47'),
(159, '2019-03-29', 'cajero', 'ok', '05:04:18'),
(160, '2019-03-29', 'cajero', 'ok', '05:08:55'),
(161, '2019-03-29', 'cajero', 'ok', '05:16:13'),
(162, '2019-03-29', 'cajero', 'ok', '05:19:05'),
(163, '2019-03-29', 'cajero', 'ok', '05:20:33'),
(164, '2019-03-29', 'cajero', 'ok', '05:25:54'),
(165, '2019-03-29', 'cajero', 'ok', '05:28:29'),
(166, '2019-03-29', 'cajero', 'ok', '05:30:04'),
(167, '2019-03-29', 'cajero', 'ok', '05:32:19'),
(168, '2019-03-29', 'cajero', 'ok', '05:47:34'),
(169, '2019-03-29', 'admin', 'ok', '05:51:24'),
(170, '2019-03-29', 'cajero', 'ok', '06:00:06'),
(171, '2019-03-29', 'admin', 'ok', '06:01:03'),
(172, '2019-03-29', 'cajero', 'ok', '06:02:05'),
(173, '2019-03-29', 'inventario', 'ok', '06:04:36'),
(174, '2019-03-29', 'inventario', 'ok', '06:35:19'),
(175, '2019-03-29', 'inventario', 'ok', '06:40:00'),
(176, '2019-03-29', 'inventario', 'ok', '06:47:05'),
(177, '2019-03-29', 'inventario', 'ok', '07:12:58'),
(178, '2019-03-29', 'inventario', 'ok', '07:37:59'),
(179, '2019-03-29', 'inventario', 'ok', '07:41:59'),
(180, '2019-03-29', 'inventario', 'ok', '07:48:03'),
(181, '2019-03-29', 'inventario', 'ok', '07:54:26'),
(182, '2019-03-29', 'inventario', 'ok', '10:19:40'),
(183, '2019-03-29', 'inventario', 'ok', '10:26:32'),
(184, '2019-03-29', 'inventario', 'ok', '10:45:02'),
(185, '2019-03-29', 'inventario', 'ok', '10:47:53'),
(186, '2019-03-29', 'inventario', 'ok', '11:03:59'),
(187, '2019-03-29', 'inventario', 'ok', '11:17:16'),
(188, '2019-03-29', 'inventario', 'Fallo', '11:21:35'),
(189, '2019-03-29', 'inventario', 'ok', '11:21:48'),
(190, '2019-03-29', 'inventario', 'ok', '11:35:45'),
(191, '2019-03-29', 'inventario', 'ok', '12:08:55'),
(192, '2019-03-29', 'inventario', 'ok', '12:15:30'),
(193, '2019-03-29', 'inventario', 'ok', '12:29:24'),
(194, '2019-03-29', 'inventario', 'Fallo', '12:35:49'),
(195, '2019-03-29', 'inventario', 'ok', '12:36:12'),
(196, '2019-03-29', 'inventario', 'ok', '13:02:04'),
(197, '2019-03-29', 'cajero', 'ok', '13:28:59'),
(198, '2019-03-29', 'cajero', 'ok', '13:30:15'),
(199, '2019-03-29', 'cajero1', 'Fallo', '13:30:59'),
(200, '2019-03-29', 'cajero 2', 'ok', '13:31:21'),
(201, '2019-03-29', 'cajero2', 'ok', '13:41:47'),
(202, '2019-03-29', 'cajero2', 'ok', '13:44:44'),
(203, '2019-03-29', 'cajero2', 'ok', '13:47:21'),
(204, '2019-03-29', 'cajero2', 'ok', '13:57:10'),
(205, '2019-03-29', 'cajero2', 'ok', '14:04:16'),
(206, '2019-03-29', 'cajero2', 'ok', '14:10:13'),
(207, '2019-03-29', 'cajero2', 'ok', '14:12:04'),
(208, '2019-03-29', 'cajero2', 'ok', '14:14:08'),
(209, '2019-03-29', 'cajero2', 'ok', '14:16:59'),
(210, '2019-03-29', 'admin', 'ok', '18:02:44'),
(211, '2019-03-29', 'admin', 'ok', '18:10:26'),
(212, '2019-03-29', 'admin', 'ok', '18:11:51'),
(213, '2019-03-29', 'cajero2', 'ok', '18:12:27'),
(214, '2019-03-29', 'admin', 'ok', '21:01:55');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=215;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;