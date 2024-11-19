function onData(event){
    const modal_inicial = document.getElementById("initialModal");
    const button = document.getElementById("initalModal__container__div__leftColumn__button");
    Streamlit.setFrameHeight(document.documentElement.clientHeight);


}

function closeModal(){
    const modal_inicial = document.getElementById("initialModal");
    modal_inicial.style.display = "none";

    Streamlit.setComponentValue("True")
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onData)
Streamlit.setComponentReady();