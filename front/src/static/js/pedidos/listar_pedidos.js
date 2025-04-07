async function abrirModal(pedidoId) {
    const modal = document.getElementById('detalhesModal');
    const detalhesDiv = document.getElementById('detalhesPedido');

    try {
        // Realizando a requisição para obter os detalhes do pedido
        const response = await fetch(`/api/pedido/${pedidoId}`);
        if (response.ok) {
            const pedido = await response.json();
            let trocoHtml = "";
            if (pedido.valor_entregue != pedido.valor_total) {
                const troco = (pedido.valor_entregue - pedido.valor_total).toFixed(2);
                trocoHtml = `<p><strong>Troco:</strong> R$ ${troco}</p>`;
            }
            // Montando o HTML com os dados do pedido
            let html = `
                <p><strong>ID do Pedido:</strong> ${pedido.id}</p>
                <p><strong>Cliente:</strong> ${pedido.cliente_nome}</p>
                <p><strong>Observação:</strong> ${pedido.observacao}</p>
                <p><strong>Endereço:</strong> ${pedido.endereco}</p>
                <p><strong>Valor Total:</strong> R$ ${parseFloat(pedido.valor_total).toFixed(2)}</p>
                <p><strong>Forma de pagamento</strong>  ${pedido.forma_pagamento}</p>
                ${trocoHtml} 
                <h4>Itens do Pedido:</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Produto</th>
                            <th>Quantidade</th>
                            <th>Valor Unitário</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            // Iterando sobre os itens para preencher a tabela
            for (const item of pedido.itens) {
                const produto = item.produto || {};
                html += `
                    <tr>
                        <td>${produto.nome || 'Produto não encontrado'}</td>
                        <td>${item.quantidade}</td>
                        <td>R$ ${produto.valor ? parseFloat(produto.valor).toFixed(2) : '0.00'}</td>
                        <td>R$ ${(produto.valor ? produto.valor * item.quantidade : 0).toFixed(2)}</td>
                    </tr>
                `;
            }

            html += `
                    </tbody>
                </table>
            `;

            // Exibindo os dados no modal
            detalhesDiv.innerHTML = html;
            modal.style.display = 'block';
        } else {
            // Exibindo mensagem de erro no modal
            detalhesDiv.innerHTML = `<p>Erro ao carregar os detalhes do pedido.</p>`;
            modal.style.display = 'block';
        }
    } catch (error) {
        // Exibindo mensagem de erro no modal
        detalhesDiv.innerHTML = `<p>Erro ao carregar os detalhes do pedido.</p>`;
        console.error('Erro ao buscar os detalhes do pedido:', error);
        modal.style.display = 'block';
    }
}

// Fechar o modal
function fecharModal() {
    const modal = document.getElementById('detalhesModal');
    modal.style.display = 'none';
} 
document.addEventListener("DOMContentLoaded", function () {
    function atualizarPedidos() {
        // Captura os valores dos filtros ativos
        const dataInicio = document.getElementById('data_inicio').value;
        const dataFim = document.getElementById('data_fim').value;
        const apenasNaoFinalizados = document.getElementById('entregues').checked ? 'on' : '';

        // Monta a URL da API com os filtros aplicados
        const url = `/api/pedidos?data_inicio=${dataInicio}&data_fim=${dataFim}&entregues=${apenasNaoFinalizados}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector("tbody");
                tbody.innerHTML = ""; // Limpa a tabela

                if (data.pedidos.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="6">Nenhum pedido encontrado.</td></tr>`;
                    return;
                }

                data.pedidos.forEach(pedido => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${pedido.id}</td>
                        <td>${pedido.cliente_nome}</td>
                        <td>R$ ${pedido.valor_total.toFixed(2)}</td>
                        <td>${pedido.criado_em}</td>
                        <td>
                            ${pedido.entregue == 1 ? '<span class="status amarelo"></span>' :
                              pedido.entregue == 2 ? '<span class="status verde"></span>' :
                              '<span class="status vermelho"></span>'}
                        </td>
                        <td>
                            <a href="/editar_pedido/${pedido.id}" class="btn"><i class="fa-solid fa-pen"></i></a>
                            <a class="btn" onclick="abrirModal('${pedido.id}')"><i class="fa-solid fa-eye"></i></a> 
                            <a href="/gerar_cupom/${pedido.id}" class="btn" onclick="return confirm('Gerar cupom?')"><i class="fa-solid fa-print"></i></a>
                            <a href="/confirmar_pedido/${pedido.id}" class="btn_green" onclick="return confirm('Tem certeza que deseja finalizar esse pedido?')"><i class="fa-solid fa-check"></i></a>
                            <a href="/deletar_pedido/${pedido.id}" class="btn btn-delete" onclick="return confirm('Tem certeza que deseja deletar este pedido?')" > <i class="fa-solid fa-trash"></i></a>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            })
            .catch(error => console.error("Erro ao buscar pedidos:", error));
    }

    // Atualiza a cada 5 segundos
    setInterval(atualizarPedidos, 5000);

    // Chamada inicial
    atualizarPedidos();
}); 
