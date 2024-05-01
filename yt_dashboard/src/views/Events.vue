<template>
  <v-container
    fluid
  >
    <v-row>

      <v-col cols="12">
        <create_event></create_event>
      </v-col>
      <v-col cols="12">
        <v-form>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            :placeholder="$t('Search by event or location')"
            outlined
            flat
            hide-details
            style="width:100%"

          ></v-text-field>
        </v-form>
      </v-col>



      <v-col cols="12">
    <panel>
        <v-data-table
          :headers="$vuetify.breakpoint.smAndDown ? mobile_headers : headers"
          :items="events"
          item-key="id"
          class="elevation-0 scroll-table"
          :loading="loading"
          :search="search"
          mobile-breakpoint="0"
          :footer-props="{
        
           'items-per-page-text':'',
          }"
        >
          <template v-slot:item.title="{ item }">
            <router-link :to="{ name: 'event_dashboard', params: { id: item.pk }}">{{item.title}}</router-link>
            <template v-if="item.shared_event === 'true'"> ({{$t('Shared with you')}})</template>
          </template>
          <template v-slot:item.event_public="{ item }">
            <v-icon v-if="item.event_public" color="green">mdi-eye</v-icon>
            <v-icon v-else-if="!item.event_public">mdi-eye-off</v-icon>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-btn :href="item.url" target="_blank" text x-small v-if="item.event_public">{{$t('ticketshop')}}</v-btn>
          </template>
        </v-data-table>


    </panel>
      </v-col>
    </v-row>
  </v-container>

</template>

<script>

import {mapGetters} from "vuex";
import create_event from "@/components/dialogs/create_event";

export default {
  name: 'Events',
  components:{create_event},
  mounted () {
    this.$store.cache.dispatch('event/loadEvents')

  },
  computed: {
    ...mapGetters({
      events: 'event/getEvents'
    }),
  },
  data: (scope) => ({
    search:'',
    loading: false,
    title:'',
    headers: [
      {
        text: 'Event',
        sortable: false,
        value: 'title',
      },
      { text: scope.$t('Location'), value: 'location' },
      { text: scope.$t('Start date'), value: 'start_date', filterable:false },
      { text: scope.$t('Public'), value: 'event_public', filterable:false},
      { text: scope.$t('actions'), value:'actions', filterable:false}
    ],
    mobile_headers: [
    {
        text: 'Event',
        sortable: false,
        value: 'title',
      },
      { text: scope.$t('Start date'), value: 'start_date', filterable:false },
      { text: scope.$t('actions'), value:'actions', filterable:false}
    ]


    }),
}
</script>