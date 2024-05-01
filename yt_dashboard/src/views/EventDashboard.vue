<template>
  <v-container
    fluid
  >
    <v-row>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
        <highlight-panel cls="dark" style="height:160px;" :title="$t('Amount tickets sold')" :icon="require('@/assets/icons/tickets.svg')" :number="sold_ticket_amount" />
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
        <highlight-panel cls="dark"  style="height:160px;" :title="$t('Revenue')" :icon="require('@/assets/icons/earnings.svg')" :number="revenue" />
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
        <highlight-panel cls="dark" style="height:160px;" :title="$t('Ticketshop views')" :icon="require('@/assets/icons/visitors.svg')" :number="visitors" />
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
        <highlight-panel cls="dark" style="height:160px;" :title="$t('Conversion rate')" :icon="require('@/assets/icons/statistics.svg')" :number="conversion_rate+'%'" />
      </v-col>
    </v-row>

    <v-row>
      <v-col>
         <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
       <v-col :cols="$vuetify.breakpoint.mdAndDown ? 12 : 7" v-if="$vuetify.breakpoint.mdAndDown">
        <progress-line-chart-panel switcher="true" :data="chartParams"></progress-line-chart-panel>

      </v-col>
    </v-row>
    <v-divider v-show="$vuetify.breakpoint.mdAndDown" ></v-divider>
    <v-row>

      <v-col :cols="$vuetify.breakpoint.mdAndDown ? 12 : 4">
        <panel>

          <overlayloader :visible="!soldTicketsChartLoaded"></overlayloader>
          <v-card-title>
            {{$t('Sold tickets')}}
            <v-spacer />


            <percentageSwitcher @change="(v) => $refs.soldTicketsChart.changeDisplayType(v)"></percentageSwitcher>
          </v-card-title>
          <v-card-text align="center">
            <sold-tickets-chart
                @startLoading="soldTicketsChartLoaded = false"
                @loaded="soldTicketsChartLoaded = true"
                ref="soldTicketsChart"
            ></sold-tickets-chart>

          </v-card-text>
        </panel>
      </v-col>
      <v-divider vertical v-show="$vuetify.breakpoint.mdAndUp" ></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>

      <v-col :cols="$vuetify.breakpoint.mdAndDown ? 12 : 4">

        <ticket-distribution-chart-panel switcher="true" :data="chartParams"></ticket-distribution-chart-panel>

      </v-col>

      <v-divider vertical v-show="$vuetify.breakpoint.mdAndUp" ></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>
      <v-col :cols="$vuetify.breakpoint.mdAndDown ? 12 : 4">

        <gender-chart-panel switcher="true" :data="chartParams"></gender-chart-panel>

      </v-col>
    </v-row>
    <v-row>
      <v-col>
         <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col :cols="$vuetify.breakpoint.mdAndDown ? 12 : 5">
        <age-gender-chart-panel :data="chartParams"></age-gender-chart-panel>
      </v-col>
      <v-divider vertical v-show="$vuetify.breakpoint.mdAndUp" ></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>
      <v-col :cols="$vuetify.breakpoint.mdAndDown ? 12 : 7" v-if="$vuetify.breakpoint.lgAndUp">
        <progress-line-chart-panel  :data="chartParams"></progress-line-chart-panel>

      </v-col>
    </v-row>
    <v-row v-if="$vuetify.breakpoint.lgAndUp">
      <v-col>
         <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col :cols="$vuetify.breakpoint.mdAndDown ? 12 : 4">
        <top-list show-dropdown="true" no-data-overlay="true" ref="toplist" :title="$t('Events top 10')"></top-list>
      </v-col>
      <v-divider vertical v-show="$vuetify.breakpoint.mdAndUp" ></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>

      <v-col :cols="$vuetify.breakpoint.mdAndDown ? 12 : 4">
        <returning-visitor-chart-panel no-data-overlay="true" switcher="true" :data="chartParams"></returning-visitor-chart-panel>

      </v-col>
      <v-divider vertical ></v-divider>



    </v-row>
  </v-container>
</template>

<script>

import overlayloader from "@/components/core/overlayloader";


import soldTicketsChart from "@/components/charts/soldTicketsChart";
import percentageSwitcher from "@/components/core/percentageSwitcher";
import { mapGetters } from "vuex"
import highlightPanel from "@/components/core/highlightPanel";
import returningVisitorChartPanel from "@/components/chartpanels/returningVisitorChartPanel";
import ticketDistributionChartPanel from "@/components/chartpanels/ticketDistributionChartPanel";
import ageGenderChartPanel from "@/components/chartpanels/ageGenderChartPanel";
import progressLineChartPanel from "@/components/chartpanels/progressLineChartPanel";
import genderChartPanel from "@/components/chartpanels/genderChartPanel";
import topList from "@/components/core/topList";

export default {
  name: 'EventDashboard',
  components: {
    overlayloader,
    genderChartPanel,
    soldTicketsChart,
    percentageSwitcher,
    progressLineChartPanel,
    highlightPanel,
    ageGenderChartPanel,
    returningVisitorChartPanel,
    ticketDistributionChartPanel,
    topList
  },
  mounted () {

    this.load_event_data()

  },
  computed:{
    ...mapGetters({
      event: 'event/getEvent',
    }),

  },
  methods:{

    load_event_data(){

      this.chartParams = {
        'event_id': this.$route.params.id,
        'start_date': this.start_date,
        'end_date': this.end_date
      }

      this.$store.dispatch('event/loadEvent', this.$route.params.id)

      this.$store.getters['event_statistics/getSoldTicketAmount'](this.$route.params.id)
      .then((response) => {
        this.sold_ticket_amount = response.data.total
      })
      this.$store.getters['event_statistics/getRevenue'](this.$route.params.id)
        .then((response) => {
          this.revenue = response.data.total
        })
      this.$store.getters['event_statistics/getVisitors'](this.$route.params.id)
        .then((response) => {
          this.visitors = response.data.total
        })
      this.$store.getters['event_statistics/getConversionRate'](this.$route.params.id)
        .then((response) => {

          this.conversion_rate = response.data.total
        })

      this.load_total_sold()

      // this.$refs.toplist.load(this.$store.getters['event_statistics/listResidence'](this.$route.params.id))
      this.$refs.toplist.load('event_statistics/listResidence', this.chartParams)
    },

    load_total_sold() {
      this.$refs.soldTicketsChart.load(this.$store.getters['event_statistics/getTotalSoldOf'](this.$route.params.id))
    }
  },
  watch: {
    '$route': function(to, from){
      if(to.name === 'event_dashboard' && from.name === 'event_dashboard'){
        this.load_event_data()
      }
    }
  },
  data: () => ({
    chartParams:{
      'event_id': false,
      'start_date': '',
      'end_date': ''
    },
    soldTicketsChartLoaded:false,
    sold_ticket_amount:10,
    revenue:0,
    visitors:0,
    conversion_rate:0,
    start_date:'',
    end_date:''
  })
}
</script>
