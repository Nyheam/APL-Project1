-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 05, 2025 at 05:21 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ticket_booking_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `BookingReference` varchar(50) NOT NULL,
  `TicketType` varchar(50) DEFAULT NULL,
  `EventName` varchar(255) DEFAULT NULL,
  `Date` varchar(20) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  `PaymentMethod` varchar(50) DEFAULT NULL,
  `BookingTimestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`BookingReference`, `TicketType`, `EventName`, `Date`, `Quantity`, `Status`, `PaymentMethod`, `BookingTimestamp`) VALUES
('BOOK5465875F', 'concert', 'RockFest 2024', '2024-12-20', 2, 'reserved', NULL, '2025-03-04 04:16:16'),
('BOOK58579BCD', 'concert', 'RockFest 2024', '2024-12-20', 2, 'reserved', NULL, '2025-03-05 00:42:52'),
('BOOK760E445A', 'concert', 'Reggae Sumfest', '2024-12-20', 2, 'reserved', NULL, '2025-03-05 00:43:43');

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `EventID` int(11) NOT NULL,
  `TicketType` varchar(50) DEFAULT NULL,
  `EventName` varchar(255) DEFAULT NULL,
  `EventDate` varchar(20) DEFAULT NULL,
  `AvailableTickets` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`EventID`, `TicketType`, `EventName`, `EventDate`, `AvailableTickets`) VALUES
(1, 'concert', 'RockFest 2024', '2024-12-20', 100),
(2, 'concert', 'Jazz Night', '2024-12-25', 50),
(3, 'train ticket', 'London to Paris', '2025-01-15', 20),
(4, 'train ticket', 'New York to Boston', '2024-12-25', 15),
(5, 'bus ticket', 'Local Bus Route 1', '2024-12-10', 100),
(6, 'bus ticket', 'Express City Bus', '2024-12-18', 60),
(7, 'airline ticket', 'Flights to New York', '2025-02-10', 30),
(8, 'airline ticket', 'Flights to Tokyo', '2025-03-01', 25),
(9, 'football match', 'Local Derby Match', '2024-12-22', 80),
(10, 'football match', 'Championship Final', '2024-12-29', 40);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`BookingReference`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`EventID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `EventID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
