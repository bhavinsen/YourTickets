<template>
  <lineChart ref="chart" :chart-data="data" :chart-options="options" :style="style" />
</template>

<script>
import { Line as lineChart } from 'vue-chartjs/legacy'
import { Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement} from 'chart.js'

ChartJS.register(  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement);

export default {
  name: 'progressLineChart',
  components:{lineChart},
  emits: ['loaded', 'startLoading'],
  methods:{
    load(promise){
      this.loaded = false;
      this.$emit('startLoading')
      promise.then((response) => {

          this.data.datasets[0].data = response.data.data
          this.data.labels = response.data.labels
          this.loaded = true;
          this.$emit('loaded')
      })
    },
    loadCompare(promise){
      this.loaded = false;
      this.$emit('startLoading')
      promise.then((response) => {
          //[5, 10, 25, 4, 8, 30, 26, 5]
          this.data.datasets[1].data = response.data.data
          // this.data.labels = response.data.labels
          this.loaded = true;
          this.$emit('loaded')
      })
    }

  },
  data: (scope) => ({
    style: {
      height: "254px"
    },
    loaded: false,
    options: {
      radius: 0,
      
      plugins: {
        datalabels:{
          display:false,
        },
        legend: {
          display: false,
        },
        tooltip: {
        intersect: false,
        // mode:'average'
      }
      },
      scales: {
        x: {

          ticks:{
            // maxTicksLimit:5
            // sampleSize:2
            // stepSize:50,
            autoSkip: true,
            maxTicksLimit: function(){
              if(scope.$vuetify.breakpoint.smAndDown){
                return 8
              }else{
                return 12
              }
              
            },
            // display:false,
          },
          max: function(){
              if(scope.$vuetify.breakpoint.smAndDown){
                return 20
              }else{
                return 30
              }
              
            },
          // suggestedMin: 50,
          //       suggestedMax: 10,
          // stacked: 'single',
          gridLines: {
            display:true,
            color:'#D6ECF5',
            lineWidth:2,
            drawBorder: false,
          }
        },
        y: {
          gridLines: {
            display:false,
            drawBorder: false
          },
          min:0,
          //deze beiden uitgezet voor de bovengrens
          // max:50,
          // suggestedMax: 50,
          stepValue: 50,
          ticks: {

            stepSize:100,
            // color:'red'
          }
        }
      },
      responsive: true, maintainAspectRatio: false,
    },
    data: {
      labels: [],
      datasets: [{
        data: [],
        label: 'a',
        fill:false,
        radius:0,
        pointHitRadius:10,
        cubicInterpolationMode: 'monotone',
        borderColor:'#D92B3C',
        borderWidth: 4
      },{
        data: [],
        label: 'b',
        fill:false,
        radius:0,
        pointHitRadius:10,
        cubicInterpolationMode: 'monotone',
        borderColor:'#90D5E9',
        borderWidth: 4
      }]
    }
  })

}
</script>