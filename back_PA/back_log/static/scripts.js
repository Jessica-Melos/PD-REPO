/*Perfil*/

document.addEventListener("DOMContentLoaded", () => {
  const openModalButton = document.querySelector("#teste-modal");
  const closeModalButton = document.querySelector("#continue-popup"); 
  const modal = document.querySelector("#modal-selection");
  const overlay = document.querySelector("#overlay");
  const cursos = document.querySelector("#container");
  const lista_adc = document.querySelector("#lista-container");
  const logo_woman = document.querySelector("#logo_woman");
  const logo_perfil = document.querySelector("#logo_perfil");
  const balao_fala = document.querySelector("#balão_fala");
  const lista = document.querySelector("#colab-eleg");
  const horas = document.querySelector("#total-horas");
  
 

 
  // Abrir popup
  if (openModalButton) {
      openModalButton.addEventListener("click", () => {
          modal.classList.remove("hide");
          overlay.classList.remove("hide"); 
      });
  }

  if (closeModalButton) {
    closeModalButton.addEventListener("click", () => {

        if (modal){
          modal.remove();
        }
        if(overlay){
          overlay.classList.add("hide");
        }
        if (cursos){
           cursos.style.display = "block";
        }

        if(lista_adc){
          lista_adc.style.display = "block";
        }
        if (logo_woman) {
            logo_woman.style.display = "none"; 
        }
        if(logo_perfil){
            logo_perfil.style.display="block";
        }

        if(balao_fala){
            balao_fala.style.display="block";
        }

        if(lista){
            lista.style.display = "block";
        }
        if(horas){
            horas.style.display = "block";
        }
  
    modal.classList.add("hide");
    overlay.classList.add("hide");

      });
    }
});

let totalHoras = 0;
const NUMERO_LINHAS = 10; // Número fixo de linhas

function inicializarListaCursos() {
    let lista = document.getElementById("listaCursos");
    lista.innerHTML = ""; // Limpa a lista existente

    for (let i = 0; i < NUMERO_LINHAS; i++) {
        let divCurso = document.createElement("div");
        divCurso.classList.add("curso-item", "curso-item-oculto");
        divCurso.dataset.index = i; // Adiciona um índice para rastrear a linha

        let labelCurso = document.createElement("label");
        labelCurso.classList.add("curso-label");

        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.onchange = function() { tacharCurso(this); };

        let textoCurso = document.createTextNode(""); // Inicialmente vazio

        labelCurso.appendChild(checkbox);
        labelCurso.appendChild(textoCurso);

        divCurso.appendChild(labelCurso);
        lista.appendChild(divCurso);
    }
}


// Exemplo: chamar essa função sempre que o valor for atualizado
document.addEventListener("DOMContentLoaded", atualizarTextoCarga);

let cursosAdicionados = []; // Array para rastrear os cursos adicionados

function adicionarCurso() {
    let nomeCurso = document.getElementById("curso").value.toUpperCase();
    let cargaHoraria = parseInt(document.getElementById("carga").value);
   

    if (nomeCurso && cargaHoraria > 0) {

        let cursoJaExiste = cursosAdicionados.some(curso => curso.nome == nomeCurso);

        if (cursoJaExiste){
            exibirModalAviso("Este curso já foi adicionado");
            return; 
        }

        if (cursosAdicionados.length < NUMERO_LINHAS) {
            totalHoras += cargaHoraria;
            let lista = document.getElementById("listaCursos");

            // Criando a linha do curso dinamicamente
            let divCurso = document.createElement("div");
            divCurso.classList.add("curso-item");
            divCurso.dataset.index = cursosAdicionados.length;

            let labelCurso = document.createElement("label");
            labelCurso.classList.add("curso-label");

            let checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.classList.add("curso-checkbox"); // Adiciona uma classe para estilização
            checkbox.style.display = "inline-block"; // Garante que ele fique visível
            checkbox.onchange = function() { tacharCurso(this); };

            let nomeCursoMaiusculo = nomeCurso.toUpperCase();
            let textoCurso = document.createTextNode(` ${nomeCursoMaiusculo} - ${cargaHoraria}h`);

            labelCurso.appendChild(checkbox);
            labelCurso.appendChild(textoCurso);
            divCurso.appendChild(labelCurso);

            lista.appendChild(divCurso); // Adiciona o curso na lista
            



            // Adicionando ao array de cursos
            cursosAdicionados.push({
                index: cursosAdicionados.length,
                nome: nomeCursoMaiusculo,
                horas: cargaHoraria,
                tachado: false
            });

            document.getElementById("totalCarga").innerText = totalHoras;
            verificarLimite();
        } else {
            exibirModalAviso("Limite de cursos atingido.");
        }
    }
}



