<template>

  <v-container
    fluid

  >
    <v-row>

      <v-col cols="12">
        <v-btn elevation="0" class="primary_btn" @click="createMultishop">{{$t('Add ticketshop')}}</v-btn>
      </v-col>

      <v-col cols="12">

          <panel>
              <v-data-table
                  :headers="$vuetify.breakpoint.smAndDown ? mobile_headers : headers"
                  :items="multiticketshops"
                  item-key="id"
                  :loading="loading"
                  single-expand
                  show-expand
                  flat
                  :expanded.sync="expanded"
                  mobile-breakpoint="0"
                  class="multishop_table"

              >

                <template v-slot:item.data-table-expand="{ item, isExpanded, expand }">
                  <v-btn icon @click="expand(true)" v-if="!isExpanded">
                    <v-img contain height="10" src="@/assets/icons/chevron_right_black.svg"></v-img>
                  </v-btn>
                  <v-btn icon @click="expand(false)" v-if="isExpanded">
                    <v-img contain height="6" src="@/assets/icons/chevron_down.svg"></v-img>
                  </v-btn>
                </template>

                <template v-slot:expanded-item="{ headers, item }">
                  <td :colspan="headers.length">
                    <v-list>
                      <v-list-item :key="event.event__title" v-for="event in item.events">{{event.event__title}}</v-list-item>
                    </v-list>
                  </td>
                </template>

                <template v-slot:item.url="{ item }">
                  <v-btn class="primary_btn" elevation="0" v-if="!item.url" x-small @click="request_url(item)">{{$t('Request url')}}</v-btn>
                  <template v-else>/{{item.url}}
                    <v-btn icon x-small elevation="0" @click="copyToClipboard"><v-icon>mdi-clipboard-multiple</v-icon></v-btn>
                    <v-text-field class="d-none" :value="item.full_url" ref="textToCopy"></v-text-field>
                  </template>
                </template>

                <template v-slot:item.actions="{ item }">
                  <v-btn icon @click="editMultishop(item)">
                    <v-img contain height="12" class="" src="@/assets/icons/pencil.svg" ></v-img>
                  </v-btn>
                    <v-divider vertical></v-divider>
                  <v-btn icon @click="deleteMultishop(item)">
                    <v-img contain height="12" src="@/assets/icons/trash.svg" ></v-img>
                  </v-btn>
                </template>
              </v-data-table>
          </panel>

      </v-col>
    </v-row>




    <v-dialog v-model="layout.delete_dialog" max-width="500px">
      <v-card>
        <v-card-title class="headline">{{$t('Are you sure you want to remove this?')}}</v-card-title>
        <v-card-actions>

          <v-btn class="secondary_btn blue" text @click="closeDelete">{{$t('Cancel')}}</v-btn>
          <v-spacer></v-spacer>
          <v-btn class="primary_btn" text @click="deleteConfirm">{{$t('Ok')}}</v-btn>

        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="layout.edit_dialog" width="802" scrollable :fullscreen="$vuetify.breakpoint.smAndDown" content-class="overflow-visible">
      <v-card min-height="400">
        <v-btn @click="layout.edit_dialog = false" v-show="$vuetify.breakpoint.mdAndUp" icon class="close_button"><v-img src="@/assets/icons/close.svg"></v-img></v-btn>
      <v-btn @click="layout.edit_dialog = false" icon v-show="$vuetify.breakpoint.smAndDown" class="close_button_mobile"><v-icon>mdi-close</v-icon></v-btn>
        <v-card-title style="padding-bottom:22px;padding-top:34px">{{formTitle}}</v-card-title>
        <v-card-text  style="height:100%;">
          <v-divider class="grey"></v-divider>
          <v-form  ref="create_form" lazy-validation>
            <v-container fluid>

              <h2 class="form_header">{{$t('Ticketshop name')}}</h2>
              <v-row>
                <v-col cols="4">
                  <v-text-field
                    outlined
                    flat
                    placeholder="ticketshop 1"
                    height="32"
                    required
                    v-model="layout.editedItem.name"
                  ></v-text-field>
                </v-col>

              </v-row>
              <v-divider class="grey" style="margin-top:12px;"></v-divider>
              <h2 class="form_header">{{$t('Add events to the multi-ticketshop')}}</h2>
              <v-row>
                <v-col cols="6">
                  <v-text-field
                    outlined
                    flat
                    :placeholder="$t('Search all events')"
                    height="32"
                    v-model="event_search"
                  ></v-text-field>
                </v-col>
                <v-col cols="6">{{$t('Added to the multi-ticketshop')}}</v-col>
              </v-row>
              <v-row >
                <v-col cols="6">
                  <v-card
                  v-for="(item, key) in layout.events" :key="key"
                    class="d-flex pa-2 item-small-custom"
                    outlined
                    tile
                    @click="add(item)"
                  >
                    <div class="mr-auto">{{ key + 1 }}. {{ item.title }}</div>
                    <div class="right">
                      <v-btn @click.stop="add(item)" x-small icon style="height:20px!important;">
                        <v-img contain height="12" src="@/assets/icons/plus_blue.svg"></v-img>
                      </v-btn>
                    </div>
                  </v-card>
                </v-col>
                <v-col cols="6">

                  <v-card
                  v-for="(item, key) in layout.selected_events" :key="item.name"
                    class="d-flex pa-2 item-small-custom"
                    outlined
                    tile
                  >
                    <div class="mr-auto">{{ key + 1 }}. {{ item.title }}</div>
                    <div class="right">
                      <v-btn @click="del(key)" x-small icon style="height:20px!important;">
                        <v-img contain height="12" src="@/assets/icons/trash_blue.svg"></v-img>
                      </v-btn>
                    </div>
                  </v-card>

                </v-col>

              </v-row>
            </v-container>
          </v-form>

        </v-card-text>
        <v-card-actions>

          <v-btn
              class="secondary_btn blue"
              text
              @click="layout.edit_dialog = false"
          >
              {{ $t('Cancel') }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
              class="primary_btn"
              text
              @click="save()"
          >
              {{$t('Save')}}
          </v-btn>

        </v-card-actions>
      </v-card>

    </v-dialog>

    <v-dialog
        v-model="layout.shorturl_dialog"
        max-width="600px"
    >
      <v-card>
        <v-card-title>Request short url</v-card-title>
        <v-card-text>
          <v-text-field v-model="layout.shorturl_name" prefix="https://yourtickets.nl/"></v-text-field>

        </v-card-text>
        <v-card-actions>

          <v-btn class="secondary_btn blue" text @click="layout.shorturl_dialog = false">{{$t('Cancel')}}</v-btn>
          <v-spacer></v-spacer>
          <v-btn elevation="0" color="primary_btn" @click="request_url_ok">{{$t('-request-popup-request-btn')}}</v-btn>
        </v-card-actions>
      </v-card>

    </v-dialog>


  </v-container>

</template>

<script>


export default {
  name: 'Multishop',
  mounted() {
    this.refreshTable();
  },
  computed: {
    formTitle () {
      return this.layout.editedIndex === -1 ? this.$t('Create a new multi-ticketshop') : this.$t('Edit multi-ticketshop')
    },
  },
  watch: {
      'event_search' () {
        this.filter_events()
      }
    },
  methods:{
    copyToClipboard(){
      this.$refs.textToCopy.$el.classList.remove('d-none')
      let textToCopy = this.$refs.textToCopy.$el.querySelector('input')
          textToCopy.select()
          document.execCommand("copy");
      this.$refs.textToCopy.$el.classList.add('d-none')
    },
    request_url(item){
      this.layout.shorturl_dialog = true;
      this.layout.shorturl_id = item.id
    },
    request_url_ok(){
      this.$store.dispatch('multiticketshops/request_url', {
        'multiticketshop_id': this.layout.shorturl_id,
        'url_name': this.layout.shorturl_name
      })
          .then(() => {
            this.layout.shorturl_dialog = false

          })
          .finally(() => this.loading = false)
    },
    filter_events(){
      this.$store.dispatch('event/getFilteredEvents', this.event_search)
          .then(response => {
          this.layout.events = response.data
        })
    },
    add(item){
      this.layout.selected_events.push(item)
    },
    del(key){
      this.layout.selected_events.splice(key,1)
    },
    refreshTable(){
      this.loading = true
      this.$store.dispatch('multiticketshops/getall')
        .then((response) => {
          this.multiticketshops = response.data.multishops

        })
        .finally(() => this.loading=false)
    },
    deleteMultishop(item){
      this.layout.editedIndex = this.multiticketshops.indexOf(item)
      this.layout.editedItem = Object.assign({}, item)
      this.layout.delete_dialog = true
    },
    closeDelete () {
      this.layout.delete_dialog = false
      this.$nextTick(() => {
        this.layout.editedItem = Object.assign({}, this.layout.defaultItem)
        this.layout.editedIndex = -1
      })
    },
    deleteConfirm(){

      this.$store.dispatch('multiticketshops/delete', {
        'multiticketshop_id': this.layout.editedItem.id
      })
      .then(() => {
        this.multiticketshops.splice(this.layout.editedIndex, 1)
        this.closeDelete()
      })
      .finally(() => this.loading = false)

    },
    createMultishop(){
      this.layout.editedIndex = -1;
      this.layout.edit_dialog = true
      this.layout.selected_events = []

      this.filter_events()

    },
    editMultishop(item){
      this.layout.edit_dialog = true;
      this.layout.editedIndex = this.multiticketshops.indexOf(item)
      this.layout.editedItem = Object.assign({}, item)

      this.$store.getters['multiticketshops/getEventsForShop'](item.id)
        .then((response) => {
          this.filter_events()
          this.layout.selected_events = response.data.events
        })
        .finally(() => this.loading = false)
    },
    save(){

      if (this.layout.editedIndex === -1) {


        this.$store.dispatch('multiticketshops/create', {
          //'multiticketshops_id': this.$route.params.id,
          'name': this.layout.editedItem.name,
          'events': this.layout.selected_events
        })
        .then(() => {

          this.refreshTable();
          this.layout.edit_dialog = false;
          this.layout.editedItem.name = '';
          this.$store.dispatch('messages/add', {text: this.$t('Multishop added')})
        })
        .finally(() => this.loading = false)

      }else{

        this.$store.dispatch('multiticketshops/update', {
          'multiticketshop_id': this.layout.editedItem.id,
          'name': this.layout.editedItem.name,
          'events': this.layout.selected_events
        })
        .then(() => {

          this.layout.editedIndex = -1;

          this.refreshTable();
          this.layout.edit_dialog = false
        })
        .finally(() => this.loading = false)
      }

    }
  },
  data: (scope)=>({
    expanded:[],
    event_search:'',
    layout:{
      delete_dialog:false,
      edit_dialog:false,
      shorturl_dialog: false,
      shorturl_name:'',
      shorturl_id:0,

      editedIndex: -1,
      events:[],
      selected_events:[],
      editedItem: {
        name: '',
      },
      defaultItem: {
        name: '',
      },
    },

    loading:false,
    headers:[
      { text: '', value: 'data-table-expand', sortable: false },
      { text: 'Multiticketshops', value: 'name' },
      { text: scope.$t('Total events'), value: 'total_events' },
      { text: 'Url', value: 'url' },
      { text: '', value: 'actions', sortable: false },
    ],
    mobile_headers:[
      { text: '', value: 'data-table-expand', sortable: false },
      { text: 'Multiticketshops', value: 'name' },
      { text: 'Url', value: 'url' },
      { text: '', value: 'actions', sortable: false },
    ],
    multiticketshops:[],
  })
}
</script>
