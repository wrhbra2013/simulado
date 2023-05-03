let btnShow = document.querySelector('button');
let result = document.getElementById('resultado');

btnShow.addEventListener('click',()=>{
    let selected = document.querySelector('input[type="radio"]:checked');
    result.innerHTML = selected.value;
})

