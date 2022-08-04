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
<!-- SCRIPT -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script> 
<!-- Tipo de letra -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kanit&display=swap" rel="stylesheet">


<title>QUERY</title>
</head> 
    <nav class="navbar navbar-expand-lg navbar-Info bg-color">
        <div class="container-fluid"> 
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavInfoDropdown" aria-controls="navbarNavInfoDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
            <div class="collapse navbar-collapse" id="navbarNavInfoDropdown">
                <ul class="navbar-nav">
                <ul class="navbar-nav"> 
                <a class="navbar-brand" href="{{ url_for('principal')}}">INDEX</a>
                        <a class="navbar-brand" href="{{ url_for('consulta')}}" >CONSULTA</a> 
                        <a class="navbar-brand" href="{{ url_for('original')}}">DATASET ORIGINAL</a> 
                        <a class="navbar-brand" href="{{ url_for('demencia')}}">SUBIR DATASET</a> 
                    </ul>
                </ul>
            </div>
        </div>
    </nav>

    <body> 
 <div  class="auron">
 <img src="{{ url_for('static', filename='img/crazy-auron.gif' ) }}" alt="Demencia" />
 </div>
<form action="" method="post" style="text-align: center;"> 
        <h1>INGRESE TU DEFINICIÓN DE DEMENCIA</h1>
        <textarea name="consulta" id="consulta" cols="100" rows="8"  placeholder="Describe tu definición aquí..." style="resize:none;"></textarea> 
        <br>
        <input type="submit" id="send-signup" class="btn btn-dark" name="signup" value="ENVIAR" />
        <!-- <input type="reset" id="send-rest" class="btn btn-dark" name="rest" value="RESTABLECER" /> -->
    </form>
<br>  
        
    

    
    
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



    
    <div class="tabla2" id="cont">
        <table >
            <tr>
                <th  class="td_h" colspan="2" >
                    SIMILITUD CON JACCARD
                </th>
            </tr>
            <tr>
            {% for i in range (2) %}
                {% if i == 0%}
                <td>
                  ENFOQUE
                  </td>
                  {% else %}
                  <td>
                  DOCUMENTO
                  </td>
                {%endif%}
               
                {% endfor %}
            </tr>
            {% for i in range(tam_enfoque) %}
            <tr>
           
                <td>
                    {{bolsa_enfoque[i]}} 
                </td>
                <td>
                    {{matriz_jaccard[i]}} %
                </td>
            
            </tr>
            {% endfor %}
           
    </table>
    <table >
            <tr>
                <th  class="td_h" colspan="2" >
                    SIMILITUD CON COSENO VECTORIAl
                </th>
            </tr>
            <tr>
            {% for i in range (2) %}
                {% if i == 0%}
                <td>
                  ENFOQUE
                  </td>
                  {% else %}
                  <td>
                  DOCUMENTO 
                  </td>
                {%endif%}
               
                {% endfor %}
            </tr>
            {% for i in range(tam_enfoque) %}
            <tr>
           
                <td>
                    {{bolsa_enfoque[i]}} 
                </td>
                <td>
                    {{lista_tf_idf[i]}} %
                </td>
            
            </tr>
            {% endfor %}
           
    </table>
    </div>
   



    </body>


    <footer>
<p>
    <br> 
Elaborado por: Patricio Cadena - Freddy Camacho - Saskia Guerrero - Jefferson Sandoval <br> Estudiantes de la Universidad Politécnica Salesiana.
</p>
</footer>

</html>