// var obtener=document.querySelectorAll(".script");
// for (var x = 0; x < obtener.length; x++)
//         obtener[x].addEventListener("click");


// for (var x = 0; x < obtener.length; x++)

// obtener[x].addEventListener;   



document.querySelectorAll(".script").forEach(el => {
    el.addEventListener("click", e => {
      var id = e.target.getAttribute("id");
    //   id=id.slice(1)
    //   id=id.slice(id.lenght)
    id=id.replace(new RegExp("\\(", 'g'), '');
    id=id.replace(new RegExp("\\)", 'g'), '');
    console.log(id);  
    var dato= id.split(",");
      var valor= document.getElementById('Resultado');
      var fila=dato[0];
      var columna=dato[1];
      
      fila=parseInt(fila)+1;
      columna=parseInt(columna)+1; 
      valor.textContent = "Similarity between the documents [Document "+fila+" and Document "+columna+"]  is of: "+dato[2];
       
    });
  });
        
 