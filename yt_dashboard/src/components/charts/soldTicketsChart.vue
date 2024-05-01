<template>

  <doughnutchart
      :options="options"
      :chart-data="data"
      :style="style"
      :plugins="plugins"
  >

  </doughnutchart>
</template>

<script>
import doughnutchart from "@/components/charts/doughnutchart";
// import {percentageFormatter} from "@/helpers/chartHelpers";

export default {
  components:{doughnutchart},
  name: 'soldTicketsChart',
  emits: ['loaded', 'startLoading'],
  methods:{
    update(){
      this.$refs.chart.updateChart()
    },
    load(promise){
      this.loaded = false;
      this.$emit('startLoading')
      promise.then((response) => {
        this.changeDisplayType()
        this.data.datasets[0].data = [response.data.tickets_sold, response.data.tickets_available - response.data.tickets_sold]
        this.data.total = response.data.tickets_available
        this.loaded = true;
        this.$emit('loaded')
      })
    },
    changeDisplayType(val){
      this.displayType = val
      if(this.data.datasets[0].label === 'a'){
        this.data.datasets[0].label = 'b'
      }else{
        this.data.datasets[0].label = 'a';
      }
    }
  },
  data: (context) => ({
    style:{
      height:"254px"
    },
    displayType:'percentage',
    loaded: false,
    options: {
      animation:false,
      responsive: true, maintainAspectRatio: false,
    },
    plugins: [
        {
            id: 'percentage_formatter',
            beforeDraw: function (chart) {

          var width = chart.width;
          var height = chart.height;
          var ctx = chart.ctx;

          ctx.restore();
          // var fontSize = (height / 114).toFixed(2);
          // ctx.font = fontSize + "em sans-serif";
          // console.log(fontSize + "em sans-serif")
          ctx.font = 'bold 2.23em sans-serif';
          ctx.textBaseline = "middle";
          // let opts = chart.options.centertext;
          let sold = context.data.datasets[0].data[0];
          let total = context.data.total;
          let percentage = 0
          if(total > 0){
            percentage = ((sold /  total) * 100).toFixed(2)
          }

          //chart.data.datasets[0].data[0]
          var text =  + percentage + '%';
          if(context.displayType === 'number'){
            text = sold;
          }
          var textX = Math.round((width - ctx.measureText(text).width) / 2);
          var textY = height / 2;
          ctx.fillStyle = '#000000'
          ctx.fillText(text, textX, textY);
          ctx.font = '1.3em sans-serif';
          ctx.fillStyle = '#66C5E1'
          let text2 = 'verkocht'
          textX = Math.round((width - ctx.measureText(text2).width) / 2);
          ctx.fillText(text2, textX-3, textY+25);
          ctx.save();
         }
        }
    ],
    data:{
        datasets: [{
          label:'',
          borderWidth:0,
          data:[0,1],
          backgroundColor:['#66C5E1', '#EDF5F7'],
          datalabels: {
            formatter:{},
            display:false,
            align: 'start',
            anchor: 'start',
          }
        }]
      }
  })

}
</script>