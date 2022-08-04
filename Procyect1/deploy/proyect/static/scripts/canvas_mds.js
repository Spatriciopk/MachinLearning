function draw(scale, translatePos) {
  var img = new Image();  
 var canvas = document.getElementById("myCanvas");
 var context = canvas.getContext("2d");
 img.src = '../static/img/mds.png'; 
 // clear canvas
 context.clearRect(0, 0, canvas.width, canvas.height);

 context.save();
 context.translate(translatePos.x, translatePos.y);
 context.scale(scale, scale);
 context.beginPath(); // begin custom shape 

 context.drawImage(img,10,-250,750,475)
 context.closePath();  

 context.lineWidth = 5;
 context.strokeStyle = "#0000ff";
 context.stroke();
 context.restore(); 
}

window.onload = function() {
 var canvas = document.getElementById("myCanvas");

 var translatePos = {
   x: 10,
   y: 250 
 };

 var scale = 1.0;
 var scaleMultiplier = 0.8;
 var startDragOffset = {};
 var mouseDown = false;

 // add button event listeners
 document.getElementById("plus").addEventListener("click", function() {
   scale /= scaleMultiplier;
   draw(scale, translatePos);
 }, false);

 document.getElementById("minus").addEventListener("click", function() {
   scale *= scaleMultiplier;
   draw(scale, translatePos);
 }, false);

 // add event listeners to handle screen drag
 canvas.addEventListener("mousedown", function(evt) {
   mouseDown = true;
   startDragOffset.x = evt.clientX - translatePos.x;
   startDragOffset.y = evt.clientY - translatePos.y;
 });

 canvas.addEventListener("mouseup", function(evt) {
   mouseDown = false;
 });

 canvas.addEventListener("mouseover", function(evt) {
   mouseDown = false;
 });

 canvas.addEventListener("mouseout", function(evt) {
   mouseDown = false;
 });

 canvas.addEventListener("mousemove", function(evt) {
   if (mouseDown) {
     translatePos.x = evt.clientX - startDragOffset.x;
     translatePos.y = evt.clientY - startDragOffset.y;
     draw(scale, translatePos);
   }
 });

 draw(scale, translatePos); 
};


// jQuery(document).ready(function() {
//   $("#wrapper").mouseover(function(e) {
//     $('#status').html(e.pageX + ', ' + e.pageY);
//   });
//  })


