<template>
  <Doughnut :chart-data="chartData" :chart-options="options" :plugins="plugins" />
</template>

<script>
import { Doughnut } from 'vue-chartjs/legacy'

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

export default {

  name: 'doughnutchart',
  components:{Doughnut},
  props: ['chartData','options', 'plugins'],


}
</script>