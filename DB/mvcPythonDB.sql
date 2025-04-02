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
	('a91b1b727100');

-- Copiando estrutura para tabela minha_aplicacao.pedidos
CREATE TABLE IF NOT EXISTS `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_nome` varchar(100) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `valor_total` decimal(10,2) NOT NULL DEFAULT 0.00,
  `entregue` int(11) NOT NULL,
  `observacao` varchar(100) NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.pedidos: ~8 rows (aproximadamente)
INSERT INTO `pedidos` (`id`, `cliente_nome`, `criado_em`, `valor_total`, `entregue`, `observacao`, `endereco`) VALUES
	(39, 'Jackson Eduardo Da Silva Costa', '2025-02-26 14:59:48', 113.00, 0, 'pedido com itens iguais', ''),
	(44, 'teste finalizar pedido', '2025-03-26 16:02:08', 982.00, 1, 'finalizar pedido', ''),
	(46, 'asdasd 3333', '2025-04-02 09:26:38', 64.50, 0, 'asdasdsdasdasdsd 333', ''),
	(47, 'jackson pelo celular', '2025-04-02 09:58:26', 50.00, 1, 'teste do celular', ''),
	(48, 'asd', '2025-04-02 10:13:44', 42.00, 0, 'asdasd', ''),
	(49, 'asd', '2025-04-02 10:15:11', 25.00, 0, 'asd', ''),
	(50, 'asd', '2025-04-02 10:21:33', 42.00, 0, 'asd', ''),
	(51, 'asd', '2025-04-02 10:25:56', 42.00, 0, 'asd', ''),
	(52, 'teste finalizar pedido', '2025-04-02 11:32:58', 29.00, 0, 'asdasdasd', 'rua da agua, 123, centro, Ewbank da Câmara, MG, CEP: 36108000'),
	(53, 'teste finalizar pedido produto 2x', '2025-04-02 11:37:01', 57.00, 0, 'asdasdasd', 'rua da agua, 123, centro, Ewbank da Câmara, MG, CEP: 36108000'),
	(54, 'teste finalizar pedido produto 2x', '2025-04-02 11:42:08', 71.00, 0, 'asdasdasd', 'rua da agua, 123, centro, Ewbank da Câmara, MG, CEP: 36108000'),
	(55, 'teste limpar', '2025-04-02 11:46:16', 22.50, 0, 'teste limpar', 'alfredo rodrigues, 123, centro, Ewbank da Câmara, MG, CEP: 36108000'),
	(56, 'teste finalizar pedido', '2025-04-02 12:02:22', 56.00, 0, 'asdasdasdasd', 'rua da agua, 123, centro, Ewbank da Câmara, MG, CEP: 36108000'),
	(57, 'teste finalizar pedido', '2025-04-02 12:14:50', 40.00, 0, 'teste finalizar pedido observação', 'rua da agua, 123, centro, Ewbank da Câmara, MG, CEP: 36108000');

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
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.pedido_itens: ~13 rows (aproximadamente)
INSERT INTO `pedido_itens` (`id`, `pedido_id`, `produto_id`, `quantidade`) VALUES
	(71, 39, 2, 2),
	(72, 39, 4, 2),
	(73, 39, 5, 3),
	(82, 44, 4, 23),
	(83, 44, 3, 44),
	(86, 46, 4, 3),
	(87, 46, 8, 3),
	(88, 47, 7, 2),
	(89, 47, 5, 2),
	(90, 48, 4, 3),
	(91, 49, 2, 2),
	(92, 50, 4, 3),
	(93, 51, 4, 3),
	(94, 52, 4, 1),
	(95, 52, 8, 2),
	(96, 53, 4, 2),
	(97, 53, 8, 2),
	(98, 53, 4, 3),
	(99, 54, 4, 1),
	(100, 54, 8, 2),
	(101, 54, 4, 3),
	(102, 55, 8, 3),
	(103, 56, 4, 4),
	(104, 57, 5, 2);

-- Copiando estrutura para tabela minha_aplicacao.produtos
CREATE TABLE IF NOT EXISTS `produtos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(200) NOT NULL,
  `valor` float NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `atualizado_em` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Copiando dados para a tabela minha_aplicacao.produtos: ~8 rows (aproximadamente)
INSERT INTO `produtos` (`id`, `nome`, `valor`, `criado_em`, `atualizado_em`) VALUES
	(1, 'SELECIONE O PRODUTO', 12, '2024-12-09 16:14:21', '2025-04-01 09:32:17'),
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
