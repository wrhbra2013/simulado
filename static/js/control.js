let btnShow = document.querySelector('#gabarito');
let result = document.getElementById('resultado');

btnShow.addEventListener('click',()=>{
    let selected = document.querySelector('input[type="radio"]:checked');
    result.innerHTML = selected.value;
})

const btn = document.querySelector('#btn');
btn.addEventListener('click', function list(){   
    //btn.value = innerHTML;
    btn.innerHTML = value();

})

