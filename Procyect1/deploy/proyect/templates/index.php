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



<!-- <link  href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<link  href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min.js" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<link  href="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<link  href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
 -->



<div class="logo">
    <img src="{{ url_for('static', filename='img/Logo.png' ) }}" alt="Logo Machine Learning" />
</div>


    <title>Machine Learning</title>
</head>
<body>
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
    
 
    <h1>DESCRIPTION OF THE PROJECT</h1>
<div id="abstract"> 
    <div id="abstract1">
In this website a comparative analysis of the similarity of three main documents will be carried out,
which are the following: social sciences, computer science, medicine, and exact sciences with their 
fifteen references, using three variables (title, summary and keywords). <br>
Once the database is made, we proceed to make the processes and analysis of the documents with the 
same topics, each document goes through the NLP process, to obtain a database ready to use, then the
 process of similarity between documents of the same type, distance matrix of documents, graphs to 
 indicate the distance matrix of the entire database and each document, also runs a clustering task 
 using the DHC algorithm with the purpose that each document must show some graph that identifies the 
 resulting articles and a list with the titles of the articles of each group. <br>
In this case, Visual Studio Code has been used, as it is an application that helps the creation of
 programs through Python, and the construction of the dataset was also made by the members of the group
  themselves, it contains different diagrams to have a better abstraction of the program and the project
   in general, to understand each of the implemented algorithms.
   </div>
</div> 



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


    <!-- <ul class="sticky-social-bar">
  <li class="social-icon">
    <a href="https://facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwal.ee%2F" target="_blank">
      <i class="bi bi-github" aria-hidden="true"></i>
      <span class="social-icon-text">Github Repository Project</span>
    </a>
  </li>
  <li class="social-icon">
    <a href="https://twitter.com/intent/tweet/?text=Super%20fast%20and%20easy%20Social%20Media%20Sharing%20Buttons.%20No%20JavaScript.%20No%20tracking.&amp;url=https%3A%2F%2Fwal.ee%2F" target="_blank">
      <i class="bi bi-git" aria-hidden="true"></i>
      <span class="social-icon-text">Github Repository CSV</span>
    </a>
  </li>
  <li class="social-icon">
    <a href="https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fwal.ee%2F&amp;media=https%3A%2F%2Fwal.ee%2F&amp;description=Super%20fast%20and%20easy%20Social%20Media%20Sharing%20Buttons.%20No%20JavaScript.%20No%20tracking." target="_blank">
    <img src="{{ url_for('static', filename='img/Heroku.png')}}" width="10" height="10">
      <span class="social-icon-text">Website Machine Learning </span>
    </a>
  </li>
  <li class="social-icon">
    <a href="https://t.me/share/url?url=https://wal.ee&amp;text=Walee - URL Shortener" target="_blank">
    <img src="{{ url_for('static', filename='img/Heroku.png')}}" width="10" height="10">
      <span class="social-icon-text">Website Flask</span>
    </a>
  </li>

  <li class="social-icon">
    <a href="https://t.me/share/url?url=https://wal.ee&amp;text=Walee - URL Shortener" target="_blank">
    <img src="{{ url_for('static', filename='img/Heroku.png')}}" width="10" height="10">
      <span class="social-icon-text">Website Visual Studio Code</span>
    </a>
  </li>

</ul> -->
 

</body>


<footer>
<p>
Elaborated by: Students of the Salesian Polytechnic University.
</p>
</footer>

</html>