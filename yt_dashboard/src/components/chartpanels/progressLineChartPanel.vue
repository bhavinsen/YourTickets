<template>
  <panel>
    <overlayloader :visible="!loaded"></overlayloader>
      <v-toolbar dense flat>
        <v-toolbar-title>
          <simpleDropDown v-if="switcher" @change="load" :items="dropdownItems" ></simpleDropDown>
          <span v-if="!switcher">
            {{ $t('Sold ticket amount') }}
            </span>

        </v-toolbar-title>
        <v-spacer></v-spacer>
          <stats-event-dropdown v-if="data.event_id && comparer" :dropdownTitle="$t('Compare with event')" @select_event="select_event"></stats-event-dropdown>
      </v-toolbar>
        <v-card-text align="center">
          <progressLineChart
            ref="chart"
            @startLoading="loaded = false"
            @loaded="loaded = true"
          ></progressLineChart>
        </v-card-text>
    </panel>

</template>
<script>

  import overlayloader from "@/components/core/overlayloader";
  import progressLineChart from "@/components/charts/progressLineChart";
  import simpleDropDown from "@/components/core/simpleDropDown";
  import statsEventDropdown from "@/views/stats/components/statsEventDropdown";


  export default {
    name: 'progressLineChartPanel',
    components: {overlayloader, progressLineChart, simpleDropDown, statsEventDropdown},
    props:['data', 'switcher', 'comparer'],
    mounted () {

    },
    watch: {
      'data': function(){
        this.load(this.dropdownItems[0])
      },
    },
    methods:{
      select_event({event}){
        this.selected_event = event
        //load and add dataset
        this.$refs.chart.loadCompare(
              this.$store.getters['event_statistics/getEarnings'](this.selected_event.pk, this.data.start_date, this.data.end_date)
          )
      },
      load(selectedItem={}) {

        if(this.data.event_id){
          this.$refs.chart.load(
              this.$store.getters['event_statistics/getEarnings'](this.data.event_id, this.data.start_date, this.data.end_date)
          )
        }else{
          let params = {'chart_type': selectedItem.selection,'start_date': this.data.start_date, 'end_date': this.data.end_date}

          this.$refs.chart.load(this.$store.dispatch('stats/getEarnings', params)
          )
        }

      },
    },
    computed: {


    },
    data:(scope) => ({
      loaded:false,
      selected_event:{},
      dropdownItems:[
        {
          text: scope.$t('Sold tickets'),
          selection: 'sold_tickets'
        },{
          text: scope.$t('Revenue'),
          selection: 'revenue'

      }],


    })
  }
</script>
