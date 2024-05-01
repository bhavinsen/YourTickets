<template>

  <div :class="active ? 'active' : ''" class="stepper_item">
      <h2 class="stepper_item_header">
        {{ $t('-createevent.when.header') }}
       </h2>

      <v-container fluid>
        <v-row>
          <v-col cols="4" style="padding-left:0px!important;">
            <v-form>
              <div class="form_field_label">
                {{ $t('-createevent.when.Date') }}
                </div>
                    <v-text-field
                        :rules="form_rules.start_date"
                        ref="start_date"
                        v-model="computedStartDate"
                        autocomplete="false"
                        name="start_date"
                        placeholder="DD-MM-YYYY"
                        outlined
                        flat
                        autofocus
                        :error-messages="form_errors.start_date"
                        hide-details
                        @input="resetValidation($refs.start_date, 'start_date')"
                        @blur="valid($refs.start_date,'start_date')"
                    >
                      <errortooltip slot="append" :errors="form_errors.start_date"></errortooltip>

                    </v-text-field>

            <div class="d-flex justify-start" style="padding-top:20px;">
             <div style="margin-right:8px;">
              <div class="form_field_label">{{ $t('Start time') }}</div>
              <v-text-field type="time" style="width:60px;" outlined flat placeholder="uu:mm" v-model="form_data.start_time"></v-text-field>
              </div>
              <div>
                <div class="form_field_label">{{ $t('End time') }}</div>
              <v-text-field type="time" style="width:60px;" outlined flat placeholder="uu:mm" v-model="form_data.end_time"></v-text-field>
              </div>
              </div>

            </v-form>
          </v-col>
          <v-col cols="7" style="padding-top:0px;padding-left:52px;">
            <v-date-picker
                show-adjacent-months
                class="create_event"

                v-model="form_data.start_date"
                no-title
                @input="start_date_menu = false">
            </v-date-picker>
          </v-col>
        </v-row>


      </v-container>
    </div>

</template>
<script>
  import resetForm from "@/mixins/resetForm";
  import {isDate, required} from "@/plugins/validate";
  import errortooltip from "@/components/core/errortooltip";
  import watchData from "@/mixins/watchData";

  export default {
    name: 'createEventStep2',
    components:{
      errortooltip
    },
    emits:['change'],
    props:['active', 'data', 'unload'],
    mixins:[resetForm, watchData],
    mounted () {

    },
    computed: {
      computedStartDate: {
        get () {
          return this.formatDate(this.form_data.start_date);
        },
        set (v) {

          if(v === ''){
            return
          }
          let d = new Date(this.reverseDate(v))
          if(d instanceof Date && !isNaN(d)){
            this.event.start_date = this.reverseDate(v)
            this.event.end_date = this.reverseDate(v)
          }
        },
      },


      computedEndDate () {
        return this.formatDate(this.event.end_date);
      },

    },
    methods:{
      formatDate (date) {
        if (!date) return null

        const [year, month, day] = date.split('-')
        return `${day}-${month}-${year}`
      },
      reverseDate(date){
        const [day, month, year] = date.split('-')
        return `${year}-${month}-${day}`
      },
    },
    data:(scope) => ({
      start_date_menu:false,
      form_data:{
        start_date:'',
        end_date:'',
        start_time:'',
        end_time:'',
      },

      form_errors: {
        start_date: [],

        start_time:[],
        end_time:[],

      },
      form_rules: {
        start_date: [
            required(),
            isDate(true, scope.$t('-createevent.when.Fill in a correct date'))
        ],
      }

    })
  }
</script>
