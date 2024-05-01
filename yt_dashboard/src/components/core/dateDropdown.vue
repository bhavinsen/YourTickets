<template>

<v-menu :close-on-content-click="false" offset-y bottom left v-model="menu_open" >

  <template v-slot:activator="{ on, attrs }">
    <v-btn class="primary_btn" :class="menu_open ? 'dark' : ''" v-bind="attrs" v-on="on" elevation="0">
      {{start_date}} - {{end_date}}
      <v-img class="ml-2" contain height="10" src="@/assets/icons/chevron_down_white.svg"></v-img>
    </v-btn>

  </template>
  <v-card dark style="background-color:#363A4F!important;" flat elevation="0" class="elevation-0" width="600">
    <v-card-text style="padding:0px!important;">
      <v-container fluid>
      <h2 style="margin-bottom:20px;">
        {{ $t('Period') }}
        </h2>

        <v-btn
            x-small
            @click="preset_dates('last_week')"
           :class="preset_date === 'last_week' ? 'primary_btn' : 'secondary_btn'"
           style="height:21px!important;font-size:10px!important;margin-right:8px;"
            :style="$vuetify.breakpoint.smAndDown ? 'margin-bottom:10px' : ''"
           rounded
        >
        {{ $t('Period') }}
        {{ $t('Last') }} week</v-btn>
        <v-btn x-small
           @click="preset_dates('last_30_days')"
           :class="preset_date === 'last_30_days' ? 'primary_btn' : 'secondary_btn'"
           style="height:21px!important;font-size:10px!important;margin-right:8px;"
               :style="$vuetify.breakpoint.smAndDown ? 'margin-bottom:10px' : ''"
               rounded>
               {{ $t('Last 30 days') }}
               </v-btn>
        <v-btn x-small
               @click="preset_dates('last_3_months')"
           :class="preset_date === 'last_3_months' ? 'primary_btn' : 'secondary_btn'"
               style="height:21px!important;font-size:10px!important;margin-right:8px;"
               :style="$vuetify.breakpoint.smAndDown ? 'margin-bottom:10px' : ''"
               rounded>
               {{ $t('Last 3 months') }}
               </v-btn>
        <v-btn x-small
               @click="preset_dates('last_year')"
           :class="preset_date === 'last_year' ? 'primary_btn' : 'secondary_btn'"
               style="height:21px!important;font-size:10px!important;margin-right:8px;"
               :style="$vuetify.breakpoint.smAndDown ? 'margin-bottom:10px' : ''"
               rounded>
               {{ $t('Last year') }}
               </v-btn>

      <v-divider style="margin-bottom:10px;margin-top:10px"></v-divider>

        <v-form class="dark">
          <v-row>
            <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : '6'">
              <span style="font-size:12px;margin-right:20px">{{ $t('By') }}</span>
              <v-text-field
                  outlined
                  flat
                  v-model="start_date"
                  class="d-inline-block"
                  style="width:50%;margin-bottom:4px;color:#ffffff!important;"
              >
              </v-text-field>
              <v-date-picker
                  show-adjacent-months
                  v-model="computeRange_start"
                  no-title
                  range
                  light
                  ref="start_date"

                  width="100%"></v-date-picker>
            </v-col>
            <v-col :cols="$vuetify.breakpoint.smAndDown ? 12 : '6'">
              <span style="font-size:12px;margin-right:20px">
                {{ $t('Till') }}
                </span>
              <v-text-field
                  outlined
                  flat
                  color="white"
                  class="d-inline-block"
                  v-model="end_date"
                style="width:50%;margin-bottom:4px;color:#ffffff!important;"
              >
              </v-text-field>
              <v-date-picker
                  show-adjacent-months
                  light
                  width="100%"
                  no-title
                  color="red"
                  range
                  ref="end_date"
                  v-model="computeRange_end"
              >
              </v-date-picker>
            </v-col>
          </v-row>
          <v-divider style="height:2px;margin-top:10px;"></v-divider>
          </v-form>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-btn class="secondary_btn" @click="menu_open = false;" style="margin-right:12px;">
        {{ $t('Cancel') }}
        </v-btn>
              <v-spacer ></v-spacer>
              <v-btn class="primary_btn" @click="manualDate(); menu_open = false;">
                {{ $t('Set date') }}
                </v-btn>
    </v-card-actions>
  </v-card>
