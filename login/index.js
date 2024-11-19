function onData(event){
    const login = document.getElementById("login_container");
    const button = document.getElementById("login_form_submitButton");
    togglePassword = document.getElementById("togglePassword");
    Streamlit.setFrameHeight(document.documentElement.clientHeight);


    button.addEventListener("click", function(event) {
        let nom_jugador = document.getElementById("login_form_input_namePlayer").value;
        let nom_partida = document.getElementById("login_form_input_nameGame").value;
        let codi = document.getElementById("login_form_input_password").value;

        let jsonObject = {
            "nom_jugador": nom_jugador,
            "nom_partida": nom_partida,
            "codi": codi
        };


        Streamlit.setComponentValue(jsonObject)

        login.style.display = "none";
    })
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onData)
Streamlit.setComponentReady();



