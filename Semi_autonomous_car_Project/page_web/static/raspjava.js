 var variable1 = 0 ;   //puissance droite
 var variable2 = 0 ;  // puissance gauche
 var variable3= "forward" //oreintation
 var auto=0  //0=manuel/1=auto

 /*ancienne version
function getPuissance() {
    var range = document.getElementById('PUISSANCE').value;
    console.log(range);
    variable1 = range ;
    envoyerDonnees();
    }
function getOrient() {
    var range1 = document.getElementById('ORIENTATION').value;
    console.log(range1);
    variable2 = range1;
    envoyerDonnees();
    }
*/

function a() {
    variable1 = 70;
    variable2 = 70;
    variable3= "forward";
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
    variable1 = 0;
    variable2 = 0;
    variable3= "forward";
    setTimeout(envoyerDonnees,400);

}
function ad() {
    variable1 = 40;
    variable2 = 70;
    variable3= "forward";
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
    variable1 = 0;
    variable2 = 0;
    variable3= "forward";
    setTimeout(envoyerDonnees,400);

}
function ag() {
    variable1 = 70;
    variable2 = 40;
    variable3= "forward";
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
    variable1 = 0;
    variable2 = 0;
    variable3= "forward";
    setTimeout(envoyerDonnees,400);
}   
function b() {
    variable1 = 70 ;
    variable2 = 70;
    variable3= "backward" ;
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
    variable1 = 0;
    variable2 = 0;
    variable3= "backward";
    setTimeout(envoyerDonnees,400);
}
function bg() {
    variable1 = 70 ;
    variable2 = 40;
    variable3= "backward" ;
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
    variable1 = 0;
    variable2 = 0;
    variable3= "backward";
    setTimeout(envoyerDonnees,400);
}

function vitesse() {
    variable1 = 100 ;
    variable2 = 100;
    variable3= "forward" ;
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
}

function bd() {
    variable1 = 40;
    variable2 = 70;
    variable3= "backward" ;
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
    variable1 = 0;
    variable2 = 0;
    variable3= "backward";
    setTimeout(envoyerDonnees,400);
}   

function Demg() {
    variable1 = 40;
    variable2 = 0;
    variable3= "forward";
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
    variable1 = 0;
    variable2 = 0;
    variable3= "forward";
    setTimeout(envoyerDonnees,2100);
}
function Demd() {
    variable1 = 0;
    variable2 = 40;
    variable3= "forward";
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();
    variable1 = 0;
    variable2 = 0;
    variable3= "forward";
    setTimeout(envoyerDonnees,2100);
}

function Mode_automatique() {
    variable1 = 0;
    variable2 = 0;
    variable3= "forward";
    if (auto > 0) {
        auto = 0;
      } else {
        auto = 1;
      }
    envoyerDonnees()
    }
    



function getSTOP() {
    variable1= 0;
    variable2 = 0; /*j'y crois moyen */
    variable3 = "forward"
    auto=0
    console.log(variable1);
    console.log(variable2);
    envoyerDonnees();}





function envoyerDonnees() { 
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/traiter_donnees/'+variable1+'+'+variable2+'+'+variable3+'+'+auto, true);
   
    xhr.onload = function () {
        if (xhr.status === 200) {
           console.log('Données envoyées avec succès !');
        }
    };  
    xhr.send(); 
    }
