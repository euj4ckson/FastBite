from fpdf import FPDF
from flask import send_file
from models.models import Pedidos, Produto
import os

def initcupom(app):
    @app.route('/gerar_cupom/<int:id>', methods=['GET'])
    def gerar_cupom(id):
        pedido = Pedidos.query.get_or_404(id)
        pedido_dict = pedido.to_dict()

        for item in pedido_dict['itens']:
            produto = Produto.query.get(item['produto_id'])
            item['produto'] = {
                'nome': produto.nome,
                'valor': produto.valor
            }

        caminho_pdf = gerar_cupom_pdf(pedido_dict)
        return send_file(caminho_pdf, as_attachment=True)

def gerar_cupom_pdf(pedido):
    cliente_nome = pedido["cliente_nome"]
    venda_id = pedido["id"]
    valor_total = float(pedido["valor_total"])
    itens = pedido["itens"]
    data_pedido = pedido["criado_em"]

    # Dimensões do cupom
    largura_pagina = 80  
    linha_altura = 6  
    margem_superior = 8  
    margem_inferior = 8  

    # Calcular altura total
    altura_fixa = margem_superior + margem_inferior + (linha_altura * 16)  # Cabeçalho e rodapé fixos
    altura_itens = linha_altura * len(itens)  # Altura dinâmica conforme a quantidade de itens
    altura_total = altura_fixa + altura_itens

    # Criar PDF com altura correta
    pdf = FPDF(orientation="P", unit="mm", format=(largura_pagina, altura_total))
    pdf.add_page()
    pdf.set_font("Courier", size=9)

    # Cabeçalho
    pdf.set_font("Courier", style="B", size=12)
    pdf.cell(0, linha_altura, "MEIRELES LANCHONETE", ln=True, align="C")
    pdf.set_font("Courier", size=9)
    pdf.cell(0, linha_altura, "CNPJ: 12.345.678/0001-90", ln=True, align="C")
    pdf.cell(0, linha_altura, "-" * 32, ln=True, align="C")

    # Informações do pedido
    pdf.cell(0, linha_altura, f"Venda: {venda_id} {data_pedido}", ln=True, align="L")
    pdf.cell(0, linha_altura, f"Cliente: {cliente_nome}", ln=True, align="L")
    pdf.cell(0, linha_altura, "-" * 32, ln=True, align="C")

    # Cabeçalho dos produtos
    pdf.cell(24, linha_altura, "ITEM", border=0)
    pdf.cell(10, linha_altura, "QTD", border=0 ,align="L")
    pdf.cell(15, linha_altura, "UNIT", border=0 ,align="L")
    pdf.cell(15, linha_altura, "TOTAL", border=0, align="R")
    pdf.cell(0, linha_altura, "", ln=True)
    pdf.cell(0, 1, "-" * 32, ln=True, align="C")

    # Lista de produtos corrigida
    for item in itens:
        produto_nome = item["produto"]["nome"][:14]
        quantidade = item["quantidade"]
        preco_unitario = item["produto"]["valor"]
        total_item = quantidade * preco_unitario

        pdf.cell(24, linha_altura, produto_nome, border=0)
        pdf.cell(10, linha_altura, str(quantidade), border=0, align="C")
        pdf.cell(15, linha_altura, f"{preco_unitario:.2f}", border=0, align="C")
        pdf.cell(15, linha_altura, f"{total_item:.2f}", border=0, align="R")
        pdf.cell(0, linha_altura, "", ln=True)  # Evita quebra incorreta

    pdf.cell(0, 1, "-" * 32, ln=True, align="C")

    # Total da venda
    pdf.set_font("Courier", style="B", size=10)
    pdf.cell(0, linha_altura, f"TOTAL: R$ {valor_total:.2f}", ln=True, align="C")

    # Mensagem de agradecimento
    pdf.cell(0, linha_altura, "-" * 32, ln=True, align="C")
    pdf.set_font("Courier", size=9)
    pdf.cell(0, linha_altura, "OBRIGADO PELA PREFERENCIA!", ln=True, align="C")
    pdf.cell(0, linha_altura, "VOLTE SEMPRE!", ln=True, align="C")

    # Salvar PDF
    caminho_destino = "C:/Users/jacksonSS/Pictures/cupom/"
    if not os.path.exists(caminho_destino):
        os.makedirs(caminho_destino)
    arquivo_pdf = os.path.join(caminho_destino, f"cupom_venda_{venda_id}.pdf")
    pdf.output(arquivo_pdf)

    return arquivo_pdf
