<template>
  <v-dialog eager v-model="show_dialog" width="734" :fullscreen="$vuetify.breakpoint.smAndDown" content-class="overflow-visible">

    <template v-slot:activator="{ on, attrs }">
      <v-btn :block="$vuetify.breakpoint.smAndDown" v-bind="attrs" elevation="0" v-on="on"
             :class="$vuetify.breakpoint.smAndDown ? 'secondary_btn blue' : 'primary_btn'"
              style="margin-right:15px;">

      {{$t('Sales channels')}}</v-btn>
    </template>

    <v-card>
      <v-btn @click="show_dialog = false" v-show="$vuetify.breakpoint.mdAndUp" icon class="close_button"><v-img src="@/assets/icons/close.svg"></v-img></v-btn>
      <v-btn @click="show_dialog = false" icon v-show="$vuetify.breakpoint.smAndDown" class="close_button_mobile"><v-icon>mdi-close</v-icon></v-btn>
        <v-card-title style="padding-bottom:30px;padding-top:34px">
          {{$t('Sales channels')}}
        </v-card-title>
        <v-card-text style="height:400px;overflow:hidden;padding-left:24px!important;padding-right:24px!important;">
          <edit_table
                :headers="table.headers"
                :default-item="table.defaultItem"
                :items="table.items"
                v-on:create_item_saved="add"
                v-on:edit_item_saved="editsave"
                v-on:delete_item_confirmed="del"
                mobile-breakpoint="0"
            >
              <template v-slot:add_form="{addItemObject, add}">

                <tr>
                  <td colspan="2">

                      <v-text-field
                        single-line
                        dense
                        outlined
                        :placeholder="$t('Channel name')"
                        v-model.trim="addItemObject.name"
                        autofocus
                        ref="channel_name"
                        hide-details

                        :rules="form_rules.channel_name"
                        @input="resetValidation($refs.channel_name, 'channel_name')"
                        @blur="valid($refs.channel_name,'channel_name')"
                        :error-messages="form_errors.channel_name"
                      >
                        <errortooltip slot="append" :errors="form_errors.channel_name"></errortooltip>

                      </v-text-field>

                  </td>
                  
                  <td class="text-md-right">

                    <v-btn class="primary_btn d-inline-block"
                           :disabled.sync="addItemObject.name === '' || !addItemObject.name"
                           small elevation="0"
                           @click="add()"><v-icon>mdi-plus</v-icon></v-btn>
                  </td>
                </tr>

              </template>

              <template v-slot:item.name="{ item, editItem }">

                <v-text-field single-line dense v-if="editItem"
                                  outlined
                                  :placeholder="$t('Channel name')"
                                  v-model="editItem.name"></v-text-field>
                    <span v-else> {{ item.name }}</span>
              </template>
              <template v-slot:item.revenue="{ item }">


                    <span>&euro; {{ item.revenue }}</span>
              </template>
            <template v-slot:action_buttons="{item}">

              <v-btn class="d-inline-block primary_btn" x-small elevation="0"
                   @click="copyToClipBoard(item.url_name)">
                   {{ $t('copy url') }}
                
              </v-btn>
              <v-divider vertical style="margin-bottom:-4px!important;margin-left:10px"></v-divider>



            </template>


            </edit_table>
        </v-card-text>
    </v-card>

  </v-dialog>
</template>

<script>

import edit_table from "@/components/event/edit/edit_table";
import { required, alphaNumeric} from "@/plugins/validate";
import errortooltip from "@/components/core/errortooltip";


export default {
  name: 'event_sales_channels',
  components:{
    edit_table,
    errortooltip
  },
  mounted () {


  },
  methods: {
    add(addItemObject){
      this.resetValidation(this.$refs.channel_name, 'channel_name')
      this.$store.dispatch('event_saleschannels/create', {
          'event_id': this.$route.params.id,
          'name': addItemObject.name
        })
        .then((response) => {
          // this.saleschannels.push(response.data.saleschannel)
          addItemObject.id = response.data.saleschannel.id

        })
    },
    copyToClipBoard(url){
      navigator.clipboard.writeText(url);
    },
    editsave(item){

      this.$store.dispatch('event_saleschannels/update', {
        'event_id': this.$route.params.id,
        'saleschannel_id': item.id,
        'name': item.name
      })
      .then(() => {
        //show a nice message?
      })

    },
    del(item){
      this.$store.dispatch('event_saleschannels/delete', {
        'event_id': this.$route.params.id,
        'saleschannel_id': item.id
      })
      .then(() => {
        //show a message?
      })
    },
    valid(el, key){

      if(!el.valid && el.errorMessages.length === 0){
        this.form_errors[key].push(el.errorBucket[0]);
      }else if(el.valid){
        this.form_errors[key] = []
      }
    },
    resetValidation(el, key){
      el.resetValidation()
      this.form_errors[key] = []
    },
    load(){
      this.$store.getters['event_saleschannels/getall'](this.$route.params.id)
        .then((response) => {
          this.table.items = response.data.channels

        })
    }
  },
  computed:{

  },
  watch:{
    'show_dialog'(val) {
      if(val === true){
        this.load()
        this.resetValidation(this.$refs.channel_name, 'channel_name')
        this.$refs.channel_name.reset()
      }
    }
  },
  data: () => ({
      show_dialog:false,
      form_rules: {
        channel_name: [
          required(),
          alphaNumeric()
        ],
      },
      form_errors: {
        channel_name: [],
      },
      table:{
        defaultItem:{
          id: 0,
          name: '',
          revenue: 0,
        },
        items:[],
        headers:[
          { text: 'Channel name', value: 'name' },
          { text: 'Revenue', value: 'revenue' },
          {text: '', value: 'actions', sortable: false },
        ]
      },

  })
}
</script>