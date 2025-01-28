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

-- Copiando estrutura para tabela minha_aplicacao.alembic_version
CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.alembic_version: ~0 rows (aproximadamente)
INSERT INTO `alembic_version` (`version_num`) VALUES
	('3af07fd60a5a');

-- Copiando estrutura para tabela minha_aplicacao.pedidos
CREATE TABLE IF NOT EXISTS `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_nome` varchar(100) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `valor_total` decimal(10,2) NOT NULL DEFAULT 0.00,
  `entregue` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.pedidos: ~5 rows (aproximadamente)
INSERT INTO `pedidos` (`id`, `cliente_nome`, `criado_em`, `valor_total`, `entregue`) VALUES
	(25, 'jackson', '2025-01-09 10:37:10', 78.00, 0),
	(27, 'MARIAO', '2025-01-07 21:12:33', 34.00, 0),
	(31, 'ULTIMO TESTE DE VERDADE EDITADO', '2025-01-09 15:42:18', 36.00, 0),
	(32, 'hoje', '2025-01-23 11:19:57', 67.50, 0),
	(33, 'TESTE', '2025-01-28 16:50:37', 28.00, 0);

-- Copiando estrutura para tabela minha_aplicacao.pedido_itens
CREATE TABLE IF NOT EXISTS `pedido_itens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pedido_id` int(11) NOT NULL,
  `produto_id` int(11) NOT NULL,
  `quantidade` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `pedido_itens_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `pedido_itens_ibfk_2` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.pedido_itens: ~11 rows (aproximadamente)
INSERT INTO `pedido_itens` (`id`, `pedido_id`, `produto_id`, `quantidade`) VALUES
	(34, 25, 3, 2),
	(41, 27, 4, 1),
	(46, 27, 7, 2),
	(47, 27, 1, 1),
	(48, 25, 4, 2),
	(49, 25, 7, 4),
	(52, 31, 3, 2),
	(54, 31, 9, 2),
	(55, 32, 1, 3),
	(56, 32, 8, 5),
	(57, 33, 4, 2);

-- Copiando estrutura para tabela minha_aplicacao.produtos
CREATE TABLE IF NOT EXISTS `produtos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(200) NOT NULL,
  `valor` float NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `atualizado_em` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.produtos: ~9 rows (aproximadamente)
INSERT INTO `produtos` (`id`, `nome`, `valor`, `criado_em`, `atualizado_em`) VALUES
	(1, 'Hambúrguer Simples', 10, '2024-12-09 16:14:21', '2024-12-09 16:14:21'),
	(2, 'Cheeseburger', 12.5, '2024-12-09 16:14:21', '2024-12-09 16:14:21'),
	(3, 'X-Bacon', 15, '2024-12-09 16:14:21', '2024-12-09 16:14:21'),
	(4, 'X-Egg', 14, '2024-12-09 16:14:21', '2024-12-09 16:14:21'),
	(5, 'X-Tudo', 20, '2024-12-09 16:14:21', '2024-12-09 16:14:21'),
	(7, 'Refrigerante Lata', 5, '2024-12-09 16:14:21', '2024-12-09 16:14:21'),
	(8, 'Refrigerante 600ml', 7.5, '2024-12-09 16:14:21', '2024-12-09 16:14:21'),
	(9, 'Água Mineral', 3, '2024-12-09 16:14:21', '2024-12-09 16:14:21');

-- Copiando estrutura para tabela minha_aplicacao.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `atualizado_em` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.usuarios: ~2 rows (aproximadamente)
INSERT INTO `usuarios` (`id`, `nome`, `email`, `senha`, `criado_em`, `atualizado_em`) VALUES
	(1, 'jack', 'jacksonduardo6@gmail.com', 'scrypt:32768:8:1$7Mly5KOVK1srgmgr$9052e20976c6c1645c985565f9fd8cd3138d80891c89d559bb88c32de9844b69d3fc24454b78b13a9382dc58ac7f9a6ffad170718430735c616eacf62f885446', '2024-09-26 10:48:34', '2024-09-27 16:17:05'),
	(7, 'teste evento', 'suporte@sssolucoes.net', 'scrypt:32768:8:1$DRzITEIeqGwsB8vu$cf7d173fe033441b83098ed95e4624aaeedca2e5a0778065ac05e5cd5ef707373fddb502460eed33014089297c2e9fd51a1d8fa26fb3e03f509b919110cd3602', '2024-09-30 17:00:41', '2024-09-30 17:00:41');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
