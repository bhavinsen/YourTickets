let chartLegend = {

    position: 'right',
    align:'center',
    labels: {

      usePointStyle: true,
      font: {
        size: 12,
        weight:'bold'
      }
    },

}

function chartLegendDynamic(scope){
    let config = chartLegend
    if(scope.$vuetify.breakpoint.smAndDown){
        config.position = 'bottom'
    }
    return config
}

export {chartLegend, chartLegendDynamic}