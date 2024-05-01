<template>

  <doughnutchart
      :options="options"
      :chart-data="data"
      :style="style">
  </doughnutchart>
</template>

<script>
import doughnutchart from "@/components/charts/doughnutchart";
import {chartLegendDynamic} from "@/helpers/chartStyle";
import {percentageFormatter} from "@/helpers/chartHelpers";

export default {
  components:{doughnutchart},
  name: 'genderChart',
  emits: ['loaded', 'startLoading', 'noData'],
  methods:{
    update(){
      this.$refs.chart.updateChart()
    },
    load(promise){
      this.loaded = false;
      this.$emit('startLoading')
      return promise.then((response) => {
        this.changeDisplayType('percentage')

        let data = response.data;
        if(data[0] === 0 && data[1] === 0){
          this.data.datasets[0].data = this.dummiData;
          this.options.plugins.datalabels.display = false;
          this.$emit('noData')
        }else{
          this.data.datasets[0].data = response.data
        }

        this.loaded = true;
        this.$emit('loaded')
        return response
      })
    },
    changeDisplayType(val){
      this.data.datasets[0].datalabels.formatter = (value, ctx) => {
        return percentageFormatter(value, ctx, val)
      }
    }
  },
  data: (scope) => ({
    dummiData: [1,1],
    style:{
      height:"254px"
    },
    loaded: false,
    options: {

      backgroundColor: [
        '#EC939C',
        '#66C5E1',
      ],
      borderWidth: 1,
      plugins: {
        datalabels:{},
        legend: chartLegendDynamic(scope)
      },
      responsive: true, maintainAspectRatio: false,
    },
    data:{
      labels: [scope.$t('Female'), scope.$t('Male'),],
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