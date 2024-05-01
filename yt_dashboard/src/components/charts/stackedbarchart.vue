<template>
  <div>
    <GChart type="ColumnChart" :options="options" :data="data" />
  </div>
</template>
 
<script>
import { GChart } from "vue-google-charts/legacy";
export default {
  name: "stackedbarchart",
  components: {
    GChart
  },
  props: ['chartData', 'chartOptions'],
  data(scope) {
    return {
      data: [
        ['Element', 'Male', { role: 'male' }, 'Female', { role: 'female' }],
      ],
      labels: ['< 18 ' + scope.$t('year'), '18 - 25', '26 - 35', '36 - 45', '46+'],
      options: {
        width: 550,
        height: 400,
        series: [
          { color: '#67c9e6' },
          { color: '#DC3547' },
        ]
      }
    };
  },
  mounted() {
    this.updateChart(this.chartData);
  },
  watch: {
    chartData: {
      handler(newChartData) {
        this.updateChart(newChartData);
      },
      deep: true
    }
  },
  methods: {
    updateChart(chartDatas) {
      
      console.log('chartDaaaatas',chartDatas);
      const ageGender = [];
      chartDatas.male.forEach((dataset,index) => {
        ageGender[index] = [this.labels[index],dataset,'#44800b',chartDatas.female[index],'#050bab']
      });
      this.data = [this.data[0],...ageGender];
    }
  }
}
</script>                       