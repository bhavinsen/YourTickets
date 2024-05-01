<template>

  <panel>
    <overlayloader :visible="!loaded"></overlayloader>
    <no-data-overlay v-if="noDataOverlay" :visible="noData"></no-data-overlay>
    <v-toolbar dense flat>
      <v-toolbar-title>
        {{ $t('Ticket type distribution') }}
        
      </v-toolbar-title>
      <v-spacer />
      <percentageSwitcher v-if="switcher" @change="(v) => $refs.chart.changeDisplayType(v)"></percentageSwitcher>
    </v-toolbar>
    <v-card-text align="center">
      <ticketDistributionChart
          @startLoading="loaded = false"
          @loaded="loaded = true"
          ref="chart"
      ></ticketDistributionChart>
    </v-card-text>
  </panel>

</template>
<script>

  import overlayloader from "@/components/core/overlayloader";
  import percentageSwitcher from "@/components/core/percentageSwitcher";
  import ticketDistributionChart from "@/components/charts/ticketDistributionChart";
  import noDataOverlay from "@/components/core/noDataOverlay";


  export default {
    name: 'genderChartPanel',
    components: {overlayloader, percentageSwitcher, ticketDistributionChart, noDataOverlay},
    props:['switcher','data', 'noDataOverlay'],
    mounted () {

    },
    watch: {
      'data': function(){
        this.load()
      },
    },
    methods:{
      async load() {
        this.noData = false
        let response;
        if(this.data.event_id){
          response = await this.$refs.chart.load(
              this.$store.getters['event_statistics/getTicketsCount'](this.data.event_id, this.data.start_date, this.data.end_date)
          )

        }else{
          let params = {'start_date': this.data.start_date, 'end_date': this.data.end_date}
          response = await this.$refs.chart.load(this.$store.dispatch('stats/getTicketsCount', params))

        }

        if(response.data.labels.length === 0){
          this.noData = true;
        }
      },
    },
    data:() => ({
      loaded:false,
      noData:false
    })
  }
</script>