</v-menu>

</template>
<script>
  import {mapActions} from "vuex";

  export default {
    name: 'dateDropdown',
    emits:['date_changed'],
    mounted () {
      this.preset_dates(this.default_preset_date)
    },
    watch: {
      'menu_open': function(val){
        if(val){
          this.end_change()
        }
      },
      'start_date': function(){
        this.end_change()
      },
      'end_date': function(){
        this.end_change()
      },
    },
    methods:{
      ...mapActions({
        setStartDate: "layout/setStartDate",
        setEndDate: "layout/setEndDate"
      }),
      manualDate(){
        this.setStartDate(this.start_date);
        this.setEndDate(this.end_date);

        this.$emit('date_changed', this.start_date, this.end_date)
      },
      preset_dates(type){
        var today = new Date()
        var today_display = today.toISOString().slice(0, 10);
        this.preset_date = type

        var d = new Date();
        if(type === 'last_week'){
          d.setDate(today.getDate() - 7);
        }
        else if(type === 'last_30_days'){
          d.setDate(today.getDate() - 30);
        }
        else if(type === 'last_3_months'){
          d.setDate(today.getDate() - (30*3));
        }
        else if(type === 'last_year'){
          d.setDate(today.getDate() - 365);
        }

        this.start_date = d.toISOString().slice(0, 10);
        this.end_date = today_display;

        this.setStartDate(this.start_date);
        this.setEndDate(this.end_date);
        
        this.menu_open = false;
        this.$emit('date_changed', this.start_date, this.end_date)


      },
      change_classes(firstEl, lastEl, item){
          if(!firstEl){
            return;
          }
          firstEl.classList.add('selected_date')
          lastEl.classList.add('other_date')

          if(this[item].first && this[item].first !== firstEl){
            this[item].first.classList.remove('selected_date')
          }
          this[item].first = firstEl

          if(this[item].last && this[item].last !== lastEl){
            this[item].last.classList.remove('other_date')
          }
          this[item].last = lastEl
      },
      end_change(){
        this.$nextTick(() => {
          if(!this.$refs['start_date']){
            return;
          }
          let start_date_el = this.$refs['start_date'].$el;
          let end_date_el = this.$refs['end_date'].$el;

          let start_first = start_date_el.querySelectorAll('.v-btn.v-btn--active')[0]
          let start_last = start_date_el.querySelectorAll('.v-btn.v-btn--active')[start_date_el.querySelectorAll('.v-btn.v-btn--active').length-1]
          this.change_classes(start_first, start_last, 'from')

          let end_first = end_date_el.querySelectorAll('.v-btn.v-btn--active')[end_date_el.querySelectorAll('.v-btn.v-btn--active').length-1]
          let end_last = end_date_el.querySelectorAll('.v-btn.v-btn--active')[0]

          this.change_classes(end_first, end_last, 'to')
        })
      },
    },
    computed: {

      computeRange_start: {
        get() {
          return [this.start_date, this.end_date]
        },
        set(val) {
          this.start_date = val[0];
          this.end_change()
        },
      },
      computeRange_end: {
        get() {
          return [this.start_date, this.end_date];
        },
        set(val) {
          this.end_date = val[0]
          this.end_change()
        },
      },
    },
    data:() => ({

      from:{
        first:'',
        last:'',
      },
      to:{
        first:'',
        last:'',
      },

      start_date:'2019-09-10',
      start_range: [],//['2019-09-10', '2019-09-20'],
      end_date:'2019-09-20',
      end_range:[],
      menu_open:false,
      preset_date:0,
      default_preset_date: 'last_week'


    })
  }
</script>
