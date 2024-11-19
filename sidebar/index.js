let gArrayAliments = []
let gArrayHabitatge = [];
let gArrayOci = [];
let gArrayTransport = [];
let gHabitatgeComprat = [];
let gTransportComprat = [];
let gHabitatgeBlock = [];
let economiaJugador = "";
let accionsJugador = "";

function onData(event){
    const data = event.detail;
    const aDic = data.args.aDic;
    const aAliments = data.args.aAliments;
    const aHabitatge = data.args.aHabitatge;
    const aOci = data.args.aOci;
    const aTransport = data.args.aTransport;
    console.log(data.args)

    if(aDic){
        gArrayAliments = [];
        gArrayHabitatge = [];
        gArrayOci = [];
        gArrayTransport = [];

        gArrayAliments = aAliments;
        gArrayHabitatge = aHabitatge;
        gArrayOci = aOci;
        gArrayTransport = aTransport;
        gHabitatgeComprat = data.args.aHabitatgeComprat;
        gTransportComprat = data.args.aTransportComprat;
        gHabitatgeBlock = data.args.aHabitatgeBlock;

        // Passem la informació a JSON
        informacio_Jugador = JSON.parse(data.args.aDic);

        // Obtenim els identificadors dels contenidors
        let jugadorElement = document.getElementById("customSidebar_nom_jugador");
        let partidaElement = document.getElementById("customSidebar_nom_partida");
        let rondaElement = document.getElementById("customSidebar_ronda");
        let salariElement = document.getElementById("customSidebar_salari_net");
        let ecnomoniaElement = document.getElementById("customSidebar_economia_total");
        let despesesElement = document.getElementById("customSidebar_despese_fixes");
        let temps = document.getElementById("customSidebar_temps");

        //Obtenim la ronda i la informació pels gràfics
        let dataRondes = JSON.parse(informacio_Jugador["Ronda"])
        let dataSalut =  JSON.parse(informacio_Jugador["Salut"])
        let dataEconomia =  JSON.parse(informacio_Jugador["Economia"])

        // Actualitzem la informació 
        jugadorElement.innerHTML = informacio_Jugador["Nom_jugador"];
        partidaElement.innerHTML = informacio_Jugador["Nom_partida"];
        rondaElement.innerHTML = "Ronda " + informacio_Jugador["Ronda_actual"];
        salariElement.innerHTML = parseFloat(informacio_Jugador["Salari"]).toFixed(2) + " €";
        ecnomoniaElement.innerHTML = parseFloat(informacio_Jugador["EconomiaTotal"]).toFixed(2)  + " €";
        despesesElement.innerHTML = parseFloat(informacio_Jugador["Despesa"]).toFixed(2) + " €";;
        temps.innerHTML = informacio_Jugador["Temps"];
        economiaJugador = parseFloat(informacio_Jugador["EconomiaTotal"]).toFixed(2);
        accionsJugador = parseFloat(informacio_Jugador["Temps"])

        // Creem els gràfics
        updateChartSalut("salut-chart",  dataRondes, dataSalut)
        updateChartEconomia("economia-chart",  dataRondes, dataEconomia)
        updateChartNecessitats("necessitats-chart", informacio_Jugador["Necessitats_habitatge"],informacio_Jugador["Necessitats_transport"])
        updateAliments("aliments-chart", informacio_Jugador["Aliments"], 1)
    }

    Streamlit.setFrameHeight(document.documentElement.clientHeight);


    document.getElementById("customModal__closeButton").addEventListener("click", function(event) {
        cleanModal();
    });
}






Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onData)
Streamlit.setComponentReady();

