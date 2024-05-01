<template>

  <v-dialog scrollable v-model="show_dialog" width="802" :fullscreen="$vuetify.breakpoint.smAndDown" eager  content-class="overflow-visible" >

    <template v-slot:activator="{ on, attrs }">
      <v-btn :block="$vuetify.breakpoint.smAndDown" v-bind="attrs" elevation="0" v-on="on"

             :class="$vuetify.breakpoint.smAndDown ? 'secondary_btn blue' : 'primary_btn'"
             style="margin-right:15px;">
      {{ $t('Visitors') }}
      </v-btn>
    </template>


    <v-card >

        <v-btn @click="show_dialog = false" v-show="$vuetify.breakpoint.mdAndUp" icon class="close_button"><v-img src="@/assets/icons/close.svg"></v-img></v-btn>
        <v-btn @click="show_dialog = false" icon v-show="$vuetify.breakpoint.smAndDown" class="close_button_mobile"><v-icon>mdi-close</v-icon></v-btn>

        <v-toolbar dense flat :style="$vuetify.breakpoint.smAndDown ? 'margin-bottom:8px;margin-top:38px' : 'margin-bottom:8px;margin-top:21px'" >
          <v-toolbar-title>
            {{ $t('Visitors') }}
          </v-toolbar-title>
        </v-toolbar>
        <div class="d-flex" style="margin-left:12px!important;margin-right:24px!important;margin-bottom:12px">
          <v-btn elevation="0" class="primary_btn" @click="downloadCsv" style="margin-right:16px;">
            <v-icon style="margin-right:6px;">mdi-tray-arrow-down</v-icon>
            {{ $t('Download CSV') }}
            
          </v-btn>
          <v-btn elevation="0"  class="primary_btn" @click="openGuestlistRow">
            <img style="margin-right:6px;" src="@/assets/icons/plus.svg" >
            <template v-if="$vuetify.breakpoint.smAndDown">
              {{ $t('Send Guest Ticket') }}
            </template>
            <template v-else>
              {{ $t('Send guestlist invitation') }}
            </template>
            
          </v-btn>
        </div>
        <v-divider style="margin-left:20px;margin-right:20px;"></v-divider>
        <v-card-text style="height:100%;padding-left:24px!important;padding-right:24px!important;">

          <v-data-table
              hide-default-footer
              :headers="table.headers"
              :items="eventTickets.tickets"
              disable-sort
              class="custom_dense"
              single-expand
              show-expand
              :expanded.sync="expandedItems"
              mobile-breakpoint="0"
              
          >

            <template v-slot:item.data-table-expand="{ item, isExpanded, expand }">
              <v-btn icon @click="expand(true); loadDataOnExpand(item)" v-if="!isExpanded">
                <v-img contain height="10" src="@/assets/icons/chevron_right_black.svg"></v-img>
              </v-btn>
              <v-btn icon @click="expand(false);" v-if="isExpanded">
                <v-img contain height="6" src="@/assets/icons/chevron_down.svg"></v-img>
              </v-btn>
            </template>

            <template v-slot:expanded-item="{ headers, item }">
                  <td :colspan="headers.length">
                    {{item.name}}
                  </td>
            </template>
            <template v-slot:item.amount_sold="{ item }">
              {{item.amount_sold}} <span style="font-size:9px;color:#66C5E1;">/ {{item.amount_available}}</span>
            </template>
            <template v-slot:item.ticket_price="{ item }">
              &euro;{{item.ticket_price}}
            </template>
            <template v-slot:item.total_amount_price="{ item }">
              &euro;{{item.total_amount_price}}
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn elevation="0" x-small text class="primary_btn" @click="downloadCsvPerTicket(item)" >
                  <v-icon size="20">mdi-tray-arrow-down</v-icon>
                </v-btn>
                

            </template>
            <template slot="body.append">
                  <tr>
                      <td></td>
                      <td class="text-start"> {{ $t('Totals') }}</td>
                      <td>{{eventTickets.total_tickets_sold}}</td>
                      <td></td>
                      <td>&euro;{{eventTickets.total_amount}}</td>
                      <td></td>
                  </tr>
            </template>
            <template v-slot:expanded-item="{ headers }">
              <td :colspan="headers.length">
                  <edit_table
                    :headers="getHeaders"
                    :default-item="editTable.defaultItem"
                    :items="editTable.items"
                    :disable-edit="true"
                    style="margin-left:10px;"
                    :loading="tableLoading"
                    @delete_item_confirmed="deleteTicket"
                    height="300"
                    ref="guestlistedit"
                  >
                  <template v-slot:item.name="{ item }">
                      <div class="text-truncate" >
                        {{ item.name }}
                      </div>
                  </template>
                  <template v-slot:item.email="{ item   }">
                    <div class="text-truncate" >
                       {{ item.email }}
                    </div>
                  </template>
                  <template v-slot:item.gender="{ item   }">

                      <template v-if="item.gender === 'F'">V</template>
                      <template v-else>M</template>
                  </template>

                </edit_table>
              </td>
            </template>
          </v-data-table>
        </v-card-text>
        <v-divider class="d-block" style="margin-left:15px;margin-right:15px;"></v-divider>
        <v-card-actions fixed v-if="showFooterForm">

          <v-form>
            <v-container fluid>
              <v-row>
                <v-col cols="4" >
                  <v-text-field single-line dense
                          outlined
                          placeholder="Naam"
                          v-model="addItemObject.name"></v-text-field>
                </v-col>
                <v-col cols="4">
                          <v-text-field single-line dense
                          outlined
                          placeholder="Email"
                          v-model="addItemObject.email"></v-text-field>
                </v-col>
                <v-col cols="4">
                  <div class="d-flex justify-center" style="padding-top:5px;">
                    <div class="d-flex" style="margin-right:4px" >M</div>
                    <v-switch
                      v-model="addItemObject.gender"
                      class="small d-flex"
                      false-value="M"
                      true-value="V"
                      style="margin-top:0px!important;"
                    ></v-switch>
                    <div class="d-flex" style="margin-left:4px" >V</div>
                  </div>
                        
                </v-col>
                <v-col cols="12" class="text-right">
                  <v-btn class="primary_btn d-inline-block" small elevation="0" @click="addd()">{{ $t('Send') }}</v-btn>
                </v-col>
              </v-row>
            </v-container>


      </v-form>

        </v-card-actions>
    </v-card>

  </v-dialog>

