from fpdf import FPDF
from flask import jsonify, send_file
from models.models import Pedidos, Produto
import os

def initcupom(app):
    @app.route('/gerar_cupom/<int:id>', methods=['GET'])
    def gerar_cupom(id):
        # Buscar o pedido do banco de dados
        pedido = Pedidos.query.get_or_404(id)
        pedido_dict = pedido.to_dict()

        # Adicionar os detalhes dos produtos ao pedido
        for item in pedido_dict['itens']:
            produto = Produto.query.get(item['produto_id'])
            item['produto'] = {
                'nome': produto.nome,
                'valor': produto.valor
            }

        # Gerar o PDF do cupom usando os dados do pedido
        caminho_pdf = gerar_cupom_pdf(pedido_dict)

        # Retornar o arquivo PDF como resposta
        return send_file(caminho_pdf, as_attachment=True)

def gerar_cupom_pdf(pedido):
    # Dados do pedido
    cliente_nome = pedido["cliente_nome"]
    venda_id = pedido["id"]
    valor_total = float(pedido["valor_total"])
    itens = pedido["itens"]
    data_pedido = pedido["criado_em"]

    # Dimensões do cupom
    largura_pagina = 80  # Largura fixa do cupom em mm
    linha_altura = 6  # Altura padrão de uma linha em mm
    margem_superior = 10
    margem_inferior = 10
    margem_segura = 10

    # Calcular a altura total do conteúdo
    altura_total = 0

    # Cabeçalho
    altura_total += linha_altura  # Nome do negócio
    altura_total += linha_altura  # CNPJ
    altura_total += 5  # Linha divisória

    # Informações do pedido
    altura_total += linha_altura  # Número e data
    altura_total += linha_altura  # Cliente
    altura_total += 5  # Linha divisória

    # Produtos
    altura_total += linha_altura  # Título "Itens"
    for _ in itens:
        altura_total += linha_altura

    # Total
    altura_total += 5  # Linha divisória
    altura_total += linha_altura  # Total
    altura_total += 5  # Linha divisória

    # Mensagem de agradecimento
    altura_total += linha_altura

    # Adicionar margens
    altura_total += margem_superior + margem_inferior + margem_segura

    # Criar o PDF
    pdf = FPDF(orientation="P", unit="mm", format=(largura_pagina, altura_total))
    pdf.add_page()
    pdf.set_fill_color(255, 255, 199)  # Cor de fundo
    pdf.rect(0, 0, largura_pagina, altura_total, style="F")
    pdf.set_font("Arial", size=10)

    # Cabeçalho
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, linha_altura, "Meireles Lanchonete", ln=True, align="C")
    pdf.set_font("Arial", size=8)
    pdf.cell(0, 5, "CNPJ: 12.345.678/0001-90", ln=True, align="C")
    pdf.cell(0, 5, "-" * 28, ln=True, align="C")

    # Informações do pedido
    pdf.set_font("Arial", size=10)
    pdf.cell(0, linha_altura, f"Venda #{venda_id} - {data_pedido}", ln=True, align="C")
    pdf.cell(0, linha_altura, f"Cliente: {cliente_nome}", ln=True, align="C")
    pdf.cell(0, 5, "-" * 28, ln=True, align="C")

    # Lista de produtos
    pdf.cell(0, linha_altura, "Itens:", ln=True, align="C")
    for item in itens:
        produto_nome = item["produto"]["nome"]
        quantidade = item["quantidade"]
        preco_unitario = item["produto"]["valor"]
        total_item = quantidade * preco_unitario
        linha = f"{produto_nome} x{quantidade} - R$ {preco_unitario:.2f} = R$ {total_item:.2f}"
        pdf.multi_cell(0, 5, linha)

    # Total da venda
    pdf.cell(0, 5, "-" * 28, ln=True, align="C")
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, linha_altura, f"Total: R$ {valor_total:.2f}", ln=True, align="C")
    pdf.cell(0, 5, "-" * 28, ln=True, align="C")

    # Mensagem de agradecimento
    pdf.set_font("Arial", size=10)
    pdf.cell(0, linha_altura, "Obrigado pela preferência!".center(28), ln=True, align="C")

    # Salvar o PDF
    caminho_destino = "C:/Users/jacksonSS/Pictures/cupom/"  # Ajustar o caminho
    if not os.path.exists(caminho_destino):
        os.makedirs(caminho_destino)
    arquivo_pdf = os.path.join(caminho_destino, f"cupom_venda_{venda_id}.pdf")
    pdf.output(arquivo_pdf)

    return arquivo_pdf
