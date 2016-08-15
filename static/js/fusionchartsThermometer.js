function addThermometer(renderAt, value, caption, subcaption){
    var fusioncharts = new FusionCharts({
    type: 'thermometer',
    renderAt: renderAt,
    id: 'Therm' +renderAt,
    width: '160',
    height: '260',
    dataFormat: 'json',
    dataSource: {
        "chart": {
            "caption": caption,
            "subcaption": subcaption,
            "lowerLimit": "-5",
            "upperLimit": "35",
            "decimals": "1",
            "numberSuffix": "°C",
            "showhovereffect": "1",
            "thmFillColor": "#008ee4",
            "showGaugeBorder": "1",
            "gaugeBorderColor": "#008ee4",
            "gaugeBorderThickness": "2",
            "gaugeBorderAlpha": "30",
            "thmOriginX": "60",
            "chartBottomMargin": "20",
            "valueFontColor": "#000000",
            "theme": "fint"
        },
        "value": value,
        "annotations": {
            "showbelow": "0",
        },
    },
  });
  fusioncharts.render();
}

function addEnergy(renderAt, value, caption, subcaption){
    var fusioncharts = new FusionCharts({
    type: 'hlineargauge',
    renderAt: renderAt,
    id: 'Energy' +renderAt,
    width: '400',
    height: '200',
    dataFormat: 'json',
    dataSource: {
        "chart": {
            "theme": "fint",
            "caption": caption,
            "subcaption": subcaption,
            "lowerLimit": "0",
            "upperLimit": "8000",
            "numberSuffix": "W",
            "chartBottomMargin": "40",
            "valueFontSize": "11",
            "valueFontBold": "0"
        },
        "colorRange": {
            "color": [{
                "minValue": "0",
                "maxValue": "2000",
                "label": "Normal",
            }, {
                "minValue": "2001",
                "maxValue": "6000",
                "label": "Alto",
            }, {
                "minValue": "6001",
                "maxValue": "8000",
                "label": "Extremo",
            }]
        },
        "pointers": {
            "pointer": [{
                "value": value
            }]
        },
        "trendPoints": {
            "point": [
                //Trendpoint
                {
                    "startValue": "1800",
                    "displayValue": "Atención",
                    "dashed": "1",
                    "showValues": "0"
                }, {
                    "startValue": "7000",
                    "displayValue": "Máximo ICP",
                    "dashed": "1",
                    "showValues": "0"
                }
            ]
        },
    },
  });
  fusioncharts.render();
}

$(function() {
    var sValue;
    var sTime;
    sValue = $('#energiaValue').attr('value')
    sTime = $('#energiaTime').attr('value')
    FusionCharts.ready(addEnergy('chart-energia', sValue, 'Energía', sTime));

    sValue = $('#temperatura_calleValue').attr('value')
    sTime = $('#temperatura_calleTime').attr('value')
    FusionCharts.ready(addThermometer('chart-tempCalle', sValue, 'Temperatura Calle', sTime));

    sValue = $('#temperatura_salonValue').attr('value')
    sTime = $('#temperatura_salonTime').attr('value')
    FusionCharts.ready(addThermometer('chart-tempSalon', sValue, 'Temperatura Salón', sTime));
    
    sValue = $('#temperatura_dormitorioValue').attr('value')
    sTime = $('#temperatura_dormitorioTime').attr('value')    
    FusionCharts.ready(addThermometer('chart-tempDormitorio', sValue, 'Temperatura Dormitorio', sTime));
})
