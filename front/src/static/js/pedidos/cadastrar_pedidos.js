
document.addEventListener("DOMContentLoaded", () => {
    const resumoCliente = document.getElementById('resumo-cliente');
    const resumoItens = document.getElementById('resumo-itens');
    const resumoTotal = document.getElementById('resumo-total');
    const clienteNomeInput = document.getElementById('cliente_nome');

    // Inicializa a variável global
    itensContainer = document.getElementById('itens');

    clienteNomeInput.addEventListener('input', () => {
        resumoCliente.textContent = clienteNomeInput.value || '-';
    });

    // Inicializa o resumo ao carregar a página
    updateResumo();
});

function updateResumo() {
    const resumoItens = document.getElementById('resumo-itens');
    const resumoTotal = document.getElementById('resumo-total');

    const itens = document.querySelectorAll('.produto-item');
    resumoItens.innerHTML = '';
    let total = 0;

    itens.forEach((item) => {
        const produtoSelect = item.querySelector('select');
        const quantidadeInput = item.querySelector('input[type="number"]');
        const valor = parseFloat(produtoSelect.options[produtoSelect.selectedIndex].dataset.valor || 0);
        const quantidade = parseInt(quantidadeInput.value || 0);

        if (quantidade > 0) {
            const subtotal = valor * quantidade;
            total += subtotal;

            const listItem = document.createElement('li');
            
            // Nome do Produto
            const nomeProduto = document.createElement('span');
            nomeProduto.classList.add('produto-nome');
            nomeProduto.textContent = produtoSelect.options[produtoSelect.selectedIndex].textContent.split(' - ')[0];

            // Detalhes (Valor, Quantidade, Subtotal)
            const detalhesProduto = document.createElement('div');
            detalhesProduto.classList.add('produto-detalhes');
            detalhesProduto.innerHTML = `
                <strong>Valor Unitário: R$ ${valor.toFixed(2)}  
                <strong>QTDE:</strong> ${quantidade}  <br>
               <strong>Subtotal:</strong> R$ ${subtotal.toFixed(2)}
            `;

            listItem.appendChild(nomeProduto);
            listItem.appendChild(detalhesProduto);
            resumoItens.appendChild(listItem);
        }
    });

    resumoTotal.textContent = ` ${total.toFixed(2)}`;

    if (!resumoItens.children.length) {
        resumoItens.innerHTML = '<li>Nenhum item adicionado ainda</li>';
    }
}

function addProduto() {
    const index = itensContainer.children.length;
    const div = document.createElement('div');
    div.classList.add('produto-item');

    const select = document.createElement('select');
    select.name = `itens[${index}][produto]`;
    select.required = true;
    select.onchange = updateResumo;

    produtos.forEach((produto) => {
        const option = document.createElement('option');
        option.value = produto.id;
        option.textContent = `${produto.nome} - R$ ${produto.valor}`;
        option.dataset.valor = produto.valor;
        select.appendChild(option);
    });

    const inputQuantidade = document.createElement('input');
    inputQuantidade.type = 'number';
    inputQuantidade.name = `itens[${index}][quantidade]`;
    inputQuantidade.min = 1;
    inputQuantidade.id = 'qtdeinput'
    inputQuantidade.placeholder = 'Quantidade';
    inputQuantidade.required = true;
    inputQuantidade.oninput = updateResumo;

    const buttonRemover = document.createElement('button');
    buttonRemover.type = 'button';
    buttonRemover.textContent = 'X';
    buttonRemover.id="deletebtn"
    buttonRemover.onclick = () => {
        div.remove();
        updateResumo();
    };

    div.appendChild(select);
    div.appendChild(inputQuantidade);
    div.appendChild(buttonRemover);
    itensContainer.appendChild(div);

    updateResumo();
}

function removeProduto(button) {
    button.parentElement.remove();
    updateResumo();
}
