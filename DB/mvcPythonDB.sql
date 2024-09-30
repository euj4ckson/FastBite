-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           11.5.2-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para minha_aplicacao
CREATE DATABASE IF NOT EXISTS `minha_aplicacao` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `minha_aplicacao`;

-- Copiando estrutura para tabela minha_aplicacao.eventos
CREATE TABLE IF NOT EXISTS `eventos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `descricao` text NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `atualizado_em` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.eventos: ~2 rows (aproximadamente)
INSERT INTO `eventos` (`id`, `titulo`, `descricao`, `usuario_id`, `criado_em`, `atualizado_em`) VALUES
	(1, 'Evento teste', 'Descrição alterada', 1, '2024-09-30 12:55:18', '2024-09-30 15:51:29'),
	(4, 'evento de usuario 2', 'evento usuario 2 teste', 7, '2024-09-30 17:01:31', '2024-09-30 17:01:31');

-- Copiando estrutura para tabela minha_aplicacao.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `criado_em` timestamp NULL DEFAULT current_timestamp(),
  `atualizado_em` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.usuarios: ~2 rows (aproximadamente)
INSERT INTO `usuarios` (`id`, `nome`, `email`, `senha`, `criado_em`, `atualizado_em`) VALUES
	(1, 'jack', 'jacksonduardo6@gmail.com', 'scrypt:32768:8:1$7Mly5KOVK1srgmgr$9052e20976c6c1645c985565f9fd8cd3138d80891c89d559bb88c32de9844b69d3fc24454b78b13a9382dc58ac7f9a6ffad170718430735c616eacf62f885446', '2024-09-26 13:48:34', '2024-09-27 19:17:05'),
	(7, 'teste evento', 'suporte@sssolucoes.net', 'scrypt:32768:8:1$DRzITEIeqGwsB8vu$cf7d173fe033441b83098ed95e4624aaeedca2e5a0778065ac05e5cd5ef707373fddb502460eed33014089297c2e9fd51a1d8fa26fb3e03f509b919110cd3602', '2024-09-30 20:00:41', '2024-09-30 20:00:41');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
