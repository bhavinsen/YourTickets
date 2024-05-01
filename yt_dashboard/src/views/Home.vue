<template>
  <v-container
    fluid
  >
    <v-row>
      <v-col>
        <div class="d-flex justify-end date_menu_container">
          <date-dropdown @date_changed="reload_all_charts"></date-dropdown>
        </div>
      </v-col>
    </v-row>
    <v-row >
<!--      <v-col cols="12" v-if="$vuetify.breakpoint.smAndDown">-->

<!--        <v-carousel height="250" light v-model="carousel_model">-->
<!--          <v-carousel-item>-->
<!--            <v-row-->
<!--              class="fill-height"-->
<!--              align="center"-->
<!--              justify="center"-->
<!--            >-->
<!--              <highlight-panel cls="dark" style="height:160px;" title="Aantal tickets verkocht in deze periode" :icon="require('@/assets/icons/tickets.svg')" :number="sold_ticket_amount" />-->
<!--            </v-row>-->

<!--          </v-carousel-item>-->
<!--           <v-carousel-item>-->
<!--              <highlight-panel cls="dark" style="height:160px;" title="Aantal tickets verkocht in deze periode" :icon="require('@/assets/icons/tickets.svg')" :number="sold_ticket_amount" />-->
<!--          </v-carousel-item>-->
<!--        </v-carousel>-->

<!--      </v-col>-->
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
        <highlight-panel cls="dark" style="height:160px;" :title="$t('Tickets sold this period')" :icon="require('@/assets/icons/tickets.svg')" :number="sold_ticket_amount" />
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
        <highlight-panel cls="dark" style="height:160px;" :title="$t('Earnings this period')" :icon="require('@/assets/icons/earnings.svg')" :number="revenue" />
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
        <highlight-panel cls="dark" style="height:160px;" :title="$t('Amount of visitors on this ticketshop')" :icon="require('@/assets/icons/visitors.svg')" :number="visitors" />
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
        <highlight-panel cls="dark" style="height:160px;" :title="$t('Conversion rate')" :icon="require('@/assets/icons/statistics.svg')" :number="conversion_rate+'%'" />
      </v-col>

    </v-row>
    <v-row>
      <v-col >
        <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <progress-line-chart-panel switcher="true" :data="chartParams"></progress-line-chart-panel>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 4">
        <top-list show-dropdown="true" ref="eventstoplist" :title="$t('Events top 10')"></top-list>
      </v-col>
      <v-divider vertical v-show="$vuetify.breakpoint.smAndUp" ></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 4">
        <gender-chart-panel switcher="true" :data="chartParams"></gender-chart-panel>
      </v-col>
      <v-divider vertical v-show="$vuetify.breakpoint.smAndUp"></v-divider>
      <v-col v-show="$vuetify.breakpoint.smAndDown">
        <v-divider></v-divider>
      </v-col>
      <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : 4">
        <age-gender-chart-panel :data="chartParams"></age-gender-chart-panel>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>



import dateDropdown from "@/components/core/dateDropdown";
import highlightPanel from "@/components/core/highlightPanel";
import genderChartPanel from "@/components/chartpanels/genderChartPanel";
import progressLineChartPanel from "@/components/chartpanels/progressLineChartPanel";
import topList from "@/components/core/topList";
import AgeGenderChartPanel from "@/components/chartpanels/ageGenderChartPanel";


export default {
  name: 'Home',
  components: {
    AgeGenderChartPanel,
    dateDropdown, highlightPanel, genderChartPanel,
    progressLineChartPanel, topList
  },
  mounted () {
    // this.preset_dates(this.default_preset_date)
    // this.$store.cache.dispatch('event/loadEvents')

    // store test
    // this.$store.cache.dispatch('event/loadTest')
    // this.$store.cache.dispatch('event/loadTest')
    // // this.$store.cache.delete('event/loadTest')
    // this.$store.cache.dispatch('event/loadTest')
    // this.testValue = this.$store.getters['event/getTest'];

    // this.$store.dispatch('event/setTest', 'yayyyyy')
    // this.testValue = this.$store.getters['event/getTest'];
  },
  methods:{
    reload_all_charts(start_date, end_date){
      this.chartParams = {
        'start_date': start_date,
        'end_date': end_date
      }
      this.date_filter.start_date = start_date;
      this.date_filter.end_date = end_date;
      this.load_top_panels()

      let params = {
        'start_date': this.date_filter.start_date,
        'end_date': this.date_filter.end_date

      }

      this.$refs.eventstoplist.load('stats/getTop5Chart', params)
      // this.load_top_5_chart(this.top_performing_menu_items[0])

    },
    load_top_panels(){

      let store_object = this.$store
      if(this.date_filter.preset_dates === this.default_preset_date){
        store_object = this.$store.cache;
      }
      let params = {'start_date': this.date_filter.start_date, 'end_date': this.date_filter.end_date}

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
    },

  },
  data: () => ({
    carousel_model:0,
    chartParams:{
      'start_date': '',
      'end_date': ''
    },
    default_preset_date: 'last_week',
    sold_ticket_amount:0,
    revenue:0,
    visitors:0,
    conversion_rate:0,

    date_filter:{
      start_date:'',
      end_date:''
    },

  })
}
</script>
