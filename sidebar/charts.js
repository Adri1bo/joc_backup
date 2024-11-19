var layout = {
    height: 200,
    margin: {
        l: 30, r: 20, b: 20, t: 10
      },
};

var layout2 = {
  height: 200,
  margin: {
      l: 80, r: 20, b: 20, t: 10
    }
};

var jugador = "";

function getArrayJugador(aDic){
    jugador = aDic;
}

function updateChartSalut(aIdElement, aRondes, aSalut){

    var trace = {
        x: aRondes,
        y: aSalut,
        type: 'scatter',
        line: {
          color: '#5E74BD'
        }
    };

    let data = [trace]
    Plotly.newPlot(aIdElement, data, layout, {displayModeBar: false});

}

function updateChartEconomia(aIdElement, aRondes, aEconomia){
    var trace = {
        x: aRondes,
        y: aEconomia,
        type: 'scatter',
        line: {
          color: '#5E74BD'
        }
    };

    let data = [trace]
    Plotly.newPlot(aIdElement, data, layout, {displayModeBar: false});

}

function updateChartNecessitats(aIdElement, habitatge, transport){
    var trace = {
        x: [transport, habitatge],
        y: ['Transport', 'Habitatge'],
        marker:{
            color: [ '#868BC7','#413354']
        },
        orientation: 'h',
        type: 'bar'
    };

    let data = [trace]
    Plotly.newPlot(aIdElement, data, layout2, {displayModeBar: false});

}

function updateAliments(aIdElement, rebost, necessitatDia){
    var trace = {
        x: [necessitatDia, rebost],
        y: ['Necessitat diària', 'Rebost'],
        marker:{
            color: [ '#868BC7','#413354']
        },
        type: 'bar',
        orientation: 'h'
    };

    let data = [trace]
    Plotly.newPlot(aIdElement, data, layout2, {displayModeBar: false});

}