function encontrarLinhaVazia() {
    let lista = document.getElementById("listaCursos");
    let linhas = lista.querySelectorAll(".curso-item");
    for (let linha of linhas) {
        if (linha.querySelector(".curso-label").childNodes[1].textContent === "") {
            return linha;
        }
    }
    return null;
}

function tacharCurso(checkbox) {
    let label = checkbox.parentElement;
    let linha = label.parentElement;
    let index = parseInt(linha.dataset.index);

    let curso = cursosAdicionados.find(c => c.index === index);
    if (curso) {
        curso.tachado = checkbox.checked;
        if (checkbox.checked) {
            label.style.textDecoration = "line-through";
        } else {
            label.style.textDecoration = "none";
        }
    }
}

function removerCursosTachados() {
    let cursosParaRemover = cursosAdicionados.filter(c => c.tachado);


//Bloco adicionado
    if (cursosParaRemover.length === 0){
        exibirModalAviso("Por favor, selecione pelo menos um curso para remover.");
        return;
    }

    cursosParaRemover.forEach(curso => {
        let linha = document.querySelector(`.curso-item[data-index="${curso.index}"]`);
        if (linha) {
            linha.remove(); 
        }
    });

    // Mantém apenas os cursos que não foram tachados
    cursosAdicionados = cursosAdicionados.filter(c => !c.tachado);

    // Recalcula a carga horária
    totalHoras = cursosAdicionados.reduce((sum, c) => sum + c.horas, 0);
    document.getElementById("totalCarga").innerText = totalHoras;

    verificarLimite();
}


function atualizarTextoCarga (){

    let totalCarga = document.getElementById("totalCarga")
    let unidadeHoras = document.getElementById ("unidadeHoras");

    let valor = parseInt(totalCarga.textContent,10);
   
    if(!isNaN(valor)){
        unidadeHoras.textContent = (valor === 1) ? " hora": " horas";
    }else{
        console.error("Valor inválido em #totalCarga");
    }
    /*
    if (valor === 1) {
        totalCarga.nextSibling.nodeValue = " hora"; // Ajusta para "hora"
    } else {
        totalCarga.nextSibling.nodeValue = " horas"; // Ajusta para "horas"
    }
} else {
    console.error("Nó de texto não encontrado após #totalCarga");
}
} else {
    console.error("Valor inválido em #totalCarga");
}*/
}
function verificarLimite() {
    let botao = document.getElementById("btnConfirmar");
    let alerta = document.getElementById("alerta");
    let modalAviso = document.getElementById("modal-aviso");//
    let overlay = document.getElementById("overlay");//
    
    if (totalHoras > 30) {
        exibirModalAviso("Limite de 30h excedido! Exclua um curso ou entre em contato.");
        /*
        botao.classList.add("disabled");
        botao.disabled = true;
        alerta.style.display = "block";
        if(modalAviso && overlay){ //mudança
        overlay.classList.remove("hide");
        modalAviso.style.display = "flex"
        }//*/

    } else {
        botao.classList.remove("disabled");
        botao.disabled = false;
        alerta.style.display = "none";
        if (modalAviso && overlay){//mudança
            overlay.classList.add("hide");
            modalAviso.style.display = "none";
        }//
    }
}

