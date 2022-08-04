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
    <!-- SCRIPTS -->
    <script src="{{url_for('static', filename='scripts/canvas_mds.js')}}"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script> 
    
    <div class="logo">
        <img src="{{ url_for('static', filename='img/Logo.png' ) }}" alt="Logo Machine Learning" />
    </div>
    
    <title>MDS</title>

</head> 
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('principal')}}">Index</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDarkDropdown" aria-controls="navbarNavDarkDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDarkDropdown">
        <ul class="navbar-nav"> 
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Papers
          </a>
          <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
            <li><a class="dropdown-item" href="/doc/1">All Papers</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="/doc/2">Social Sciences</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="/doc/3">Computing</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="/doc/4">Medicine</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="/doc/5">Exact Sciences</a></li>
          </ul>
        </li>
 

            <li class="nav-item dropdown"> 
                  <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Hear Map</a>
                  <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
                  <li><a class="dropdown-item" href="/dendo/1">Papers General</a></li>   
 
                  </ul>
                </li> 
                 
                
                <li class="nav-item dropdown"> 
                  <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  MDS</a>
                  <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
                    <li><a class="dropdown-item" href="/MDS/1">General</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="/MDS/2">Social Sciences</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="/MDS/3">Computing</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="/MDS/4">Medicine</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="/MDS/5">Exact Sciences</a></li>
                  </ul>
                </li>  
                
                
                <li class="nav-item dropdown"> 
                  <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Dendogram</a>
                  <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
                    <li><a  class="dropdown-item" href="/Cluster/1"> General</a></li>
                    <li> <a class="dropdown-item" href="/Cluster/2"> Social Sciences </a></li>
                    <li><a class="dropdown-item" href="/Cluster/3"> Computing </a></li>
                    <li><a class="dropdown-item" href="/Cluster/4"> Medicine </a></li>
                    <li><a class="dropdown-item" href="/Cluster/5"> Exact Sciences </a></li>
                  </ul>
                </li>
                <a class="navbar-brand" href="{{ url_for('schedule')}}">Schedule</a>  
        </ul>
        </div>
    </div>
    </nav>
<!-- <div class="container-img">
<img src="{{ url_for('static', filename='img/mds.png' ) }}" alt="MDS" class="tam_imagen"/>
</div>  -->
<body >
    <h1>METRIC MDS</h1>
    <form  action="" method="post"> 
    <select name="carlist" id="carlist"class="form-select" aria-label="Default select ">  <option value="euclidean">Euclidean</option>
<option value="precomputed">Precomputed</option>
</select>
<input type="submit" class="btn btn-dark" id="send-signup" name="signup" value="Enviar" />
 </form>  
    
 <img id="zoom_01" src="{{ url_for('static', filename='img/mds.png' ) }}" data-zoom-image="{{ url_for('static', filename='img/mds.png' ) }}"/>
    <script>
      $('#zoom_01').elevateZoom({
        cursor: "crosshair",  
        zoomWindowFadeIn: 5, 
        zoomWindowFadeOut: 5 
      }); 
    </script>


    <div class="sticky-container">
        <ul class="sticky">
            <li>
            <i class="bi bi-github"></i>
                <a href="https://github.com/Spatriciopk/Prueba" target="_blank">Repository<br>Project </a> 
            </li>
            <li>
            <i class="bi bi-git"></i>
               <a href="https://github.com/Freddy8-C/Proyecto_MachineLearning" target="_blank">Repository<br>CSV </a>
            </li>

            <li>
            <i class="bi bi-globe"></i>
                <a href="https://machinlearning2.herokuapp.com/" target="_blank">Website<br>Machine Learning</a>
            </li> 

            <li>
                <img src="{{ url_for('static', filename='img/Flask.png')}}" width="25" height="25">
                <a href="https://flask.palletsprojects.com/en/2.1.x/installation/" target="_blank">Website<br>Flask</a>
            </li>

            <li>
                <img src="{{ url_for('static', filename='img/Heroku.png')}}" width="25" height="25">
                <a href="https://www.heroku.com/" target="_blank">Website<br>Heroku</a>
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
Elaborated by: Students of the Salesian Polytechnic University.
</p>
</footer>

</html>