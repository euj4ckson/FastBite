from fpdf import FPDF
from flask import send_file
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

    # Dimensões fixas do cupom
    largura_pagina = 80  # Largura do cupom em mm
    linha_altura = 6  # Altura padrão de uma linha em mm
    margem_superior = 10
    margem_inferior = 10

    # Calcular a altura do conteúdo dinamicamente
    altura_cabecalho = linha_altura * 2 + 5  # Cabeçalho (nome e CNPJ)
    altura_infos_pedido = linha_altura * 2 + 5  # Informações do pedido (venda, cliente)
    altura_itens = linha_altura * len(itens)  # Altura proporcional ao número de itens
    altura_total = (
        margem_superior
        + altura_cabecalho
        + altura_infos_pedido
        + linha_altura  # Título "Itens"
        + altura_itens
        + 5  # Linha divisória antes do total
        + linha_altura  # Total da venda
        + linha_altura  # Mensagem de agradecimento
        + margem_inferior
        +30
    )

    # Criar o PDF com altura dinâmica
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
    pdf.cell(0, linha_altura, f"Venda {venda_id} - {data_pedido}", ln=True, align="C")
    pdf.cell(0, linha_altura, f"Cliente: {cliente_nome}", ln=True, align="C")
    pdf.cell(0, 5, "-" * 28, ln=True, align="C")

    # Lista de produtos
    pdf.cell(0, linha_altura, "Itens:", ln=True, align="C")
    for item in itens:
        produto_nome = item["produto"]["nome"]
        quantidade = item["quantidade"]
        preco_unitario = item["produto"]["valor"]
        total_item = quantidade * preco_unitario
        linha = f"{produto_nome} x {quantidade} = R$ {total_item:.2f}"
        pdf.multi_cell(0, linha_altura, linha)

    # Total da venda
    pdf.cell(0, 5, "-" * 28, ln=True, align="C")
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, linha_altura, f"Total: R$ {valor_total:.2f}", ln=True, align="C")
    pdf.cell(0, 5, "-" * 28, ln=True, align="C")

    # Mensagem de agradecimento
    pdf.set_font("Arial", size=10)
    pdf.cell(0, linha_altura, "Obrigado pela preferência!".center(28), ln=True, align="C")

    # Salvar o PDF
    caminho_destino = "C:/Users/jacksonSS/Pictures/cupom/"
    if not os.path.exists(caminho_destino):
        os.makedirs(caminho_destino)
    arquivo_pdf = os.path.join(caminho_destino, f"cupom_venda_{venda_id}.pdf")
    pdf.output(arquivo_pdf)

    return arquivo_pdf