function confirmarCriacao() {
    document.getElementById("popup").style.display = "block";
    overlay.classList.remove("hide");
}

function fecharPopup() {
    document.getElementById("popup").style.display = "none";
    overlay.classList.add("hide");
 
}



// Modal de aviso
const modalAviso = document.getElementById("modal-aviso");
const mensagemModal = document.getElementById("mensagemModal");
const btnFecharModal = document.getElementById("btnFecharModal");
const fecharModalSpan = document.querySelector("#modal-aviso .fechar-aviso");

function exibirModalAviso(mensagem) {
  mensagemModal.textContent = mensagem;
  modalAviso.style.display = "flex";
}

function fecharModalAviso() {
  modalAviso.style.display = "none";
}

btnFecharModal.onclick = fecharModalAviso;
fecharModalSpan.onclick = fecharModalAviso;

window.onclick = function(event) {
  if (event.target == modalAviso) {
    fecharModalAviso();
  }
};


function fecharModalAviso() {
  modalAviso.style.display = "none"
}

/*
closeModalButton.addEventListener("click", () => {
    modal.classList.add("hide");
    overlay.classList.add("hide");
    if (cursos) cursos.style.display = "block";
    if (lista_adc) lista_adc.style.display = "block";
    if (logo_woman) logo_woman.style.display = "none";
    if (logo_perfil) logo_perfil.style.display = "block";
    if (balao_fala) balao_fala.style.display = "block";
    if (botaoEditar) botaoEditar.style.display = "block";
});*/


btnFecharModal.onclick = fecharModalAviso;
fecharModalSpan.onclick = fecharModalAviso;

window.onclick = function(event) {
    if (event.target == modalAviso) {
        fecharModalAviso();
    }
};

// Finaliza Cadastro de Cursos
function finalizarCadastro() {
  exibirModalAviso("Parabéns, líder! Os Cursos foram cadastrados com sucesso! Em breve você poderá acompanhá-los no Plano de Aprendizagem de sua equipe!");
  document.getElementById("popup").style.display = "none";
  exibirListaCursos();

//Desabilitar o botão "Confirmar"
let botaoConfirmar = document.getElementById("btnConfirmar");
if(botaoConfirmar){
    botaoConfirmar.style.display ="none";
    }
}

let listaHabilitada = true;

function exibirListaCursos(){
    // Esconder todos os elementos da página, exceto a lista de cursos
    let elementosParaOcultar = document.querySelectorAll("#container, #modal-selection, #overlay, #logo_woman, #balão_fala, #logo_perfil, #btnRemoverTachados, #colab-eleg");
    elementosParaOcultar.forEach(elemento => {
        if (elemento) {
            elemento.style.display = "none";
        }
    });

    // Exibir apenas a lista de cursos adicionados
    let lista_adc = document.getElementById("lista-container");
    if (lista_adc) {
        lista_adc.style.display = "block";
        lista_adc.style.position = "absolute";
        lista_adc.style.left = "80%";
        lista_adc.style.width = "50vw";
        lista_adc.style.height = "440px";
  
      
       
        lista_adc.style.margin = "0"; 
       
    }

    // Ajustar o tamanho da lista para melhor visualização
    let listaCursos = document.getElementById("listaCursos");
    if (listaCursos) {
        listaCursos.style.display = "block";
        listaCursos.style.flexDirection = "column";
        listaCursos.style.position = "relative";
        listaCursos.style.height = "180px";
        listaCursos.style.width = "660px"; //Mudança
        listaCursos.style.fontSize = "17px";
        listaCursos.style.padding = "10px";
        listaCursos.style.border = "1px solid #eee"; //Mudança
        listaCursos.style.left = "-17%"; //Mudança
       

        
    let cursos = listaCursos.querySelectorAll (".curso-item");
    cursos.forEach(curso => curso.classList.add("curso-desabilitado"));
    
    }
// Exibe o botão "Editar"
let botaoEditar = document.getElementById("btnEditar");
if (botaoEditar) {
botaoEditar.style.display = "flex";
botaoEditar.style.position =  "fixed";
botaoEditar.style.top = "100px";
botaoEditar.style.left = "170%";
 
    }

let totalHoras = document.getElementById("total-horas");
if(totalHoras){
    totalHoras.style.position = "absolute";
    totalHoras.style.top = "520px";
    totalHoras.style.left = "50px";
    totalHoras.style.transform = "translateX(-17%)";
    totalHoras.style.bottom = "5px";
    totalHoras.style.color = "#cfcece"
}

    let cursos = listaCursos.querySelectorAll(".curso-item");
    cursos.forEach(curso => {
        let checkbox = curso.querySelector("input[type='checkbox']");
        let botaoExcluir = curso.querySelector(".botao-excluir");
    
        if (checkbox) {
            checkbox.disabled = true; // Desabilita o checkbox
            checkbox.style.display = "none"; // Oculta o checkbox
        }
        if (botaoExcluir) {
            botaoExcluir.style.display = "none"; // Oculta o botão de exclusão
        }
    });
    

}


