<template>
  <v-card>

    <v-navigation-drawer
      :permanent="$vuetify.breakpoint.mdAndUp"
      width="228"
      app
      mini-variant-width="120"
      v-model="$store.state.layout.navopen"
      :mini-variant="$vuetify.breakpoint.mdAndUp && $store.state.layout.navismini"
    >
      <v-img src="@/assets/logo_yt.svg" width="42" height="28" v-show="$store.state.layout.navismini" style="margin:0 auto;margin-top:20px"></v-img>
      <v-img src="@/assets/logo_yourtickets.svg" width="148" v-show="!$store.state.layout.navismini" style="margin:0 auto;margin-top:20px"></v-img>
      <v-btn class="text-decoration-underline" block href="/dashboard" style="font-size:12px!important;letter-spacing: normal" text plain color="white" >{{ $t('To the old dashboard') }}</v-btn>

      <v-list dense :style="$vuetify.breakpoint.smAndDown ? '' : 'margin-top:94px;'">
        <template v-for="item in items">
          <template v-if="item.isPanel && !$store.state.layout.navismini">

            <div style="padding-left:20px;padding-right:20px;" :key="item.text" :to="item.link">
              <v-expansion-panels flat>
                <v-expansion-panel class="rounded-lg" @click="collapse_toggle">
                  <v-expansion-panel-header :class="events_collapsed ? 'active': ''">
                      <v-img src="@/assets/icons/menu/events.svg" max-width="24" style="margin-right:10px;"></v-img>
                      Events
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <v-card class="rounded-0" elevation="0" dark>
                      <v-card-text style="padding:8px;padding-left:18px;">
                        <v-text-field
                            v-model="event_search"
                            class="nav_search"
                            flat
                            outlined
                            :placeholder="$t('Search for event')+'...'"
                          ></v-text-field>

                      </v-card-text>
                    </v-card>
                    <v-card style="padding-left:0px;margin-top:2px;max-height: 160px;overflow-y: scroll;" class="rounded-0" elevation="0" dark>
                      <v-card-text>
                        <v-list dense v-for="item in event_list" :key="item.pk">

                          <v-list-item :to="{name:'event_dashboard', params:{id:item.pk}}" link class="event_list_item">{{item.title}}</v-list-item>
                        </v-list>

                      </v-card-text>
                    </v-card>
                    <v-btn :to="item.link" elevation="0" block color="#363A4F" class="rounded-0 rounded-b-lg" style="margin-top:2px;color:white;height:50px!important;">
                      {{ $t('Show all events') }}
                      
                      <v-img class="justify-end" style="width:12px;height:12px;color:white;" contain src="@/assets/icons/chevron_right.svg"></v-img>
                    </v-btn>


                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>
          </template>
          <template v-else>
            <v-list-item :key="item.text" :to="item.link" link>
              <v-list-item-action style="color:white;height:auto!important;" class="align-center" >
                <v-img :src="require('@/assets/icons/menu/' + item.icon + '.svg')"></v-img>
                <div v-if="$store.state.layout.navismini" style="margin-top:10px">{{ item.text }}</div>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>
                  {{ $t(item.text) }}
                </v-list-item-title>

              </v-list-item-content>

            </v-list-item>
          </template>

        </template>
      </v-list>
      <template v-slot:append>
        <div class="btn-container">
          <create_event responsive="true"></create_event>
          <v-btn :block="$store.state.layout.navismini" target="_blank" href="/contact" class="secondary_btn" style="margin-right: 8px;margin-top:8px;">
            {{$t('Help')}}
          </v-btn>
          <v-btn @click="openappwindow" class="secondary_btn" style="margin-top: 8px;" v-show="!$store.state.layout.navismini" >
            {{$t('Download app')}}
          </v-btn>
          <v-btn plain v-ripple="false" @click="togglenav" style="margin-top: 8px;margin-bottom:16px;">
            {{collapse_text_collapse}}
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </v-card>
</template>
<script>
  import create_event from "@/components/dialogs/create_event";
  import { mapGetters } from "vuex"

  export default {
    name:'LeftMainNavigation',
    components: {
      create_event
    },
    mounted (){
      this.$store.dispatch('event/loadEvents')

    },
    methods: {
      togglenav() {
        this.$store.commit('layout/navismini',!this.$store.state.layout.navismini)
      },
      collapse_toggle(){
        this.events_collapsed = this.events_collapsed ? false : true;
      },
      filter_events(){

        if(this.event_search === ''){
          this.event_list = this.events
        }else {
          this.$store.dispatch('event/getFilteredEvents', this.event_search)
              .then(response => {
                this.event_list = response.data
              })
        }
      },
      openappwindow(){
        window.open("https://apps.apple.com/nl/app/yourtickets/id1126030142", "_blank");
      }
    },
    computed:{
      ...mapGetters({
        events: 'event/getEvents'
      }),
      collapse_text_event(){
        return this.$store.state.layout.navismini === false ? '+ ' + this.$t('New event') : '+ ' + this.$t('Event')
      },
      collapse_text_collapse(){
        return this.$store.state.layout.navismini === false ? '< ' + this.$t('Collapse') : this.$t('Expand') + ' >'
      },

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
      'events'(){
        this.filter_events()
      }
    },
    data: () => ({
      events_collapsed:false,
      showEventNavigation:false,
      event_search:'',
      event_list:[],
      event:{
        title:'',
        location:'',
        start_date:'',
        header_img:'test.img'
      },
      items: [
        { icon: 'home', text: 'Dashboard', link: '/' },
        { icon: 'events', text: 'Events >' ,link: '/events', isPanel: true},
        { icon: 'stats', text: 'Statistics',link: '/stats'  },
        { icon: 'multishop', text: 'Multi shop',link: '/multishop'  },
      ],
    }),
  }
</script>
