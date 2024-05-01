<template>

  <doughnutchart
      :options="options"
      :chart-data="data"
      :style="style">

  </doughnutchart>
</template>

<script>
import doughnutchart from "@/components/charts/doughnutchart";
import {chartLegend} from "@/helpers/chartStyle";
import {percentageFormatter} from "@/helpers/chartHelpers";

export default {
  components:{doughnutchart},
  name: 'returnVisitorsChart',
  emits: ['loaded', 'startLoading', 'noData'],
  methods:{
    update(){
      this.$refs.chart.updateChart()
    },
    load(promise){
      this.loaded = false;
      this.$emit('startLoading')
      promise.then((response) => {
        this.changeDisplayType('percentage')

        let data = response.data;
        if(data[0] === 0 && data[1] === 0){
          this.data.datasets[0].data = this.dummiData
          this.$emit('noData')
        }else {
          this.data.datasets[0].data = response.data
        }
          this.loaded = true;
          this.$emit('loaded')
      })
    },
    changeDisplayType(val){
      this.data.datasets[0].datalabels.formatter = (value, ctx) => {
        return percentageFormatter(value, ctx, val)
      }
    }
  },
  data: (scope) => ({
    dummiData:[1,1],
    style:{
      height:"254px"
    },
    loaded: false,
    options: {
      backgroundColor: [
        '#66C5E1',
        '#cef0fd',

      ],
      borderWidth: 1,
      plugins: {
        legend: chartLegend
      },
      responsive: true, maintainAspectRatio: false,
    },
    data:{
      labels: [scope.$t('New'), scope.$t('Returning')],
      datasets: [{
        data:[],
        datalabels: {
            color: '#000000',
            formatter:{},
            labels: {
              title: {
                font: {
                  weight: 'bold',
                  size:'16'
                }
              }
            },
          }
      }]
    }
  })

}
</script>