-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Dec 01, 2025 at 07:52 PM
-- Server version: 8.0.34
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ia637_clinicappointment`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `aid` int NOT NULL,
  `date` date NOT NULL,
  `time` varchar(20) NOT NULL,
  `duration` int DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `patientid` int NOT NULL,
  `doctorid` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`aid`, `date`, `time`, `duration`, `status`, `patientid`, `doctorid`) VALUES
(1, '2025-01-15', '10:00', 30, 'confirmed', 2, 1),
(2, '2025-01-16', '14:30', 45, 'scheduled', 2, 1),
(3, '2025-01-18', '09:00', 60, 'completed', 2, 1),
(4, '2025-12-01', '15:15', 0, 'requested', 6, 1),
(5, '2025-12-02', '15:45', NULL, 'requested', 7, NULL),
(6, '2025-11-30', '14:50', 5, 'confirmed', 8, 7),
(7, '2025-12-15', '12:15', 63, 'confirmed', 2, 7);

-- --------------------------------------------------------

--
-- Table structure for table `checkin`
--

CREATE TABLE `checkin` (
  `cid` int NOT NULL,
  `checkintime` varchar(25) NOT NULL,
  `checkouttime` varchar(25) DEFAULT NULL,
  `status` varchar(25) NOT NULL,
  `aid` int NOT NULL,
  `uid` int NOT NULL,
  `rid` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `checkin`
--

INSERT INTO `checkin` (`cid`, `checkintime`, `checkouttime`, `status`, `aid`, `uid`, `rid`) VALUES
(1, '10:00', '', 'waiting', 1, 1, 1),
(2, '', '', 'in room', 6, 1, 1),
(3, '15:19', NULL, 'waiting', 6, 8, NULL),
(4, '12:16', NULL, 'waiting', 7, 2, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `rid` int NOT NULL,
  `roomtype` varchar(50) NOT NULL,
  `roomnumber` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`rid`, `roomtype`, `roomnumber`) VALUES
(1, 'Consultation', '101'),
(2, 'Examination', '102');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `uid` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `role` varchar(25) NOT NULL,
  `password` varchar(100) NOT NULL,
  `specialty` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`uid`, `name`, `email`, `role`, `password`, `specialty`) VALUES
(1, 'beata', 'beata@clarkson.edu', 'doctor', 'a4eb2e0f3e0cbac5c3e64ddc4d24f1df', NULL),
(2, 'Tatenda', 'tatenda@clarkson.edu', 'patient', 'a4eb2e0f3e0cbac5c3e64ddc4d24f1df', NULL),
(3, 'ethan', 'ethan@clarkson.edu', 'patient', '0582ca83820ab884ea72a9bfc8b2c232', NULL),
(5, 'nomcebo', 'nono@gmail.com', 'patient', 'a4eb2e0f3e0cbac5c3e64ddc4d24f1df', NULL),
(6, 'isabel', 'isabel@a.com', 'patient', 'a4eb2e0f3e0cbac5c3e64ddc4d24f1df', NULL),
(7, 'nala', 'nala@g.com', 'doctor', 'e5c5ec94023c839c53ab88bd7c184100', NULL),
(8, 'spongebob', 'bob@sponge.com', 'patient', 'e5c5ec94023c839c53ab88bd7c184100', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointment`
--
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`aid`),
  ADD KEY `patientid` (`patientid`),
  ADD KEY `doctorid` (`doctorid`);

--
-- Indexes for table `checkin`
--
ALTER TABLE `checkin`
  ADD PRIMARY KEY (`cid`),
  ADD KEY `aid` (`aid`),
  ADD KEY `uid` (`uid`),
  ADD KEY `rid` (`rid`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`rid`),
  ADD UNIQUE KEY `roomnumber` (`roomnumber`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `aid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `checkin`
--
ALTER TABLE `checkin`
  MODIFY `cid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `room`
--
ALTER TABLE `room`
  MODIFY `rid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `uid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointment`
--
ALTER TABLE `appointment`
  ADD CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`patientid`) REFERENCES `user` (`uid`),
  ADD CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`doctorid`) REFERENCES `user` (`uid`);

--
-- Constraints for table `checkin`
--
ALTER TABLE `checkin`
  ADD CONSTRAINT `checkin_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `appointment` (`aid`),
  ADD CONSTRAINT `checkin_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`),
  ADD CONSTRAINT `checkin_ibfk_3` FOREIGN KEY (`rid`) REFERENCES `room` (`rid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