</template>

<script>

import {mapGetters} from "vuex";
import edit_table from "@/components/event/edit/edit_table";
import Api from '@/service/Api.js'

export default {
  name: 'event_visitors',
  components:{
    edit_table
  },
  methods: {
    addd(){
      
      this.openGuestlistRow()
      this.$nextTick(() => {
        this.editTable.items.push(this.addItemObject)
        this.sendTicket(this.addItemObject)
        this.addItemObject = Object.assign({}, this.editTable.defaultItem)
      })
    },
    openGuestlistRow(){
      this.expandedItems = []
      let item = this.eventTickets.tickets[this.eventTickets.tickets.length -1]
      this.expandedItems.push(item)
      this.loadDataOnExpand(item)
      this.showFooterForm = true
    },
    downloadCsv(){
      window.open(Api().defaults.baseURL+ '/api/event/'+this.$route.params.id+'/visitors/download')
    },
    downloadCsvPerTicket(ticket){
      // console.log(ticket)
      window.open(Api().defaults.baseURL+ '/api/event/'+this.$route.params.id+'/visitors/download/'+ticket.id)
    },
    loadDataOnExpand(item){
      // expand(true);
      this.tableLoading = true;
      this.expandedItem = item;
      // reset the items so that it collapse faster
      this.editTable.items = []

      if(item.id === 'guest_ticket'){
        this.showAddForm = true;
      }else{
        this.showAddForm = false;
      }
      // getVisitorsForTicket
      this.$store.dispatch('event_visitors/getVisitorsForTicket', {'id': this.$route.params.id, 'ticket_id': item.id}).then((response)=>{
        this.editTable.items = response.data.data
        this.tableLoading = false;
      })
    },
    sendTicket(item){

      this.$store.dispatch('event_visitors/sendSingleTicket', {
        'event_id': this.$route.params.id,
        'name':item.name,
        'email':item.email,
        'gender':item.gender

      })
    },
    deleteTicket(item){
      this.$store.dispatch('event_visitors/deleteGuestlistTicket', {
        'event_id': this.$route.params.id,
        'ticket_id':item.id
      })
    },

    load(){
      this.$store.dispatch('event_visitors/loadEventTickets', this.$route.params.id)
    }
  },
  computed:{
    ...mapGetters({
      eventTickets: 'event_visitors/getEventTickets',
    }),
    getHeaders(){
      // headerNoActions
      if(this.expandedItem.id === 'guest_ticket'){
        return this.editTable.headers
      }
      return this.headersNoActions
    },
  },
  watch:{
    'show_dialog'(val) {
      if(val === true){
        this.load()
      }
    }
  },
  data: (scope) => ({
      showFooterForm: false,
      expandedItems:[],
      show_dialog:false,
      expanded:false,
      expandedItem:{},
      showAddForm:false,
      tableLoading:false,
      addItemObject:{
        name:'',
        email:'',
        gender:'M',
      },
      editTable:{
        defaultItem:{
        'name':'',
        'email':'',
        'gender':'M',
        },
        items:[],
        headers:[
          {text: scope.$t('Name'), align: 'start',value: 'name'},
          {text: scope.$t('Email'), value: 'email',  sortable: false },
          {text: scope.$t('Gender'), value: 'gender', align:'center',  sortable: false },
          {text: '', value: 'actions',  sortable: false },
        ]
      },
      headersNoActions:[
          {text: scope.$t('Name'),align: 'start',value: 'name',width:'150px'},
          {text: scope.$t('Email'), value: 'email', width:'150px', sortable: false },
          {text: scope.$t('Gender'), value: 'gender', align:'center', width:'100px', sortable: false },
        ],
      table:{
        items:[],
        headers:[
          {text: scope.$t('Tickettype'), align: 'start', value: 'name',},
          {text: scope.$t('Ticket amount'), align: 'start', value: 'amount_sold', sortable: false },
          {text: scope.$t('Price per ticket'), align: 'start', value: 'ticket_price', sortable: false },
          {text: scope.$t('Total amount'), align: 'start', value: 'total_amount_price', sortable: false },
          {text: '', value: 'actions',  sortable: false,  align:'end' },
          ]
      },

  })
}
</script>