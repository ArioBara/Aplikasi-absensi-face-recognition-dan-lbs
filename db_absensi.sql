-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 07 Jan 2024 pada 13.45
-- Versi server: 10.4.27-MariaDB
-- Versi PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_absensi`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`id_admin`, `username`, `password`, `nama`) VALUES
(3, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');

-- --------------------------------------------------------

--
-- Struktur dari tabel `cuty`
--

CREATE TABLE `cuty` (
  `id_cuty` int(11) NOT NULL,
  `id_employees` int(11) NOT NULL,
  `cuty_start` date NOT NULL,
  `cuty_end` date NOT NULL,
  `date_work` date NOT NULL,
  `cuty_description` text NOT NULL,
  `cuty_status` enum('menunggu','diterima','ditolak') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `employees`
--

CREATE TABLE `employees` (
  `id_employees` int(11) NOT NULL,
  `employees_code` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `id_users` int(11) NOT NULL,
  `id_position` int(11) NOT NULL,
  `id_shift` int(11) NOT NULL,
  `photo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `faces`
--

CREATE TABLE `faces` (
  `id_faces` int(11) NOT NULL,
  `id_employees` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `position`
--

CREATE TABLE `position` (
  `id_position` int(11) NOT NULL,
  `position_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `position`
--

INSERT INTO `position` (`id_position`, `position_name`) VALUES
(1, 'CEO'),
(2, 'Keuangan');

-- --------------------------------------------------------

--
-- Struktur dari tabel `presence`
--

CREATE TABLE `presence` (
  `id_presence` int(11) NOT NULL,
  `id_employees` int(11) NOT NULL,
  `presence_date` date NOT NULL,
  `time_in` varchar(50) NOT NULL,
  `time_out` varchar(50) NOT NULL,
  `picture_in` varchar(255) NOT NULL,
  `picture_out` varchar(255) NOT NULL,
  `id_present` int(11) NOT NULL,
  `koordinat_in` varchar(100) NOT NULL,
  `koordinat_out` varchar(100) NOT NULL,
  `keterangan` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `present_status`
--

CREATE TABLE `present_status` (
  `id_present` int(11) NOT NULL,
  `present_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `present_status`
--

INSERT INTO `present_status` (`id_present`, `present_name`) VALUES
(1, 'Hadir'),
(2, 'Sakit'),
(3, 'Izin');

-- --------------------------------------------------------

--
-- Struktur dari tabel `shift`
--

CREATE TABLE `shift` (
  `id_shift` int(11) NOT NULL,
  `shift_name` varchar(20) NOT NULL,
  `time_in` time NOT NULL,
  `time_out` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `shift`
--

INSERT INTO `shift` (`id_shift`, `shift_name`, `time_in`, `time_out`) VALUES
(1, 'Full Time', '08:00:00', '17:00:00'),
(2, 'Part Time', '08:00:00', '12:00:00'),
(3, 'Remote', '08:30:00', '16:00:00');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id_users` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indeks untuk tabel `cuty`
--
ALTER TABLE `cuty`
  ADD PRIMARY KEY (`id_cuty`),
  ADD KEY `id_employees` (`id_employees`);

--
-- Indeks untuk tabel `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id_employees`),
  ADD KEY `id_users` (`id_users`),
  ADD KEY `id_position` (`id_position`),
  ADD KEY `id_shift` (`id_shift`);

--
-- Indeks untuk tabel `faces`
--
ALTER TABLE `faces`
  ADD PRIMARY KEY (`id_faces`),
  ADD KEY `id_employees` (`id_employees`);

--
-- Indeks untuk tabel `position`
--
ALTER TABLE `position`
  ADD PRIMARY KEY (`id_position`);

--
-- Indeks untuk tabel `presence`
--
ALTER TABLE `presence`
  ADD PRIMARY KEY (`id_presence`),
  ADD KEY `id_employees` (`id_employees`),
  ADD KEY `id_present` (`id_present`);

--
-- Indeks untuk tabel `present_status`
--
ALTER TABLE `present_status`
  ADD PRIMARY KEY (`id_present`);

--
-- Indeks untuk tabel `shift`
--
ALTER TABLE `shift`
  ADD PRIMARY KEY (`id_shift`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_users`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `cuty`
--
ALTER TABLE `cuty`
  MODIFY `id_cuty` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `employees`
--
ALTER TABLE `employees`
  MODIFY `id_employees` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT untuk tabel `faces`
--
ALTER TABLE `faces`
  MODIFY `id_faces` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT untuk tabel `position`
--
ALTER TABLE `position`
  MODIFY `id_position` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `presence`
--
ALTER TABLE `presence`
  MODIFY `id_presence` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT untuk tabel `present_status`
--
ALTER TABLE `present_status`
  MODIFY `id_present` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `shift`
--
ALTER TABLE `shift`
  MODIFY `id_shift` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id_users` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `cuty`
--
ALTER TABLE `cuty`
  ADD CONSTRAINT `cuty_ibfk_1` FOREIGN KEY (`id_employees`) REFERENCES `employees` (`id_employees`);

--
-- Ketidakleluasaan untuk tabel `employees`
--
ALTER TABLE `employees`
  ADD CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`id_users`) REFERENCES `users` (`id_users`),
  ADD CONSTRAINT `employees_ibfk_2` FOREIGN KEY (`id_position`) REFERENCES `position` (`id_position`),
  ADD CONSTRAINT `employees_ibfk_3` FOREIGN KEY (`id_shift`) REFERENCES `shift` (`id_shift`);

--
-- Ketidakleluasaan untuk tabel `faces`
--
ALTER TABLE `faces`
  ADD CONSTRAINT `faces_ibfk_1` FOREIGN KEY (`id_employees`) REFERENCES `employees` (`id_employees`);

--
-- Ketidakleluasaan untuk tabel `presence`
--
ALTER TABLE `presence`
  ADD CONSTRAINT `presence_ibfk_1` FOREIGN KEY (`id_employees`) REFERENCES `employees` (`id_employees`),
  ADD CONSTRAINT `presence_ibfk_2` FOREIGN KEY (`id_present`) REFERENCES `present_status` (`id_present`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
