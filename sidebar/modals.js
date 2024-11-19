let arrayProductesSeleccionats = [];
let preuTotal = 0;
let accionsTotals = 0;
let modalTipusProducte = "";

/**
 * 
 * @param {*} this 
 */
function openModal(aIdProducte){
    document.getElementById("customModal__preuTotal").innerHTML = "Total compra: - "
    document.getElementById("customModal__accionsTotals").innerHTML = "Total temps: - "
    document.getElementById("customModal__comprarButton").disabled = true;
    preuTotal = 0;
    accionsTotals = 0;

    let idElement = aIdProducte.id;
    let substringIdElement = idElement.split("_");
    let tipusProducte = substringIdElement[1];

    let modal = document.getElementById("customModal");
    let container = document.getElementById("containerModal");
    let productesModal = document.getElementById("productes_modal");
    let stringProductes = "";

    modalTipusProducte = ""
    modalTipusProducte = tipusProducte;
    modal.style.display = "block";
    container.style.display = "block";

    let arrayProductes = getTipusProductes(tipusProducte)    

    stringProductes = crearCardsProductes(arrayProductes)
    productesModal.innerHTML = stringProductes;
}


function getTipusProductes(aTipusProducte){
    tipusColumnes = [];
    switch (aTipusProducte) {
        case "aliments":
            tipusColumnes = [{"Tipus":"Temps", "Icona": "clock"},{"Tipus":"Aliments", "Icona": "apple-whole"},{"Tipus":"Salut", "Icona":"heart"},{"Tipus":"Contaminació", "Icona":"smog"}]
            return gArrayAliments;
            break;

        case "habitatge":
            tipusColumnes = [{"Tipus":"Necessitats_habitatge", "Icona":"house"},{"Tipus":"Contaminació", "Icona":"smog"},{"Tipus":"Energia", "Icona":"bolt"}]
            return gArrayHabitatge;
            break;
            
        case "oci":
            tipusColumnes = [{"Tipus":"Temps", "Icona": "clock"},{"Tipus":"Salut", "Icona":"heart"},{"Tipus":"Contaminació", "Icona":"smog"}]
            return gArrayOci;
            break;

        case "transport":
            tipusColumnes = [{"Tipus":"Necessitats_transport", "Icona":"car-side"},{"Tipus":"Contaminació", "Icona":"smog"},{"Tipus":"Energia", "Icona":"bolt"}]
            return gArrayTransport;
            break;

        default:
            break;
    }
}

function getInfoProductesCard(aProducte, aJsonProducte){
    divString = "";

    aJsonProducte.forEach(element => {
        divString += '<div class="col-6" style="margin-top: 4px;margin-bottom:4px; color:#7a7a7a"><i style="font-size: 0.8rem;" class="fa-solid fa-'+element['Icona']+'"></i> '+aProducte[element['Tipus']]+'</div>';
    });

    return divString;
}


function crearCardsProductes(aArrayProductes){
    let productes = "";

    aArrayProductes.forEach(function(element) {
        let divProducte = "";
        let producteComprat = "";
        let nomProducte = element["Nom"];

        producteComprat = isProducteComprat(modalTipusProducte, nomProducte);
        divProducte = getInfoProductesCard(element, tipusColumnes);

        productes  +=
        '<div class="col-12 col-md-6 col-lg-2" style="padding-top: 8px; padding-bottom: 8px;">'+
            '<div class="card" data-producte="'+element["Nom"]+'">'+
                '<div class="card-body">'+
                    '<div class="row">'+
                        '<div class="col-12">'+
                            '<div style="display:flex; background-color: #F0FFFF; height: 150px;"><img style="width: 100px; margin: auto;" src="./img/icons/'+element["nom_"]+'.png" alt="'+element["Nom"]+'"></div>'+
                        '</div>'+
                    '</div>'+
                    '<div class="row" style="margin-top: 16px;">'+
                        '<div class="col-12"><h4 style="font-size: 1rem; line-height: 1.4rem; height: 2.8rem; overflow:hidden;">'+element["Nom"]+'</h4></div>'+divProducte+
                    '</div>'+
                    '<div class="row" style="margin-top: 16px;">'+
                        '<div class="col">'+
                            '<div style="border-radius: 5px;text-align: left; font-weight: bold; font-size: 1.2rem">'+element["Preu"]+'€</div>'+
                        '</div>'+
                        '<div class="col-auto my-auto">'+producteComprat+
                        '</div>'+
                    '</div>'+
                '</div>'+
            '</div>'+
        '</div>'
    });

    return productes;
}


/**
 * Funció que passat el nom d'un producte, obté el preu de l'array d'aliments
 * @param {String} aNomProducte 
 * @returns 
 */
function obtenirPreu(aNomProducte){
    let arrayProductes = getTipusProductes(modalTipusProducte);

    for (let index = 0; index < arrayProductes.length; index++) {
        const element = arrayProductes[index];
        
        if(element.Nom === aNomProducte){
            return { Preu: element.Preu, Producte: element, Accions: element.Temps };
        }  
    }
}

