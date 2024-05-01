<template>
  <v-dialog v-model="create_dialog" persistent @click:outside="closeDialog" :fullscreen="$vuetify.breakpoint.smAndDown" :width="730" eager content-class="overflow-visible">

    <v-dialog v-model="changes_dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline text-center justify-center">
            {{ $t('-unsaved_changes.message') }}
            
          </v-card-title>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="secondary_btn blue" text @click="changes_dialog = false">{{ $t('Cancel') }}</v-btn>
            <v-btn class="primary_btn" text @click="changes_dialog = false;create_dialog=false">{{ $t('Close') }}</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>

    <template v-slot:activator="{ on, attrs }">
      <v-btn
          :block="$vuetify.breakpoint.smAndDown"
        v-if="$props.editmode"
        class="secondary_btn blue"
        v-bind="attrs"
        v-on="on"
        @click="load_data"
        elevation="0">
          <v-img style="margin-right:6px;width:12px;flex:0 auto;" width="12" src="@/assets/icons/pencil_blue.svg"/>
          {{ $t('Edit event') }}
          
      </v-btn>
      <v-btn v-else v-bind="attrs" :block="responsiveAndNavClosed" elevation="0" :min-width="$vuetify.breakpoint.smAndDown ? '100%' : ''" @click="initiate_event" v-on="on" class="primary_btn" style="margin-right:15px;">
        <img style="margin-right:6px;" src="@/assets/icons/plus.svg">
        <template v-if="!responsiveAndNavClosed && !$vuetify.breakpoint.mdAndDown">
          {{ $t('Create new event') }}
          </template>
        <template v-else-if="$vuetify.breakpoint.mdAndDown">
          {{ $t('New event') }}
          </template>
      </v-btn>
    </template>

    <v-card class="d-flex flex-column">
      <v-btn @click="closeDialog" v-show="$vuetify.breakpoint.mdAndUp" icon class="close_button"><v-img src="@/assets/icons/close.svg"></v-img></v-btn>
      <v-btn @click="closeDialog" icon v-show="$vuetify.breakpoint.smAndDown" class="close_button_mobile"><v-icon>mdi-close</v-icon></v-btn>
      <v-card-title style="padding-top:34px;font-size:16px;">
        {{ $t('Time for a new event!') }}
        </v-card-title>
        <v-card-text style="height:400px;padding-top:30px;padding-left:24px!important;">

          <div class="stepper">
            <div :class="stepper_class(1)" class="step d-inline-block" style="margin-left:0;">
              <div @click="stepper_step = 1" style="cursor: pointer;" class="text">{{ $t('Name') }}</div>
              <div class="line"></div>
            </div>
            <div :class="stepper_class(2)" class="step d-inline-block">
              <div @click="stepper_step = 2" style="cursor: pointer;" class="text">{{ $t('When') }}</div>
              <div class="line"></div>
            </div>
            <div :class="stepper_class(3)" class="step d-inline-block">
              <div @click="stepper_step = 3" style="cursor: pointer;" class="text">{{ $t('Where') }}</div>
              <div class="line"></div>
            </div>
            <div :class="stepper_class(4)" class="step d-inline-block">
              <div @click="stepper_step = 4" style="cursor: pointer;" class="text">{{ $t('Tickets') }}</div>
              <div class="line"></div>
            </div>
            <div :class="stepper_class(5)" class="step d-inline-block">
              <div @click="stepper_step = 5" style="cursor: pointer;" class="text">{{ $t('Line-up') }}</div>
              <div class="line"></div>
            </div>
            <div :class="stepper_class(6)" class="step d-inline-block">
              <div @click="stepper_step = 6" style="cursor: pointer;" class="text">{{ $t('Design') }}</div>
              <div class="line"></div>
            </div>

            <v-divider style="margin-top:10px;border-color:#E5E5E5!important;margin-bottom:25px;"></v-divider>

            <v-container fluid>
            <div style="color:#66C5E1">{{ $t('Step') }} {{stepper_step}}/6</div>
              <div class="stepper-content">

                <create-event-step1
                    :unload="create_dialog === false"
                    :active="stepper_step === 1"
                    :data="event"
                    @change="formChanged"
                ></create-event-step1>

                <create-event-step2
                  :unload="create_dialog === false"
                  :active="stepper_step === 2"
                  :data="event"
                  @change="formChanged"
                ></create-event-step2>

                <create-event-step3
                  :unload="create_dialog === false"
                  :active="stepper_step === 3"
                  :data="event"
                  @change="formChanged"
                ></create-event-step3>

                <create-event-step4
                  :unload="create_dialog === false"
                  :active="stepper_step === 4"
                  :data="event"
                  @change="formChanged"
                ></create-event-step4>

                <create-event-step5
                  :unload="create_dialog === false"
                  :active="stepper_step === 5"
                  :data="event"
                  @change="formChanged"
                ></create-event-step5>

                <create-event-step6
                  :unload="create_dialog === false"
                  :active="stepper_step === 6"
                  :data="event"
                  @change="formChanged"
                ></create-event-step6>

              </div>
            </v-container>
          </div>





        </v-card-text>
      <v-spacer></v-spacer>
      <v-divider class="d-block" style="margin-left:15px;margin-right:15px;"></v-divider>
      <v-card-actions >
        <v-btn
            :class="stepper_step===1 ? 'd-none' : ''"
            @click="stepper_step -= 1"
            elevation="0"
            class="secondary_btn blue">&lt; {{ $t('Previous') }}</v-btn>
        <v-btn
            style="margin-left:0;"
            :class="stepper_step!==1 ? 'd-none': ''"
            @click="closeDialog"
            elevation="0"
            class="secondary_btn blue">{{ $t('Cancel') }}</v-btn>

        <v-spacer></v-spacer>

        <v-btn v-if="this.stepper_step < 6" elevation="0" class="primary_btn" @click="next_step">{{ $t('Next') }} ></v-btn>
        <v-btn v-if="this.stepper_step === 6" elevation="0" class="primary_btn" :disabled="saving_disabled" @click="save_event">{{ $t('Save') }}</v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>
