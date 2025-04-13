from flask import send_file, jsonify
from io import BytesIO
import qrcode
from models.models import Pedidos

def initqrcode(app):
    def gerar_payload_pix(chave, nome, cidade, valor, txid):
        def format_field(id, value):
            length = f"{len(value):02}"
            return f"{id}{length}{value}"

        merchant_account_info = (
            format_field("00", "BR.GOV.BCB.PIX") +
            format_field("01", chave)
        )
        merchant_account = format_field("26", merchant_account_info)
        txid_info = format_field("05", txid)
        additional_data_field = format_field("62", txid_info)

        payload = (
            format_field("00", "01") +  # Payload Format Indicator
            merchant_account +          # Merchant Account Info
            format_field("52", "0000") +  # Merchant Category Code
            format_field("53", "986") +   # Currency (BRL)
            format_field("54", f"{valor:.2f}") +  # Transaction amount
            format_field("58", "BR") +    # Country Code
            format_field("59", nome) +    # Merchant Name
            format_field("60", cidade) +  # Merchant City
            additional_data_field +       # Additional Data Field Template (TXID)
            "6304"                         # CRC16 placeholder
        )

        def crc16(payload):
            polinomio = 0x1021
            resultado = 0xFFFF
            for char in payload:
                resultado ^= ord(char) << 8
                for _ in range(8):
                    if resultado & 0x8000:
                        resultado = (resultado << 1) ^ polinomio
                    else:
                        resultado <<= 1
                    resultado &= 0xFFFF
            return f"{resultado:04X}"

        crc = crc16(payload)
        return payload + crc


    @app.route('/pix_qrcode/<int:pedido_id>')
    def gerar_pix_qrcode(pedido_id):
        pedido = Pedidos.query.get(pedido_id)
        if not pedido:
            return {"erro": "Pedido não encontrado"}, 404

        if pedido.forma_pagamento.lower() != 'pix':
            return {"erro": "A forma de pagamento do pedido não é Pix"}, 400

        try:
            chave_pix = 'jacksonduardo6@gmail.com'
            nome_recebedor = 'Lanchonete Meireles'
            cidade = 'EWBANK'
            valor = float(str(pedido.valor_total).replace(',', '.'))
            txid = f"PED{pedido.id:06d}"

            payload = gerar_payload_pix(
                chave=chave_pix,
                nome=nome_recebedor,
                cidade=cidade,
                valor=valor,
                txid=txid
            )

            qr = qrcode.make(payload)
            buf = BytesIO()
            qr.save(buf, format='PNG')
            buf.seek(0)

            return send_file(
                buf,
                mimetype='image/png',
                as_attachment=False,
                download_name=f'qrcode_pedido_{pedido.id}.png'
            )

        except Exception as e:
            return {"erro": f"Erro ao gerar QR Code: {str(e)}"}, 500

    @app.route('/pix_copiaecola/<int:pedido_id>')
    def gerar_pix_copiaecola(pedido_id):
        pedido = Pedidos.query.get(pedido_id)
        if not pedido:
            return {"erro": "Pedido não encontrado"}, 404

        if pedido.forma_pagamento.lower() != 'pix':
            return {"erro": "A forma de pagamento do pedido não é Pix"}, 400

        try:
            chave_pix = 'jacksonduardo6@gmail.com'
            nome_recebedor = 'Lanchonete Meireles'
            cidade = 'EWBANK'
            valor = float(str(pedido.valor_total).replace(',', '.'))
            txid = f"PED{pedido.id:06d}"

            payload = gerar_payload_pix(
                chave=chave_pix,
                nome=nome_recebedor,
                cidade=cidade,
                valor=valor,
                txid=txid
            )

            return jsonify({"pix": payload})

        except Exception as e:
            return {"erro": f"Erro ao gerar código Pix: {str(e)}"}, 500
