<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  

<!-- LIBRERÍA BOOSTRAP -->
    

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>


<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css"> 
<!-- Estilos -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/Estilos.css' ) }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/Estilo_botones.css' ) }}">
<!-- Script --> 
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script> 

<!-- Tipo de letra -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kanit&display=swap" rel="stylesheet"> 
<!-- <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@200&display=swap" rel="stylesheet"> -->



<!-- <link  href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<link  href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min.js" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<link  href="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<link  href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
 -->

 


    <title>Machine Learning</title>
</head>

    <nav class="navbar navbar-expand-lg navbar-Info bg-color">
        <div class="container-fluid">           
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavInfoDropdown" aria-controls="navbarNavInfoDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavInfoDropdown">
                    <ul class="navbar-nav"> 
                        <a class="navbar-brand" href="{{ url_for('principal')}}">INDEX</a>
                        <a class="navbar-brand" href="{{ url_for('consulta')}}" >CONSULTA</a> 
                        <a class="navbar-brand" href="{{ url_for('original')}}">DATASET ORIGINAL</a> 
                        <a class="navbar-brand" href="{{ url_for('demencia')}}">SUBIR DATASET</a> 
                    </ul>
                </div>
        </div>
    </nav>
    <body>    
 
    <h1>DESCRIPTION OF THE PROJECT</h1> 
 
    <div> 
        <div class="cards">
            <div class="card1"> 
                RESUMEN
                <br>
                El presente documento presentará una página web, donde se obtendrán diferentes conceptos de 
                demencia al ingresar estos conceptos se indicará a que se orienta, en este caso existen tres
                 tipos de orientaciones las cuales son las siguientes: biomédica, psicosocial-comunitaria y cotidiana. ; el usuario ingresa un concepto y este indicará que término es similar, además indicará el nivel de similitud entre la entrada y las taxonomías. Mediante el Jaccard y el coseno vectorial. Para que este sistema funcione correctamente se ha probado con definiciones externas de diferentes textos científicos, esto se hizo para que la herramienta funcione correctamente. La interfaz es amigable, muy intuitiva y fácil de navegar, ya que fue diseñada para todo tipo de usuarios.    
            </div>
            <div class="card2"> 
                INTRODUCCIÓN 
                <br>
                El problema se debe a que en los últimos años ha existido niveles altos de demencia, por lo cual es bueno saber sobre lo que opinan los médicos y personas
comunes, y saber su definición a que se encuentra orientada, la demencia no es una enfermedad específica, sino un grupo de trastornos caracterizados por el
deterioro de, al menos, dos funciones cerebrales, como la memoria y la razón. Los síntomas incluyen olvidos, aptitudes sociales restringidas y razonamiento tan
limitado que interfiere en las actividades diarias. Los medicamentos y la terapia pueden ayudar a controlar los síntomas. Algunas causas son reversibles.
            </div> 
        </div>
    </div>


   </div>
</div> 
 

    <div class="sticky-container">
        <ul class="sticky">
            <li>
            <i class="bi bi-github"></i>
                <a href="https://github.com/Freddy8-C/MachineLearning_Proyecto" target="_blank">Repositorio<br>Project </a> 
            </li>
            <li>
            <i class="bi bi-git"></i>
               <a href="https://github.com/Freddy8-C/Proyecto_MachineLearning2" target="_blank">Repositorio<br>CSV </a>
            </li>

            <li>
            <i class="bi bi-globe"></i>
                <a href="https://demencia.herokuapp.com/" target="_blank">Página web<br>en heroku</a>
            </li> 

            <li>
                <img src="{{ url_for('static', filename='img/Flask.png')}}" width="25" height="25">
                <a href="https://flask.palletsprojects.com/en/2.1.x/installation/" target="_blank">Página web<br>Flask</a>
            </li>

            <li>
                <img src="{{ url_for('static', filename='img/Heroku.png')}}" width="25" height="25">
                <a href="https://www.heroku.com/" target="_blank">Página web<br>Heroku</a>
            </li>
            <li>
                <img src="{{ url_for('static', filename='img/VisualSC.png')}}" width="25" height="25">
                <a href="https://code.visualstudio.com/" target="_blank"> Visual<br>Studio Code</a>
            </li>
        </ul>
    </div>  
 
</body> 


<footer>
<p>
    <br>
Elaborado por: Patricio Cadena - Freddy Camacho - Saskia Guerrero - Jefferson Sandoval <br> Estudiantes de la Universidad Politécnica Salesiana.
<br> Carrera Ingeniería en Ciencias de la Computación
</p>
</footer>

</html>