</template>

<script>

import createEventStep1 from "@/components/dialogs/create_event/createEventStep1";
import createEventStep2 from "@/components/dialogs/create_event/createEventStep2";
import createEventStep3 from "@/components/dialogs/create_event/createEventStep3";
import createEventStep4 from "@/components/dialogs/create_event/createEventStep4";
import createEventStep5 from "@/components/dialogs/create_event/createEventStep5";
import createEventStep6 from "@/components/dialogs/create_event/createEventStep6";


export default {
  name: 'create_event',
  props:['editmode', 'responsive', 'manuallyShow', 'activeTab'],
  emits:['close'],
  components:{
    createEventStep1,
    createEventStep2,
    createEventStep3,
    createEventStep4,
    createEventStep5,
    createEventStep6
  },
  mounted () {
  },
  watch:{

    'create_dialog'(val){

      if(val === true){
        this.formIsChanged = false
        if(!this.$props.manuallyShow) {
          this.stepper_step = 1
        }
      }
      if(val === false){
        this.$emit('close')
        // this.eventWatch()
      }
    },
    'manuallyShow'(tab){
      if(tab !== false){
        this.create_dialog = true
        this.stepper_step = tab
        this.load_data()
      }
    }
  },
  methods: {
    test(){
      console.log(this.$refs.tab1)
    },
    closeDialog(){
      if(this.formIsChanged === true){
        this.changes_dialog = true
      }else{
        this.create_dialog = false
      }
    },
    initiate_event(){
      let d = new Date();
      this.event = Object.assign({},this.default_event);
      this.saving_disabled = false;
      this.event.start_time = d.getHours() + ":" + d.getMinutes();
      let day = (d.getMonth()+1).toString().padStart(2, '0')
      this.event.start_date = d.getFullYear()+ "-" + day + "-" +  d.getDate();
      d.setHours(d.getHours() + 2);
      this.event.end_date = d.getFullYear()+ "-" + day + "-" +  d.getDate();
      this.event.end_time = d.getHours() + ":" + d.getMinutes();


    },
    formChanged(data){

      for (const [key, value] of Object.entries(data)) {
        this.event[key] = value
      }

      this.formIsChanged = true;
    },
    load_data(){
      this.$store.getters['event/getEventApi'](this.$route.params.id)
      .then((response) => {
        let data = response.data.event;
        if(data.primary_color === null){
          data.primary_color = this.default_event.primary_color
        }
        if(data.secondary_color === null){
          data.secondary_color = this.default_event.secondary_color
        }
        data.tickets = response.data.tickets
        data.lineups = response.data.lineups
        this.event = data;

      })
    },
    stepper_class:function(step){
      let classList = ''
      if(step === this.stepper_step){
        classList = 'active'
      }
      if(step < this.stepper_step){
        classList = 'done'
      }
      return classList
    },
    next_step: function(){
      if(this.stepper_step === 6){
        return;
      }
      this.stepper_step += 1;
    },

    save_event(){
      let formData = new FormData();

      //temp disabled
      // this.saving_disabled = true;

      formData.append("header_img", this.event.header_img);
      formData.append("bg_img", this.event.bg_img);
      formData.append("primary_color", this.event.primary_color);
      formData.append("secondary_color", this.event.secondary_color);
      formData.append("name", this.event.name)
      formData.append("online", this.event.online)
      formData.append("event_location", this.event.location)
      let time_s = this.event.start_time === '' ? '00:00': this.event.start_time
      let time_e = this.event.end_time === '' ? '00:00': this.event.end_time
      formData.append("start_date", this.event.start_date + ' ' + time_s)
      // end date same as start date
      formData.append("end_date", this.event.start_date + ' ' +time_e)
      formData.append('tickets', JSON.stringify(this.event.tickets));
      formData.append('lineup', JSON.stringify(this.event.lineups));

      if(this.event.id){
        formData.append('id', this.event.id)
      }


      this.$store.dispatch('event/createEvent', formData)
          .then((response)=>{

            if(response.success) {
              this.create_dialog = false;
              this.event = this.default_event;
              this.saving_disabled = false;
              this.stepper_step = 1;
              this.$store.dispatch('event/loadEvents')
            }else{
              this.stepper_step = response.errors[0].tab
            }
          })
    },


  },
  computed:{
    responsiveAndNavClosed(){
      if(this.$props.responsive && this.$store.state.layout.navopen){
        return true
      }
      return false
    }
  },
  data: () => ({
      changes_dialog:false,
      eventWatch:{},
      formIsChanged:false,
      saving_disabled:false,
      stepper_step:1,
      create_dialog:false,
      event:{
        name:'',
        start_date:'',
        end_date:'',
        start_time:'',
        end_time:'',
        location:'',
        public:false,
        online:false,
        tickets:[],
        lineups:[],
        primary_color:'#B2283A',
        secondary_color:'#53A4BE',
        header_img: '',
        bg_img:''
      },
      default_event:{
        name:'',
        start_date:'',
        end_date:'',
        start_time:'',
        end_time:'',
        location:'',
        public:false,
        online:false,
        tickets:[],
        lineups:[],
        primary_color:'#B2283A',
        secondary_color:'#53A4BE',
        header_img: '',
        bg_img:''
      },
  })
}
</script>