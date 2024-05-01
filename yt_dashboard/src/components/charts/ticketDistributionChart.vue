<template>
    <pieChart ref="chart" :chart-data="data" :chart-options="options" :style="style" />
</template>

<script>
import pieChart from "@/components/charts/pieChart";
import {chartLegend} from "@/helpers/chartStyle";
import {percentageFormatter, pieChartOffsetFormatter} from "@/helpers/chartHelpers";

export default {
  components:{pieChart},
  name: 'ticketDistributionChart',
  emits: ['loaded', 'startLoading', 'noData'],
  methods:{
    load(promise){
      this.loaded = false;
      this.$emit('startLoading')
      return promise.then((response) => {
          this.changeDisplayType('percentage')

          let data = response.data;
          if(data.labels.length === 0){
            this.data.datasets[0].data = this.dummiData.data
            this.data.labels = this.dummiData.labels
            this.$emit('noData')
          }else{
            this.data.datasets[0].data = response.data.data
            this.data.labels = response.data.labels
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
    dummiData:{"labels": [scope.$t('No ticket sold')], "data": [1]},
    style:{
      height:"254px"
    },
    loaded: false,
    options:{
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: chartLegend,
      }
    },
    data:{
      labels: [],
      datasets: [{
          borderRadius:6,
          data: [],
          backgroundColor: [
              'rgb(102, 197, 225)',
              'rgb(102, 197, 225, 0.8)',
              'rgb(102, 197, 225, 0.6)',
              'rgb(102, 197, 225, 0.4)',
          ],
          borderWidth: 4,
          datalabels: {
            color: '#000000',
            align: 'end',
            // formatter: (value, ctx) => {
            //   return percentageFormatter(value, ctx, instance.displayType)
            // },
            offset:pieChartOffsetFormatter,
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
      },],
    }
  })

}
</script>