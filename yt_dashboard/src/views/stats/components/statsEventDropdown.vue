<template>
  <v-menu :close-on-content-click="false" offset-y bottom right v-model="menu_open" >

    <template v-slot:activator="{ on, attrs }">
      <v-btn class="primary_btn" :class="menu_open ? 'dark' : ''" v-bind="attrs" v-on="on" elevation="0">
        <template v-if="selected_event.title">
          {{selected_event.title}}
        </template>
        <template v-else-if="dropdownTitle">
          {{dropdownTitle}}
        </template>
        <template v-else>{{$t('Select event')}}</template>

        <v-img class="ml-2" contain height="10" src="@/assets/icons/chevron_down_white.svg"></v-img>
      </v-btn>

    </template>
    <v-card dark style="background-color:#363A4F!important;" flat elevation="0" class="elevation-0" width="280" height="260">
      <v-card-text style="padding:0px!important;">
        <v-container fluid>
          <v-form >
            <v-row>
              <v-col cols="12">
                <v-text-field
                  single-line
                  dense
                  outlined
                  :placeholder="$t('Event name')"
                  autofocus
                  v-model.trim="event_search"
                  ref="lineup_artist"
                  hide-details

                  class="white"


                ></v-text-field>



              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" style="padding-top:0;" >
                <div style="background-color:white;border-radius: 4px; height:204px;overflow-y: scroll;">
                  <v-card light style="padding-left:0px;margin-top:2px;max-height: 204px;" class="rounded-0" elevation="0">
                      <v-card-text style="padding:8px;padding-top:0;">
                        <v-list>
                          <div v-for="item in event_list" :key="item.pk">
                            <v-list-item @click="select_event(item)"  class="stats-dropdown-event-list d-block" >
                              <div class="d-block"><b>{{item.title}}</b></div>
                              <div class="d-block">{{$t('Date')}}:{{item.start_date}} {{$t('Location')}}: {{item.location}}</div>

                            </v-list-item>
                            <v-divider style="margin-bottom:4px;margin-top:4px;"></v-divider>
                          </div>

                        </v-list>

                      </v-card-text>
                    </v-card>

                </div>

              </v-col>
            </v-row>

            </v-form>
        </v-container>
      </v-card-text>
    </v-card>
  </v-menu>


</template>
<script>
  import {mapGetters} from "vuex";


  export default {
    name: 'statsEventDropdown',
    emits: ['select_event'],
    props:['dropdownTitle'],
    mounted (){
      this.$store.cache.dispatch('event/loadEvents')
      this.filter_events()

    },
    methods:{
      select_event(item){
        this.selected_event = item;
      },
      filter_events(){

        if(this.event_search === ''){
          this.event_list = this.events
          // this.selected_event = this.events[0]
        }else {
          this.$store.dispatch('event/getFilteredEvents', this.event_search)
            .then(response => {
              this.event_list = response.data
          })
        }
      },
    },
    computed: {
      ...mapGetters({
        events: 'event/getEvents'
      }),
    },
    watch: {
      'events_collapsed' (val) {
        if(val){
          this.filter_events();

        }
      },
      'event_search' () {
        this.filter_events()
      },
      'selected_event'(){

        this.$emit('select_event', {'event': this.selected_event})
      }
    },
    data: () => ({
      menu_open:false,
      some:'',
      event_search:'',
      selected_event:{},
      event_list:[]
    })
  }
</script>
