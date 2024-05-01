<template>

  <panel>
    <overlayloader :visible="!loaded"></overlayloader>
    <no-data-overlay v-if="noDataOverlay" :visible="noData"></no-data-overlay>
    <v-toolbar dense flat>
      <v-toolbar-title>
        {{ $t('New vs returning visitor') }}
        
      </v-toolbar-title>
      <v-spacer />
      <percentageSwitcher v-if="switcher" @change="(v) => $refs.chart.changeDisplayType(v)"></percentageSwitcher>
    </v-toolbar>
    <v-card-text align="center">
      <returningVisitorsChart
          @startLoading="loaded = false"
          @loaded="loaded = true"
          @noData="noData = true"
          ref="chart"
      ></returningVisitorsChart>
    </v-card-text>
  </panel>

</template>
<script>

  import overlayloader from "@/components/core/overlayloader";
  import percentageSwitcher from "@/components/core/percentageSwitcher";
  import returningVisitorsChart from "@/components/charts/returningVisitorsChart";
  import noDataOverlay from "@/components/core/noDataOverlay";

  export default {
    name: 'returningVisitorChartPanel',
    components: {overlayloader, percentageSwitcher, returningVisitorsChart, noDataOverlay},
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
              this.$store.getters['event_statistics/getNewReturningVisitors'](this.data.event_id, this.data.start_date, this.data.end_date)
          )
        }else{
          let params = {'start_date': this.data.start_date, 'end_date': this.data.end_date}
          this.$refs.chart.load(this.$store.dispatch('stats/getNewReturningVisitors', params))
        }
      },
    },
    data:() => ({
      loaded:false,
      noData:false,
    })
  }
</script>
