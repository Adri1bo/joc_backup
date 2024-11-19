function onData(event){
    const modal_inicial = document.getElementById("economiaModal");
    const data = event.detail;
    const jugador = data.args.aJugador;

    if(jugador){
        string = JSON.parse(jugador);
        document.getElementById("modalEconomia__salari").innerHTML = string["Salari"];
        document.getElementById("modalEconomia__despeses").innerHTML = string["Despesa"];
    }

    Streamlit.setFrameHeight(document.documentElement.clientHeight);


}

function closeEconomiaModal(){
    const modal_economia = document.getElementById("economiaModal");
    modal_economia.style.display = "none";

    Streamlit.setComponentValue("True")
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onData)
Streamlit.setComponentReady();