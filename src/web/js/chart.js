
let lineChart;

function renderChart(inputData) {
    const ctx = document.getElementById('myChart');

    temperature = inputData.map(element => {
        return {
            x: element.timestamp.substring(11),
            y: parseInt(element.temperature)
        }
    })

    // humidity = inputData.map(element => {
    //     return {
    //         x: element.timestamp.substr(9),
    //         y: parseFloat(element.humidity)
    //     }
    // })

    config = {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Temperature',
                    data: temperature,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)'
                },
                // {
                //     label: 'Humidity',
                //     data: humidity,
                //     fill: false,
                //     borderColor: 'rgb(66, 202, 59)'
                // }
            ]
        }
    }

    if (lineChart){
        lineChart.destroy()
    }

    lineChart = new Chart(ctx, config)
}

function displayCurrentData(inputData) {
    document.getElementById("nodeName").innerHTML = inputData.name;
    document.getElementById("temperatureValue").innerHTML = inputData.tempF + " F";
    document.getElementById("humidityValue").innerHTML = inputData.humidity + "%";
    document.getElementById("highTempValue").innerHTML = inputData.high_temp + " F";
    document.getElementById("lowTempValue").innerHTML = inputData.low_temp + " F";
}

function fetchCurrentData() {
    fetch("/json")
        .then(response => response.json())
        .then(data => displayCurrentData(data));
}

function fetchChartData() {
    fetch("/history")
        .then(response => response.json())
        .then(data => renderChart(data));
}

fetchChartData()
fetchCurrentData()

const millisecond = 1000;
const minute = 60

setInterval(fetchChartData, millisecond * (minute * 10));
setInterval(fetchCurrentData, millisecond * (minute * 5));

