function CheckColors(val){
  var element2=document.getElementById('salario');
  var element3=document.getElementById('salario2');
  if(val=="1"){
    element2.disabled = false;
    element3.disabled = false;
  }else if(val=="2"){
    element2.disabled = false;
    element3.disabled = false;
  }else if(val=="3"){
    element2.disabled = true;
    element3.disabled = true;
  }
}


function grafico(){
  document.getElementById('mostrar1').style.display="block";
  document.getElementById('mostrar2').style.display="none";
}

function boto(){
  document.getElementById('mostrar2').style.display="block";
  document.getElementById('mostrar1').style.display="none";
}

function abrir(){
  document.getElementById('vent').style.display="block";
  document.getElementById('vent2').style.display="block";
}

function cerrar(){
  document.getElementById('vent').style.display="none";
  document.getElementById('vent2').style.display="none";
}