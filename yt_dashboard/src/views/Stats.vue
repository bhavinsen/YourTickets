<template>
  <v-container
    fluid
  >
    <v-row>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 6">
        <stats-event-dropdown @select_event="select_event"></stats-event-dropdown>
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 6" :class="$vuetify.breakpoint.mdAndUp ? 'text-right' : ''">
        <date-dropdown @date_changed="select_date"></date-dropdown>
      </v-col>
    </v-row>
    <v-layout row v-if="$vuetify.breakpoint.mdAndUp">
        <v-flex col  class="lg5-custom">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Amount tickets sold')" :icon="require('@/assets/icons/tickets.svg')" :number="sold_ticket_amount" />
        </v-flex>
        <v-flex col class="lg5-custom">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Earnings this period')" :icon="require('@/assets/icons/earnings.svg')" :number="revenue" />
        </v-flex>
        <v-flex col  class="lg5-custom">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Ticketshop views')" :icon="require('@/assets/icons/visitors.svg')" :number="visitors" />
        </v-flex>
        <v-flex col  class="lg5-custom">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Unique ticketshop views')" :icon="require('@/assets/icons/visitors.svg')" :number="new_visitors" />
        </v-flex>
        <v-flex col  class="lg5-custom">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Conversion rate')" :icon="require('@/assets/icons/statistics.svg')" :number="conversion_rate+'%'" />
        </v-flex>

    </v-layout>
    <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="6">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Amount tickets sold')" :icon="require('@/assets/icons/tickets.svg')" :number="sold_ticket_amount" />
        </v-col>
        <v-col cols="6">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Earnings this period')" :icon="require('@/assets/icons/earnings.svg')" :number="revenue" />
        </v-col>
        <v-col cols="6">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Ticketshop views')" :icon="require('@/assets/icons/visitors.svg')" :number="visitors" />
        </v-col>
        <v-col cols="6">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Unique ticketshop views')" :icon="require('@/assets/icons/visitors.svg')" :number="new_visitors" />
        </v-col>
        <v-col cols="12">
          <highlight-panel cls="dark" style="height:160px;" :title="$t('Conversion rate')" :icon="require('@/assets/icons/statistics.svg')" :number="conversion_rate+'%'" />
        </v-col>

    </v-row>

    <v-row>
      <v-col>
         <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <progress-line-chart-panel comparer="true" switcher="true" :data="chartParams"></progress-line-chart-panel>
      </v-col>

    </v-row>
    <v-row>
      <v-col>
         <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 4">
        <gender-chart-panel :data="chartParams"></gender-chart-panel>
      </v-col>
      <v-divider vertical v-show="$vuetify.breakpoint.mdAndUp" ></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 4">
        <returning-visitor-chart-panel :data="chartParams"></returning-visitor-chart-panel>
      </v-col>
      <v-divider vertical v-show="$vuetify.breakpoint.mdAndUp" ></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 4">
        <top-list ref="toplist" :title="$t('Residence top 10')"></top-list>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
         <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 6">
        <age-gender-chart-panel :data="chartParams"></age-gender-chart-panel>
      </v-col>
      <v-divider vertical v-show="$vuetify.breakpoint.mdAndUp" ></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 6">
        <top-list show-dropdown="true" ref="eventstoplist" :title="$t('Events top 10')"></top-list>
      </v-col>


    </v-row>

  </v-container>
</template>

<script>

import statsEventDropdown from "@/views/stats/components/statsEventDropdown";
import dateDropdown from "@/components/core/dateDropdown";
import highlightPanel from "@/components/core/highlightPanel";
import genderChartPanel from "@/components/chartpanels/genderChartPanel";
import progressLineChartPanel from "@/components/chartpanels/progressLineChartPanel";
import returningVisitorChartPanel from "@/components/chartpanels/returningVisitorChartPanel";
import ageGenderChartPanel from "@/components/chartpanels/ageGenderChartPanel";
import topList from "@/components/core/topList";


export default {
  name: 'Stats',
  components: {
    statsEventDropdown,
    dateDropdown,
    highlightPanel,
    genderChartPanel,
    progressLineChartPanel,
    returningVisitorChartPanel,
    ageGenderChartPanel,
    topList
  },
  mounted () {
    this.load_event_data()
  },
  computed:{

  },
  methods:{
    select_event({event}){
      this.selected_event = event;
      this.load_event_data()
    },
    select_date(start_date, end_date){
      this.start_date = start_date;
      this.end_date = end_date;

      // if(this.selected_event.pk){

        this.load_event_data()
      // }
    },
    load_event_data(){

      this.chartParams = {

        'start_date': this.start_date,
        'end_date': this.end_date
      }
      if(this.selected_event.pk != undefined) {
        this.chartParams['event_id'] = this.selected_event.pk
      }
      if(this.chartParams['event_id']) {
        this.$store.getters['event_statistics/getSoldTicketAmount'](this.selected_event.pk, this.start_date, this.end_date)
            .then((response) => {
              this.sold_ticket_amount = response.data.total
            })
        this.$store.getters['event_statistics/getRevenue'](this.selected_event.pk, this.start_date, this.end_date)
            .then((response) => {
              this.revenue = response.data.total
            })
        this.$store.getters['event_statistics/getVisitors'](this.selected_event.pk, this.start_date, this.end_date)
            .then((response) => {
              this.visitors = response.data.total
            })
        this.$store.getters['event_statistics/getConversionRate'](this.selected_event.pk, this.start_date, this.end_date)
            .then((response) => {
              this.conversion_rate = response.data.total
            })
      }else{
        let store_object = this.$store
        let params = {'start_date': this.start_date, 'end_date': this.end_date}

        store_object.dispatch('aggregate/getSoldTicketAmount', params)
        .then((response) => {
          this.sold_ticket_amount = response.data.total
        })
        store_object.dispatch('aggregate/getRevenue', params)
          .then((response) => {
            this.revenue = response.data.total
          })
        store_object.dispatch('aggregate/getVisitors', params)
          .then((response) => {
            this.visitors = response.data.total
          })
        // temp disabled
        store_object.dispatch('aggregate/getConversionRate', params)
          .then((response) => {
            this.conversion_rate = response.data.total
        })
      }

      if(this.chartParams['event_id']) {
        this.$refs.toplist.load('event_statistics/listResidence', this.chartParams)
      }else{
        this.$refs.toplist.load('stats/listResidence', this.chartParams)
      }
      //'chart_type': selectedItem.selection,
      let params = {'start_date': this.start_date, 'end_date': this.end_date}

      this.$refs.eventstoplist.load('stats/getTop5Chart', params)

      // this.$refs.eventstoplist.load(this.$store.dispatch('stats/getTop5Chart', params))
    },

  },
  data: () => ({
    chartParams:{
      'event_id': false,
      'start_date': '',
      'end_date': ''
    },
    selected_event:{},
    start_date:'',
    end_date:'',
    sold_ticket_amount:10,
    revenue:0,
    visitors:0,
    new_visitors:0,
    conversion_rate:0,


  })
}
</script>
