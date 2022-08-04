


document.querySelectorAll(".form-check-input").forEach(el => {
  el.addEventListener("change", e => {
    var id = e.target.getAttribute("id");
    var d = document.querySelectorAll(".grupo"+id);
    for (var x = 0; x < d.length; x++)
         d[x].classList.toggle("mystyle");
    
  });
});