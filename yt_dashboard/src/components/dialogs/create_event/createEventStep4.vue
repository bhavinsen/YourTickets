<template>

  <div :class="active ? 'active' : ''" class="stepper_item">
    <h2 class="stepper_item_header">{{$t('-createevent.tickets.header')}}</h2>
      <v-form ref="ticketform">
        <v-data-table
            hide-default-footer
            :headers="tickettable.headers"
            :items="form_data.tickets"
            fixed-header height="200"
            class="custom_dense"
            disable-sort

        >
          <template v-slot:body.prepend="">
            <tr>
              <td>


                <v-text-field
                    ref="ticket_type"
                    single-line dense
                    outlined
                    :placeholder="$t('-createevent.tickets.add-placeholder')"
                    hide-details
                    :rules="form_rules.ticket_type"
                    @input="resetValidation($refs.ticket_type, 'ticket_type')"
                    @blur="valid($refs.ticket_type,'ticket_type')"
                    :error-messages="form_errors.ticket_type"
                    v-model="tickettable.addTicketObject.name">
                </v-text-field>
              </td>
              <td>
                <v-text-field
                  ref="ticket_amount"
                  outlined
                  type="number"
                  placeholder="0"
                  step="1"
                  min="1"
                  hide-details
                  v-model="tickettable.addTicketObject.amount"
                  :rules="form_rules.ticket_amount"
                  @input="resetValidation($refs.ticket_amount, 'ticket_amount')"
                  @blur="valid($refs.ticket_amount,'ticket_amount')"
                  :error-messages="form_errors.ticket_amount"
                >


                </v-text-field>
              </td>
              <td>
                <v-text-field
                  outlined
                  placeholder=""
                  type="number"
                  step=".01"
                  v-model="tickettable.addTicketObject.price"
                  ref="ticket_price"
                  hide-details
                  prefix="€"
                  min="0"
                  :rules="form_rules.ticket_price"
                  @input="resetValidation($refs.ticket_price, 'ticket_price')"
                  @blur="valid($refs.ticket_price,'ticket_price')"
                  :error-messages="form_errors.ticket_price"
                >

                </v-text-field>
              </td>
              <td>
                <v-text-field
                  outlined
                  :placeholder="$t('-createevent.tickets.amount-per-order-placeholder')"
                  type="number"
                  v-model="tickettable.addTicketObject.amount_per_order"
                  hide-details
                  ref="ticket_amount_per_order"
                  :rules="form_rules.ticket_amount_per_order"
                  @input="resetValidation($refs.ticket_amount_per_order, 'ticket_amount_per_order')"
                  @blur="valid($refs.ticket_amount_per_order,'ticket_amount_per_order')"
                  :error-messages="form_errors.ticket_amount_per_order"
                >


                </v-text-field>
              </td>
              <td>
                <v-text-field
                  outlined
                  placeholder="1"
                  type="number"
                  min="1"
                  v-model="tickettable.addTicketObject.persons_per_ticket"
                  ref="ticket_persons_per_ticket"
                  hide-details
                  :rules="form_rules.ticket_persons_per_ticket"
                  @input="resetValidation($refs.ticket_persons_per_ticket, 'ticket_persons_per_ticket')"
                  @blur="valid($refs.ticket_persons_per_ticket,'ticket_persons_per_ticket')"
                  :error-messages="form_errors.ticket_persons_per_ticket"
                >


                </v-text-field>
              </td>
              <td >


                <v-menu :close-on-content-click="false" offset-y bottom left eager
                        v-model="tickettable.dateMenuAdd" >

                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                          v-bind="attrs" v-on="on"
                          block
                          :class="{ secondary_btn_error: ticket_date_has_error }"
                          class="secondary_btn blue d-inline-block"
                          small :elevation="tickettable.dateMenuAdd ? 4 : 0"
                          ><v-img src="@/assets/icons/calendar.svg" contain height="16" width="16"></v-img>
                          <div v-if="tickettable.dateMenuAdd" style="background-color:white;height:3px;position:absolute;right:-13px;width:69px;bottom:-8px;"></div>
                      </v-btn>
                    </template>


                    <v-card width="400" outlined style="border-color:#66C5E1!important;">
                      <div v-if="tickettable.dateMenuAdd" style="background-color:white;height:3px;position:absolute;right:0px;width:69px;top:-2px;"></div>

                      <v-card-text>
                        <h2 style="margin-bottom:5px;">
                          {{ $t('-createevent.tickets.sell-dates') }}
                          </h2>
                          <v-form ref="ticketdates">
                          <v-container fluid >
                          <v-row>
                            <v-col cols="6">
                              <v-menu
                                  v-model="tickettable.start_date_menu"
                                  :close-on-content-click="true"
                                  transition="scale-transition"
                                  offset-y
                                  max-width="290px"
                                  min-width="290px"

                              >
                                <template v-slot:activator="{ on, attrs }">
                                  Start verkoop
                                  <v-text-field
                                      v-model="cp_add_start_date"
                                      autocomplete="false"

                                      placeholder="dd - mm - jjjj"
                                      readonly
                                      outlined
                                      flat
                                      hide-details
                                      v-bind="attrs"
                                      v-on="on"
                                      ref="ticket_start_date"
                                      :rules="form_rules.ticket_start_date"
                                      @input="resetValidation($refs.ticket_start_date, 'ticket_start_date')"

                                    :error-messages="form_errors.ticket_start_date"
                                  ></v-text-field>
                                </template>
                                <v-date-picker
                                    v-model="tickettable.addTicketObject.start_date"
                                    no-title
                                    @input="tickettable.start_date_menu = false"></v-date-picker>
                              </v-menu>

                            </v-col>
                            <v-col cols="6">
                              {{ $t('-createevent.tickets.Time') }}
                              
                                  <v-text-field
                                      v-model="tickettable.addTicketObject.start_time"
                                      autocomplete="false"
                                      name="start_time"
                                      type="time"
                                      placeholder="uu : mm"
                                      outlined
                                      flat
                                      hide-details

                                      ref="ticket_start_time"
                                      :rules="form_rules.ticket_start_time"
                                      @input="resetValidation($refs.ticket_start_time, 'ticket_start_time')"

                                    :error-messages="form_errors.ticket_start_time"
                                  ></v-text-field>
                            </v-col>
                          </v-row>
                          <v-row>
                            <v-col cols="6">
                              <v-menu
                                  v-model="tickettable.end_date_menu"
                                  :close-on-content-click="true"
                                  transition="scale-transition"
                                  offset-y
                                  max-width="290px"
                                  min-width="290px"

                                  :rules="form_rules.ticket_end_date"

                              >
                                <template v-slot:activator="{ on, attrs }">
                                  {{ $t('-createevent.tickets.End sale') }}
                                  
                                  <v-text-field
                                      v-model="cp_add_end_date"
                                      autocomplete="false"
                                      name="end_date"
                                      placeholder="dd - mm - jjjj"
                                      readonly
                                      hide-details
                                      outlined
                                      flat
                                      v-bind="attrs"
                                      v-on="on"
                                      ref="ticket_end_date"
                                      :rules="form_rules.ticket_end_date"
                                      @input="resetValidation($refs.ticket_end_date, 'ticket_end_date')"

                                    :error-messages="form_errors.ticket_end_date"
                                  ></v-text-field>
                                </template>
                                <v-date-picker v-model="tickettable.addTicketObject.end_date" no-title @input="tickettable.end_date_menu = false"></v-date-picker>
                              </v-menu>

                            </v-col>
                            <v-col cols="6">
                              {{ $t('-createevent.tickets.Time') }}
                              
                                  <v-text-field
                                      v-model="tickettable.addTicketObject.end_time"
                                      autocomplete="false"
                                      name="end_time"
                                      type="time"
                                      placeholder="uu : mm"
                                      outlined
                                      flat
                                      hide-details
                                      ref="ticket_end_time"
                                      :rules="form_rules.ticket_end_time"
                                      @input="resetValidation($refs.ticket_end_time, 'ticket_end_time')"

                                    :error-messages="form_errors.ticket_end_time"
                                  ></v-text-field>

                            </v-col>
                          </v-row>
                        </v-container>
                        </v-form>
                      </v-card-text>

                    </v-card>

                </v-menu>


              </td>
              <td class="text-md-right">
                <v-btn block class="primary_btn" small elevation="0" @click="addTicket()"><v-icon>mdi-plus</v-icon></v-btn>
              </td>
            </tr>
          </template>
          <template v-slot:item.name="{ item }">
            <v-text-field single-line dense
                          outlined
                          :placeholder="$t('-createevent.tickets.add-placeholder')"
                          hide-details

                          :rules="form_rules.ticket_type"
                          v-model="item.name"></v-text-field>

          </template>
          <template v-slot:item.amount="{ item }">
            <v-text-field
                          outlined
                          type="number"
                          placeholder="0"
                          v-model="item.amount"></v-text-field>

          </template>

          <template v-slot:item.price="{ item }">
            <v-text-field
              outlined
              type="number"
              step=".01"
              hide-details
              prefix="€"
              min="0"
              placeholder="€"
              v-model="item.price"></v-text-field>

          </template>
          <template v-slot:item.amount_per_order="{ item }">
            <v-text-field
                          outlined
                          :placeholder="$t('-createevent.tickets.amount-per-order-placeholder')"
                          type="number"
                          v-model="item.amount_per_order"></v-text-field>
          </template>
          <template v-slot:item.persons_per_ticket="{ item }">
            <v-text-field
                          outlined
                          placeholder="1"
                          type="number"
                          step="1"
                          min="1"
                          v-model="item.persons_per_ticket"></v-text-field>

          </template>

          <template v-slot:item.start_date="{ item }">


            <v-menu :close-on-content-click="false" offset-y bottom left >

                    <template v-slot:activator="{ on, attrs }">
                      <v-btn

                          v-bind="attrs" v-on="on"
                          style="margin-right:10px;"
                          block
                          class="secondary_btn blue d-inline-block"
                          small :elevation="tickettable.dateMenuEdit ? 6 : 0"
                          ><v-img src="@/assets/icons/calendar.svg" contain height="16" width="16"></v-img>
                          <div v-if="tickettable.dateMenuEdit" style="background-color:white;height:3px;position:absolute;right:-13px;width:69px;bottom:-8px;"></div>
                      </v-btn>
                    </template>


                    <v-card width="400" outlined style="border-color:#66C5E1!important;">
                      <div v-if="tickettable.dateMenuEdit"
                           style="background-color:white;height:3px;position:absolute;right:0px;width:69px;top:-2px;"></div>
                      <v-form>
                      <v-card-text>
                        <h2 style="margin-bottom:5px;">
                          {{ $t('-createevent.tickets.sell-dates') }}
                          </h2>

                        <v-container fluid >
                          <v-row>
                            <v-col cols="6">
                              <v-menu

                                  :close-on-content-click="true"
                                  transition="scale-transition"
                                  offset-y
                                  max-width="290px"
                                  min-width="290px"

                              >
                                <template v-slot:activator="{ on, attrs }">
                                  {{ $t('-createevent.tickets.Start sale') }}
                                  
                                  <v-text-field

                                      :value="formatDate(item.start_date)"

                                      autocomplete="false"

                                      placeholder="dd / mm / jjjj"
                                      readonly
                                      outlined
                                      flat
                                      v-bind="attrs"
                                      v-on="on"
                                  ></v-text-field>
                                </template>
                                <v-date-picker
                                    v-model="item.start_date"
                                    no-title
                                    @input="tickettable.start_date_menu = false">

                                </v-date-picker>
                              </v-menu>

                            </v-col>
                            <v-col cols="6">
                              Tijd
                                  <v-text-field
                                      v-model="item.start_time"
                                      autocomplete="false"
                                      type="time"
                                      name="start_time"
                                      placeholder="uu : mm"
                                      outlined
                                      flat
                                  ></v-text-field>
                            </v-col>
                          </v-row>
                          <v-row>
                            <v-col cols="6">
                              <v-menu

                                  :close-on-content-click="true"
                                  transition="scale-transition"
                                  offset-y
                                  max-width="290px"
                                  min-width="290px"

                              >
                                <template v-slot:activator="{ on, attrs }">
                                  Einde verkoop
                                  <v-text-field
                                      :value="formatDate(item.end_date)"
                                      autocomplete="false"
                                      name="end_date"
                                      placeholder="dd / mm / jjjj"
                                      readonly
                                      outlined
                                      flat
                                      v-bind="attrs"
                                      v-on="on"
                                  ></v-text-field>
                                </template>
                                <v-date-picker v-model="item.end_date" no-title @input="tickettable.end_date_menu = false"></v-date-picker>
                              </v-menu>

                            </v-col>
                            <v-col cols="6">
                              Tijd
                                  <v-text-field
                                      v-model="item.end_time"
                                      autocomplete="false"
                                      type="time"
                                      name="end_time"
                                      placeholder="uu : mm"
                                      outlined
                                      flat
                                  ></v-text-field>

                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>
                        </v-form>
                    </v-card>
                </v-menu>


          </template>


          <template v-slot:item.actions="{ item }">
            <div class="text-md-right">


                <v-btn small class="d-inline-block" text icon elevation="0" @click="deleteTicket(item)"><v-img src="@/assets/icons/delete.svg" contain height="20" width="12"></v-img></v-btn>

            </div>
          </template>

        </v-data-table>
      </v-form>
  </div>

