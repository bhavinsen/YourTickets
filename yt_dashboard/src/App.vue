<template>
  <v-app id="inspire">
    <v-overlay :value="account_menu_open && $vuetify.breakpoint.mdAndDown" ></v-overlay>
    <v-snackbar
        :timeout="timeout"
        v-model="snackbar"
        color="green"
        top
    >
      <v-icon>mdi-check-outline</v-icon>
      <div class="ml-5 d-inline text-h5">{{snackbar_text}}</div>
    </v-snackbar>

    <v-app-bar
      color="accent-4"
      fixed
      app
      v-if="$vuetify.breakpoint.smAndDown"
    >
      <v-app-bar-nav-icon @click.stop="togglenav"></v-app-bar-nav-icon>
      <v-spacer></v-spacer>

      <v-avatar
        color="#C4C4C4"
        size="40"
       class="account_activator"
      >
        <img :src="account.avatar">
      </v-avatar>

    </v-app-bar>
    <LeftMainNavigation></LeftMainNavigation>
    <v-main :style="{background: '#EDF5F7'}">
      <v-dialog v-model="delete_dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline text-center">{{ $t('Are you sure you want to delete this event?')}}</v-card-title>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="secondary_btn blue" text @click="delete_dialog = false">{{ $t('Cancel') }}</v-btn>
            <v-btn class="primary_btn" text @click="deleteItem">{{ $t('Ok') }}</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="not_publishable_dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline text-center justify-center">{{ $t('Your event is not published yet') }}</v-card-title>
          <v-card-text class="text-center">
            {{ $t('Click on change event to publish the ticketshop') }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="secondary_btn blue" text @click="not_publishable_dialog = false">{{ $t('Cancel') }}</v-btn>
            <v-btn class="primary_btn" text @click="showEditTicketshopPopup">{{ $t('Change event') }}</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-container class="main-layout-panel"  fluid :style="$vuetify.breakpoint.mdAndUp ? 'padding:24px;' : ''">
        <v-row :style="getBarHeight" v-if="$vuetify.breakpoint.mdAndUp">
          <v-col cols="7" style="padding-top:30px;">
            <div v-if="!getEventPage"  style="font-size:18px;">
              <div style="font-size:24px;">{{ time_based_greeting }} <b>{{ account.first_name }}</b>,</div>
              {{ $t('These are the latest developments of your events') }}<br> {{ $t('between') }} {{formatDate(startDate)}} {{ $t('to') }} {{formatDate(endDate)}}</div>
            <div v-if="getEventPage" style="font-size:12px;">
              <div style="font-size:24px;font-weight:bold;">{{event.title}} </div>
              <div style="position:relative;margin-top:12px;">
                <img src="@/assets/icons/calendar_black.svg" style="width: 20px;height:20px;">
                <div class="d-inline-block" style="left:26px;top:2px;position:absolute;">
                  {{ $t('Takes place from {startdate} {starttime}', {'startdate': formatted_date, 'starttime':event.start_time})}}
                </div>
              </div>
              <div style="margin-top:12px; position:relative;">
                <img src="@/assets/icons/location.svg" style="width: 20px;height:20px;">
                <div class="d-inline-block" style="left:26px;top:2px;position:absolute;">
                  {{ $t('The {location} is the location of this event',{'location': event.location}) }}
                </div>
              </div>
            </div>
          </v-col>
          <v-col cols="5" class="text-md-right">

            <account_dialog @hide_dialog="show_account_edit_dialog = false" :show_dialog="show_account_edit_dialog"></account_dialog>

            <create_event></create_event>
            <balance_request_payout @hide="show_balance_request_payout=false" :show_dialog="show_balance_request_payout"></balance_request_payout>
            <v-btn class="secondary_btn blue" elevation="0" @click="show_balance_request_payout=true" style="margin-right:16px;">
              {{ $t('Balance') }}: &euro; {{account.saldo}}
            </v-btn>
            <v-avatar
              color="#C4C4C4"
              size="40"
              @click="account_menu_open=true"
              class="account_activator"
            >
        <img :src="account.avatar">
      </v-avatar>



          </v-col>
        </v-row>
          <v-menu
                :close-on-content-click="false"
                offset-y
                :min-width="$vuetify.breakpoint.mdAndDown ? '100%' : ''"
                :top="$vuetify.breakpoint.mdAndUp" :left="$vuetify.breakpoint.mdAndUp"

                activator=".account_activator"
            >

<!--              <template v-slot:activator="{ on, attrs }">-->
<!--                <v-avatar-->
<!--                  v-bind="attrs"-->
<!--                  v-on="on"-->
<!--                  color="#C4C4C4"-->
<!--                  size="40"-->
<!--                >-->
<!--                  <img :src="account.avatar">-->
<!--                </v-avatar>-->
<!--              </template>-->
              <v-card :width="$vuetify.breakpoint.mdAndDown ? '100%' : '537'"  style="padding:8px;">
                <v-card-text style="padding:0px!important;">
                  <v-container fluid>
                    <v-row>
                      <v-col cols="7">
                        <h2 class="header-text" style="color: #66C5E1;margin-top:16px;">{{ $t('Notifications') }}</h2>
                        <v-divider class="grey" style="margin:16px;margin-left:0px;"></v-divider>
                        {{ $t('You dont have any notifications, you are up to date!') }}
                      </v-col>
                      <v-divider vertical class="grey" inset style="position:relative;right:8px;"></v-divider>
                      <v-col cols="5" class="text-right">
                        <div class="d-flex justify-end">
                          <div class="d-flex align-center">
                            <div style="margin-right:8px;">
                              {{ $t('You are logged in as') }}
                            <br/>
                            <div class="d-inline-block">
                              {{account.first_name}}
                            </div>
                              </div>
                          </div>
                          <div class="d-flex">
                            <v-avatar
                          >
                            <img :src="account.avatar">
                          </v-avatar>
                          </div>
                        </div>
                        <div style="margin-top:16px;">
                          <create_event ></create_event>
                        </div>
                        <v-btn block class="secondary_btn blue" @click="show_balance_request_payout=true" elevation="0" style="margin-top:8px;">
                          {{ $t('Balance') }} &euro; {{account.saldo}}
                        </v-btn>
                        <v-divider style="margin-top:16px;margin-bottom:8px;"></v-divider>

                        <v-btn @click="show_account_edit_dialog = true" block class="secondary_btn blue" elevation="0">
                          <img width="16" style="margin-right:4px;" contain src="@/assets/icons/settings.svg">
                          <template v-if="$vuetify.breakpoint.mdAndUp">{{ $t('-account-settings-popup-title') }}</template>
                          <template v-if="$vuetify.breakpoint.smAndDown">{{ $t('-account-settings-popup-title-short') }}</template>
                        </v-btn>
                        <v-btn @click="logout" block class="secondary_btn blue" elevation="0" style="margin-top:8px;">
                          {{ $t('Logout') }}
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
              </v-card>
            </v-menu>
        <v-row style="padding:16px;padding-bottom:0px;">
          <v-col :cols="$vuetify.breakpoint.smAndDown ? 6 : 12">
            <div v-if="getEventPage && $vuetify.breakpoint.mdAndUp" style="font-size:12px;">
              <div style="position:relative;" class="d-flex">
                <event_visitors v-if="event.shared_event === 'false'"></event_visitors>
                <event_sales_channels v-if="event.shared_event === 'false'"></event_sales_channels>
                <v-btn class="secondary_btn blue" elevation="0" style="margin-right:12px;" @click="openTicketshop()">
                  {{ $t('Go to ticketshop') }}
                  </v-btn>
                <create_event v-if="event.shared_event === 'false'" editmode="true" :activeTab="editPopupTab" @close="showEditPopup=false" :manuallyShow="showEditPopup"></create_event>

                  <v-menu v-if="getEventPage && event.shared_event === 'false'" :close-on-content-click="true" offset-y bottom left v-model="publishUnpublishMenuOpen" >

                    <template v-slot:activator="{ on, attrs }">
                      <v-btn class="secondary_btn blue ml-auto"  text v-bind="attrs" v-on="on" elevation="0">
                        <v-icon style="margin-right:10px;" :color="publishUnpublishItems[publishUnpublishActive].iconColor" small >{{ publishUnpublishItems[publishUnpublishActive].icon }}</v-icon>
                        <template v-if="event.event_public">
                          {{ $t('Event Online') }}
                        </template>
                        <template v-else>
                          {{ $t('Event Offline') }}
                        </template>
                        <v-img class="ml-2" contain height="10" src="@/assets/icons/chevron_down.svg"></v-img>
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-text style="padding:10px!important;">

                        <v-list class="btn-list-popup">
                          <v-list-item-group v-model="publishUnpublishActive" @change="togglePublish">
                            <template v-for="(item, i) in publishUnpublishItems" >
                              <v-list-item active-class="item-small-custom" :key="i" v-show="publishUnpublishActive !== i" >

                                <v-icon style="margin-right:10px;" :color="item.iconColor" small >{{ item.icon }}</v-icon> {{ item.text }}

                              </v-list-item>
                            </template>
                          </v-list-item-group>
                        </v-list>
                        </v-card-text>
                    </v-card>
                  </v-menu>

              </div>

            </div>
            <div v-if="getEventPage && $vuetify.breakpoint.smAndDown">
              <event_visitors block v-if="event.shared_event === 'false'"></event_visitors>
            </div>
          </v-col>
          <v-col v-if="getEventPage && $vuetify.breakpoint.smAndDown" :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
            <event_sales_channels v-if="event.shared_event === 'false'"></event_sales_channels>
          </v-col>
          <v-col v-if="getEventPage && $vuetify.breakpoint.smAndDown" :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
            <v-btn :block="$vuetify.breakpoint.smAndDown" class="secondary_btn blue" elevation="0" style="margin-right:12px;" @click="openTicketshop()">{{ $t('Go to ticketshop') }}</v-btn>
          </v-col>
          <v-col v-if="getEventPage && $vuetify.breakpoint.smAndDown" :cols="$vuetify.breakpoint.smAndDown ? 6 : 3">
            <create_event v-if="event.shared_event === 'false'" editmode="true" :activeTab="editPopupTab" @close="showEditPopup=false" :manuallyShow="showEditPopup"></create_event>
          </v-col>
          <v-col cols="6" offset-sm="6" class="text-right" v-if="getEventPage && $vuetify.breakpoint.smAndDown && event.shared_event === 'false'">
            <v-menu v-if="getEventPage" :close-on-content-click="true" offset-y bottom left v-model="publishUnpublishMenuOpen" >

              <template v-slot:activator="{ on, attrs }">
                <v-btn class="secondary_btn blue" block  text v-bind="attrs" v-on="on" elevation="0">
                  <v-icon style="margin-right:10px;" :color="publishUnpublishItems[publishUnpublishActive].iconColor" small >{{ publishUnpublishItems[publishUnpublishActive].icon }}</v-icon>
                  <template v-if="event.event_public">
                      {{ $t('Event Online') }}
                  </template>
                  <template v-else>
                      {{ $t('Event Offline') }}
                  </template>
                  <v-img class="ml-2" contain height="10" src="@/assets/icons/chevron_down.svg"></v-img>
                </v-btn>

              </template>
              <v-card>
                <v-card-text style="padding:10px!important;">

                  <v-list class="btn-list-popup">
                    <v-list-item-group v-model="publishUnpublishActive" @change="togglePublish">
                      <template v-for="(item, i) in publishUnpublishItems" >
                        <v-list-item active-class="item-small-custom" :key="i" v-show="publishUnpublishActive !== i" >

                          <v-icon style="margin-right:10px;" :color="item.iconColor" small >{{ item.icon }}</v-icon> {{ item.text }}

                        </v-list-item>
                      </template>
                    </v-list-item-group>
                  </v-list>
                  </v-card-text>
              </v-card>
            </v-menu>
          </v-col>
        </v-row>
        <v-row style="padding-right:16px;">

        </v-row>
        <v-row>

          <v-col>
            <v-card class="main-layout-panel" elevation="0" style="padding:8px;">
              <router-view></router-view>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style lang="scss">
  @import 'scss/override.scss';
</style>

<script>
  import LeftMainNavigation from './components/layout/left_main_navigation.vue'
  import create_event from "@/components/dialogs/create_event";
  import { mapState, mapGetters } from "vuex"
  import event_visitors from "@/components/dialogs/event_visitors";
  import event_sales_channels from "@/components/dialogs/event_sales_channels";
  import balance_request_payout from "@/components/dialogs/balance_request_payout";
  import account_dialog from "@/components/dialogs/account_dialog";

  export default {
    components:{
      LeftMainNavigation,
      create_event,
      event_visitors,
      event_sales_channels,
      balance_request_payout,
      account_dialog
      // Appbar
    },
    mounted() {
      
      this.$store.subscribe((mutation) => {
        if(mutation.type === 'messages/add'){
          this.snackbar_text = mutation.payload.text
          this.snackbar = true
          this.$store.dispatch('messages/remove', mutation.payload)
        }

      })

      this.$store.dispatch('account/load')

    },

    methods: {
      togglePublish(el){
        if(el === 2){
          //weet je zeker?
          this.delete_dialog = true;
          //goto route dashboard
        }
        else if(this.event.event_public){
          this.$store.dispatch('event/unpublish', this.event.id)
          this.$store.dispatch('messages/add', {'text': this.$t('-message-notification-unpublished')})
        }else{
          this.$store.dispatch('event/publish', this.event.id)
          this.$store.dispatch('messages/add', {'text': this.$t('-message-notification-published')})
        }
      },

      async deleteItem(){
        await this.$store.dispatch('event/delete', this.event.id)
        this.delete_dialog = false
        await this.$router.push({ name:'home', replace: true })
      },
      togglenav() {
        
        this.$store.commit('layout/navopen',!this.$store.state.layout.navopen)
      },
      logout(){
        this.$store.dispatch('account/logout')
        .then(() => {
          localStorage.removeItem('t');
          window.location.reload();
          // this.$router.push({'name': 'login'})
        })
        .finally(() => this.loading = false)
      },
      openTicketshop(){
        // this.$i18n.locale = 'en'
        // DONT COMMIT THIS
        if(this.event.event_public) {
          window.open(this.event.url)
        }else if(this.event.can_be_published.status === false){
          this.not_publishable_dialog = true
        }
      },
      showEditTicketshopPopup(){
        this.showEditPopup = this.event.can_be_published.tab
        this.not_publishable_dialog = false
      },
      formatDate (date) {

        if (!date) return null

        const [year, month, day] = date.split('-')
        return `${day}-${month}-${year}`
      },
    },
    computed:{
      ...mapGetters({
        getEventPage: 'layout/getEventPage',
        getEventId: 'layout/getEventId',
        account: 'account/getall',
        startDate: 'layout/getStartDate',
        endDate: 'layout/getEndDate',
        event: 'event/getEvent',

      }),
      ...mapState({
        // event: (state) => state.event.event,
      }),
      getBarHeight(){
        if(this.getEventPage){
          return 'height:150px;'
        }
        return 'height:133px;'
      },
      formatted_date(){
        let date = new Date(this.event.start_date)
        const monthNames = [
          this.$t('January'), this.$t('February'), this.$t('March'), 
          this.$t('April'), this.$t('May'), this.$t('June'),
          this.$t('July'), this.$t('August'), this.$t('September'), this.$t('October'), 
          this.$t('November'), this.$t('December')
          
        ];
        return date.getDate() + ' ' + monthNames[date.getMonth()] + ' ' + date.getFullYear()
      },
      theme(){
        return (this.$vuetify.theme.dark) ? 'dark' : 'light'
      },
      time_based_greeting(){
        var today = new Date()
        var curHr = today.getHours()

        if (curHr < 12) {
         return this.$t("Good morning")
        } else if (curHr < 18) {
          return this.$t("Good afternoon")
        } else {
          return this.$t("Good evening")
        }
      },
      publishUnpublishActive:{

        get(){
          if(this.event.event_public){
            return 0
          }else{
            return 1
          }
        },
        set(){

        }
      }
    },
    data: (scope) => ({
      not_publishable_dialog:false,
      showEditPopup:false,
      editPopupTab:1,
      delete_dialog:false,
      // publishUnpublishActive:0,
      publishUnpublishMenuOpen:false,
      publishUnpublishItems:[
        {text: scope.$t('-publish-dropdown-online'), icon:'mdi-circle', iconColor:'green'},
        {text: scope.$t('-publish-dropdown-offline'),  icon:'mdi-circle', iconColor:'orange'},
        {text: scope.$t('-publish-dropdown-remove'),  icon:'mdi-circle', iconColor:'red'}
      ],
      show_balance_request_payout:false,
      account_edit_mode:false,
      snackbar:false,
      timeout:3000,
      snackbar_text:'',
      show_account_edit_dialog:false,
      account_menu_open:false,
    }),
  }
</script>
