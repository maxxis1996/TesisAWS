function CheckColors(val){
  var element=document.getElementById('numConsul');
  var element2=document.getElementById('salario');
  alert(val)
  if(val==1){
    element.style.display='block';
    element2.disabled = true;
    
  }else if(val=="2"){
    element.style.display='block';
    element2.disabled = true;
  }else if(val=="3"){
    element.style.display='block';
  }else{
    alert("holi")
  }
  alert("holi")
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