</template>
<script>
  import resetForm from "@/mixins/resetForm";
  import {isFloat, isNumericAndPositive, required} from "@/plugins/validate";

  import watchData from "@/mixins/watchData";

  export default {
    name: 'createEventStep4',
    components:{
    },
    emits:['change'],
    props:['active', 'data', 'unload'],
    mixins:[resetForm, watchData],
    mounted () {

    },
    computed: {
      cp_add_start_date(){
        return this.formatDate(this.tickettable.addTicketObject.start_date);
      },
      cp_add_end_date(){
        return this.formatDate(this.tickettable.addTicketObject.end_date);
      },

    },
    watch:{
      'active'(v){
        if(v === true){
          this.setDefaultDates()
          this.$refs.ticketform.resetValidation()
          this.form_errors = Object.assign({}, this.start_form_errors)
        }
        if(v === false){
          this.addTicket()
        }
      }
    },
    methods:{
      setDefaultDates(){
        const now = new Date()
        this.tickettable.addTicketObject.start_date = this.nowToString()
        const minutes = now.getMinutes()<10?'0':'' + now.getMinutes()
        this.tickettable.addTicketObject.start_time = now.getHours()+':'+minutes

        let end_date = Date.parse(this.$props.data.start_date + ' '+ this.$props.data.start_time)
        const addHours = 3

        const end_datee = new Date((end_date + (addHours * 60 * 60 * 1000)))
        this.tickettable.addTicketObject.end_date = end_datee.toISOString().slice(0,10)
        const end_minutes = end_datee.getMinutes()<10?'0':'' + end_datee.getMinutes()
        this.tickettable.addTicketObject.end_time = end_datee.getHours()+':'+end_minutes
      },
      nowToString(){
        let rightNow = new Date();
        return rightNow.toISOString().slice(0,10)
      },
      formatDate (date) {
        if (!date) return null

        const [year, month, day] = date.split('-')
        return `${day}-${month}-${year}`
      },
      addTicket(){

        // save
        // console.log(this.$refs.ticketdates.inputs)
        if(this.$refs.ticketform.validate() && this.$refs.ticketdates.validate()){
          this.tickettable.addTicketObject.pk = -1
          this.form_data.tickets.push(this.tickettable.addTicketObject)
          //RESET
          this.tickettable.addTicketObject = Object.assign({}, this.defaultTicket)

          this.$refs.ticketform.resetValidation()
          this.setDefaultDates()
        }
        // else{
        //   this.$refs.ticketform.validate()
        // }
        if(!this.$refs.ticketdates.validate()){
          this.ticket_date_has_error = true
        }else{
          this.ticket_date_has_error = false
        }

      },
      cancelEdit(index){
        this.tickettable.editTicketObjects.splice(index, 1)
      },

      deleteTicket(ticket){
        let index = this.form_data.tickets.indexOf(ticket)
        this.form_data.tickets.splice(index, 1)

        //@TODO
        //this.items.editItemObjects.splice(itemIndex, 1)

        // dit nog nodig?
        this.tickettable.editIndex = -1
        this.tickettable.editTicketObject = {}

      },
    },
    data:(scope) => ({
      ticket_date_has_error:false,
      form_data:{
        tickets:[],
      },
      start_form_errors: {
        ticket_type:[],
        ticket_amount:[],
        ticket_price:[],
        ticket_amount_per_order:[],
        ticket_persons_per_ticket:[],
        ticket_start_date: [],
        ticket_end_date: [],
        ticket_start_time:[],
        ticket_end_time:[],
      },
      form_errors: {
        ticket_type:[],
        ticket_amount:[],
        ticket_price:[],
        ticket_amount_per_order:[],
        ticket_persons_per_ticket:[],
        ticket_start_date: [],
        ticket_end_date: [],
        ticket_start_time:[],
        ticket_end_time:[],
      },
      form_rules: {
        ticket_type:[
            required()
        ],
        ticket_amount:[
            required(),
            isNumericAndPositive()
        ],
        ticket_price:[
            required(),
            isFloat()
        ],
        ticket_amount_per_order:[
            // required()

        ],
        ticket_persons_per_ticket:[
            required(),
            isNumericAndPositive()
        ],
        ticket_start_date:[
            // required(),
            // isDate(true)
        ],
        ticket_end_date:[
            // required(),
            // isDate(true)
        ],
        ticket_start_time:[
            // required(),
        ],
        ticket_end_time:[
            // required()
        ],
      },
      tickettable:{
        editTicketObjects:[],
        addTicketObject:{
          pk:-1,
          name:'',
          amount: '',
          price: '',
          amount_per_order: '10',
          persons_per_ticket:'1',
          start_date:'',
          end_date:'',
          start_time:'',
          end_time:'',
          actions:false
        },
        dateMenuAdd:false,
        dateMenuEdit:false,
        start_date_menu:false,
        end_date_menu:false,
        headers: [
            { text: scope.$t('-createevent.tickets.Ticket type'), value: 'name', align:'left', width:198 },
            { text: scope.$t('-createevent.tickets.Amount'), value: 'amount', align:'left' },
            { text: scope.$t('-createevent.tickets.Price'), value: 'price', align:'left' },
            { text: scope.$t('-createevent.tickets.Max per order'), value: 'amount_per_order', align:'left' },
            { text: scope.$t('-createevent.tickets.Persons per ticket'), value: 'persons_per_ticket', align:'left', width:60 },
            { text: scope.$t('-createevent.tickets.Dates'), value: 'start_date', align:'left', width:75 },
            { text: '', value: 'actions', width:'70px', align:'right' },
        ]
      },
      defaultTicket:{
        pk:-1,
        name:'',
        amount: '',
        price: '',
        amount_per_order: '',
        persons_per_ticket:'1',
        start_date:'',
        end_date:'',
        start_time:'',
        end_time:'',
        actions:false
      },
    })
  }
</script>