function isProducteComprat(aCategoriaProducte, aNom){
    
    let isB = '<div class="customCards__addButton" onclick="cardSeleccionada(this)">AFEGIR</div>';

    if(aCategoriaProducte === "habitatge"){
        gHabitatgeComprat.forEach(element => {
            
            if(element === aNom){
                isB = '<div class="" style="color: green"><i class="fa-regular fa-circle-check"></i></div>';
            }
        });

        gHabitatgeBlock.forEach(element => {
            if(element === aNom){
                isB = '<div class="" style="color: red"><i class="fa-regular fa-circle-xmark"></i></i></div>';
            }
        });
    }

    if(aCategoriaProducte === "transport"){
        gTransportComprat.forEach(element => {
            
            if(element === aNom){
                isB = '<div class="" style="color: green"><i class="fa-regular fa-circle-check"></i></div>';
            }
        });
    }

    return isB;
}


/**
 * Funció que s'executa quan cliquem al botó "Afegir" d'una card
 * @param {ElementDOM} aButton 
 */
function cardSeleccionada(aButton){
    // Obtenim el contenidor pare (card) del botó seleccionat
    let card = aButton.closest(".card")
    // Obtenim el contenidor on hi posarem el preu total
    let divPreuTotal = document.getElementById("customModal__preuTotal");
    let divAccionsTotals = document.getElementById("customModal__accionsTotals");
    let diners = "";
    let accions = "";
    let elementDiners = "";
    let elementAccions = "";
    let dictPreuIAccions = "";

    // Utilitzem toggle per alternar dos estats: si el contenidor té la classe selected__card o no
    card.classList.toggle("selected__card")

    // Obtenim el preu total i les accions dels productes seleccionats
    dictPreuIAccions = obtenirPreuTotalAndArrayElementsSeleccionats();
    preuTotal = dictPreuIAccions["PreuTotal"];
    accionsTotals = dictPreuIAccions["AccionsTotals"];

    // Calculem si el jugador tindrà prous diners
    diners = parseFloat(economiaJugador - preuTotal).toFixed(2);
    accions = parseFloat(accionsJugador - accionsTotals).toFixed(2)
    let floatPreuTotal = parseFloat(preuTotal);
    let floatEconomiaJugador = parseFloat(economiaJugador);
    let floatAccionsTotals = parseFloat(accionsTotals)
    let floatAccionsJugador = parseFloat(accionsJugador)

    if(floatPreuTotal>floatEconomiaJugador){
        document.getElementById("customModal__comprarButton").disabled = true;
        elementDiners = '<span style="color: red">Total compra: '+preuTotal+'€ / Restant:'+diners+'€</span>';
    }
    else if(floatPreuTotal<floatEconomiaJugador){
        document.getElementById("customModal__comprarButton").disabled = false;
        elementDiners = '<span style="color: black">Total compra: '+preuTotal+'€ / Restant: '+diners+'€</span>';
    }

    if(floatAccionsTotals > floatAccionsJugador && accions < -0.5){
        document.getElementById("customModal__comprarButton").disabled = true;
        elementAccions = '<span style="color: red">Total temps: '+accionsTotals+' / Restant:'+accions+'</span>';
    }
    else if(floatAccionsTotals <= floatAccionsJugador || (floatAccionsTotals > floatAccionsJugador && accions >=-0.5)){
        document.getElementById("customModal__comprarButton").disabled = false;
        elementAccions = '<span style="color: black">Total temps: '+accionsTotals+' / Restant: '+accions+'</span>';
    }
  
    // Afegim el preu total al contenidor del preu
    divPreuTotal.innerHTML = elementDiners;
    divAccionsTotals.innerHTML = elementAccions;
}


function enviarProductes(){
    //console.log("Enviat");
    Streamlit.setComponentValue(arrayProductesSeleccionats);

    cleanModal();
}

function cleanModal(){
    let cardsSeleccionades = document.querySelectorAll(".selected__card");
    cardsSeleccionades.forEach(element => {
        element.classList.remove("selected__card");
    });

    document.getElementById("containerModal").style.display="none"
    arrayProductesSeleccionats = [];
    document.getElementById("customModal__preuTotal").innerHTML = "-";
}


/**
 * Funció que obté el preu total i l'element de l'array
 * @returns 
 */
function obtenirPreuTotalAndArrayElementsSeleccionats(){
    // Obtenim totes les cards seleccionades
    let productesSeleccionats = document.querySelectorAll(".selected__card");
    let total = 0;
    let totalAccions = 0;
    // Buidem l'array de productes
    arrayProductesSeleccionats = [];

    productesSeleccionats.forEach(element => {
        let nomProducte= element.getAttribute("data-producte");
        let resposta = [];
        let preu = 0;
        let accions = 0;

        // Obtenim el preu del producte i l'element dins de l'array de productes
        resposta = obtenirPreu(nomProducte)
        preu = resposta["Preu"]
        accions = resposta["Accions"]
        // Guardem l'element de l'array a un nou array amb tots els productes seleccionats
        arrayProductesSeleccionats.push(resposta["Producte"])
        // Sumem el preu i les accions dels productes seleccionats
        total += parseFloat(preu);
        totalAccions += parseFloat(accions);
    });

    // Arrodonim a dos decimals el preu total
    total = total.toFixed(2);
    return { "PreuTotal": total, "AccionsTotals": totalAccions};
}