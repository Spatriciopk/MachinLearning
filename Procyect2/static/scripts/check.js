var tit = document.getElementById("tit");
var key = document.getElementById("key");
var asb = document.getElementById("asb");
var iden = document.getElementById("iden");
var checkbox = document.getElementById('cbox1');
checkbox.addEventListener("change", validaCheckbox, false);
function validaCheckbox()
{
  var checked = checkbox.checked;
  if(checked){
    var els = document.querySelectorAll(".tit");
    for (var x = 0; x < els.length; x++)
        els[x].style.display = '';  
        
  }
  else{
    var els = document.querySelectorAll(".tit");
    for (var x = 0; x < els.length; x++)
        els[x].style.display = 'none'; 
  }
}

var checkbox1 = document.getElementById('cbox2');
checkbox1.addEventListener("change", validaCheckbox1, false);
function validaCheckbox1()
{
  var checked1 = checkbox1.checked;
  if(checked1){
    var els = document.querySelectorAll(".key");
    for (var x = 0; x < els.length; x++)
        els[x].style.display = '';  
    
  }
  else{
    var els = document.querySelectorAll(".key");
    for (var x = 0; x < els.length; x++)
        els[x].style.display = 'none';
  }
}

var checkbox2 = document.getElementById('cbox3');
checkbox2.addEventListener("change", validaCheckbox2, false);
function validaCheckbox2()
{
  var checked2 = checkbox2.checked;
  if(checked2){
    var els = document.querySelectorAll(".asb");
    for (var x = 0; x < els.length; x++)
        els[x].style.display = '';  
    
  }
  else{
    var els = document.querySelectorAll(".asb");
    for (var x = 0; x < els.length; x++)
        els[x].style.display = 'none';
  }
}
 

