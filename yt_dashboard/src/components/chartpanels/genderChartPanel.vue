<template>

  <panel>
    <overlayloader :visible="!loaded"></overlayloader>
    <no-data-overlay v-if="noDataOverlay" :visible="noData"></no-data-overlay>
    <v-toolbar dense flat>
      <v-toolbar-title>
        {{ $t('Male - Female distribution') }}
        
      </v-toolbar-title>
      <v-spacer />
      <percentageSwitcher v-if="switcher" @change="(v) => $refs.chart.changeDisplayType(v)"></percentageSwitcher>
    </v-toolbar>
    <v-card-text align="center">
      <gender-chart
          @startLoading="loaded = false"
          @loaded="loaded = true"
          @noData="noData = true"
          ref="chart"
      ></gender-chart>
    </v-card-text>
  </panel>

</template>
<script>

  import overlayloader from "@/components/core/overlayloader";
  import percentageSwitcher from "@/components/core/percentageSwitcher";
  import genderChart from "@/components/charts/genderChart";
  import noDataOverlay from "@/components/core/noDataOverlay";


  export default {
    name: 'genderChartPanel',
    components: {overlayloader, percentageSwitcher, genderChart, noDataOverlay},
    props:['switcher','data', 'noDataOverlay'],
    watch: {
      'data': function(){
        this.load()
      },
    },
    methods:{
      load() {
        this.noData = false
        if(this.data.event_id){
          this.$refs.chart.load(
              this.$store.getters['event_statistics/getGenderChart'](this.data.event_id, this.data.start_date, this.data.end_date)
          )
        }else{
          let params = {'start_date': this.data.start_date, 'end_date': this.data.end_date}
          this.$refs.chart.load(this.$store.dispatch('stats/getGenderChart', params)).then(()=>{
            // let data = response.data;
            // if(data[0] === 0 && data[1] === 0 && data[2] === 0){
            //   this.noData = true
            // }
          })
        }

      },
    },
    data:() => ({
      loaded:false,
      noData:false,

    })
  }
</script>
