function onData(event){
    
    Streamlit.setFrameHeight(document.documentElement.clientHeight);


    button.addEventListener("click", function(event) {
        //modal_inicial.style.display = "none";

        //Streamlit.setComponentValue("True")
    })

}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onData)
Streamlit.setComponentReady();