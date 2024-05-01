<template>
  <Pie ref="chart" :chart-data="chartData" :chart-options="chartOptions" />
</template>

<script>
import { Pie } from 'vue-chartjs/legacy'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

export default {
  components:{Pie},
  name: 'pieChart',
  props: ['chartData','chartOptions'],
}
</script>