function voltarParaTelaInicial() {
    // Exibe os elementos ocultos anteriormente
    let elementosParaExibir = document.querySelectorAll("#container, #balão_fala, #logo_perfil");
    elementosParaExibir.forEach(elemento => {
        if (elemento) {
            elemento.style.display = "block";
        }
    });

    let modal = document.getElementById("modal-selection");
    if (modal) {
        modal.style.display = "block";
    }

    let overlay = document.getElementById("overlay");
    if (overlay) {
        overlay.style.display = "block";
    }

    let listaCursos = document.getElementById("listaCursos");
    if (listaCursos) {
        let cursos = listaCursos.querySelectorAll(".curso-item");
        cursos.forEach(curso => curso.classList.remove("curso-desabilitado"));
    }

    


    inicializarListaCursos();
    cursosAdicionados = [];
    totalHoras = 0;
    document.getElementById("totalCarga").innerText = totalHoras;

    // Oculta a lista de cursos e o botão "Editar"
    let lista_adc = document.getElementById("lista-container");
    if (lista_adc) {
        lista_adc.style.display = "block";
        lista_adc.style.width = "30vw";
        lista_adc.style.margin = "140px auto";
        lista_adc.style.position = "absolute";
    }

    let botaoEditar = document.getElementById("btnEditar");
    if (botaoEditar) {
        botaoEditar.style.display = "none";
    }

    // Exibe o botão "Confirmar" novamente
    let botaoConfirmar = document.getElementById("btnConfirmar");
    if (botaoConfirmar) {
        botaoConfirmar.style.display = "block";
    }
}


//Saudação
function saudacao() {
    const agora = new Date();
    const diaSemana = agora.toLocaleDateString("pt-BR", { weekday: "long" });
    const dia = agora.getDate();
    const mes = agora.toLocaleDateString("pt-BR", { month: "long" });
    const ano = agora.getFullYear();
    const hora = agora.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  
    let saudacao;
    const horaAtual = agora.getHours();
  
    if (horaAtual >= 6 && horaAtual < 12) {
      saudacao = "Bom dia!";
    } else if (horaAtual >= 12 && horaAtual < 18) {
      saudacao = "Boa tarde!";
    } else {
      saudacao = "Boa noite!";
    }
  
    const mensagem = `<b>${saudacao}</b> Hoje é ${diaSemana}, ${dia} de ${mes} de ${ano}, e agora são ${hora}.`;
    document.getElementById("saudacao").innerHTML = mensagem;
  }
  
  saudacao();