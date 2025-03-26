function filtrarProdutos() {
    let input = document.getElementById("filtro");
    let filtro = input.value.toLowerCase();
    let tabela = document.querySelector("tbody");
    let linhas = tabela.getElementsByTagName("tr");

    for (let i = 0; i < linhas.length; i++) {
        let colunaNome = linhas[i].getElementsByTagName("td")[1]; // Coluna "Descrição"

        if (colunaNome) {
            let texto = colunaNome.textContent || colunaNome.innerText;
            if (texto.toLowerCase().indexOf(filtro) > -1) {
                linhas[i].style.display = "";
            } else {
                linhas[i].style.display = "none";
            }
        }
    }
}