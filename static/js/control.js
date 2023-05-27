const btnShow = document.querySelector('#gabarito');
const result = document.getElementById('input_estudante');

btnShow.addEventListener('click',()=>{
    let selected = document.querySelector('input[type="radio"]:checked');
    result.innerHTML = selected.value;
})

const btn = document.querySelector('#btn');
btn.addEventListener('click', function list(){   
     btn.value = innerHTML;
    //btn.innerHTML = value();
  if (btn.style.display == "block") {
       btn.style.display == "none";    
  } else {
    btn.style.display == "block"    
  }


})


//Conferir valores
// provas = [];

// // 
// // if (confirm === True) {
//     function inserir(){     
//         //Incluir registro
//         let questao = window.document.getElementById('questao_id').value;
//         //Conferir envios
//         let questao_inserida = confere(questao);
//         //Testa condições
//         if (questao_inserida == null){
//             provas.push({id: questao});  
            
               
//         }else{
//             alert("Esta questão".concat(questao),"já foi enviada.")
//         }
           

//      }
// function confere(numero_id){
//     let ids = provas.find(function(q_id){
//         return q_id.id === numero_id });
//         return ids;
// }


    



