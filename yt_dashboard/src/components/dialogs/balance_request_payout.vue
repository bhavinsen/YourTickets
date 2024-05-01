<template>

  <v-dialog eager scrollable @click:outside="$emit('hide')" v-model="show_dialog" width="300" content-class="overflow-visible" >


    <v-overlay
      absolute
      :value="overlay_visible"
      opacity="0.9"
    >
      <div class="text-center text-h6" style="padding:20px;">
        {{ $t('-received request balance payout.message') }}
      </div>
      <div class="text-center">
        <v-btn elevation="0" class="primary_btn" @click="$emit('hide')">OK</v-btn>
      </div>
    </v-overlay>

    <v-card >

        <v-btn @click="$emit('hide')" v-show="$vuetify.breakpoint.mdAndUp" icon class="close_button"><v-img src="@/assets/icons/close.svg"></v-img></v-btn>
        <v-btn @click="$emit('hide')" icon v-show="$vuetify.breakpoint.smAndDown" class="close_button_mobile"><v-icon>mdi-close</v-icon></v-btn>
        <v-card-title style="padding-bottom:30px;padding-top:34px">
          {{ $t('Request for payout') }}
        </v-card-title>
        <v-card-text style="height:200px;">
          <v-form ref="form">
            <v-container fluid>
              <v-row>
                <v-col cols="12" class="" >
                  <div class="form_field_label">{{ $t('Amount') }}</div>

                  <v-text-field ref="amount"
                                :rules="rules.amount"
                                :error-messages="form_errors.amount"
                                outlined flat
                                type="number"
                                hide-details
                                prefix="€"
                                step=".01"
                                min="0"
                                v-model="amount"
                                @input="resetValidation($refs.amount, 'amount')"
                                @blur="valid($refs.amount,'amount')"
                                placeholder="Bedrag">
                      <errortooltip slot="append" :errors="form_errors.amount"></errortooltip>

                  </v-text-field>


                </v-col>
                <v-col cols="12" class="text-center" >OF</v-col>
                <v-col cols="12" class="text-center" >
                  <v-btn elevation="0" class="primary_btn" @click="payout_all">{{ $t('Everything') }}</v-btn>
                </v-col>

              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-spacer></v-spacer>
        <v-divider class="d-block" style="margin-left:15px;margin-right:15px;"></v-divider>
        <v-card-actions>

          <v-btn
              style="margin-left:0;"
              @click="$emit('hide')"
              elevation="0"
              class="secondary_btn blue">{{ $t('Cancel') }}</v-btn>

          <v-spacer></v-spacer>


          <v-btn  elevation="0" class="primary_btn" :disabled="save_btn_disabled()" @click="request_payout">{{ $t('Request') }}</v-btn>
        </v-card-actions>
    </v-card>

  </v-dialog>

</template>

<script>

import errortooltip from "@/components/core/errortooltip";
import {required, isFloat, max, min} from "@/plugins/validate";



export default {
  name: 'balance_request_payout',
  props: ['show_dialog'],
  emits: ['hide'],
  components:{
    errortooltip
  },
  mounted () {


  },
  methods: {
    request_payout(){
      this.saving_disabled = true
      this.$store.dispatch('account/request_payout', this.amount).then(()=>{
        this.overlay_visible = true
      })

    },
    payout_all(){
      this.amount = this.account.saldo
      this.resetValidation(this.$refs.amount, 'amount')
    },
    valid(el, key){
      if(!el.valid && el.errorMessages.length === 0){
        this.form_errors[key].push(el.errorBucket[0]);
      }else{
        this.form_errors[key] = []
      }
    },
    resetValidation(el, key){
      el.resetValidation()
      this.form_errors[key] = []
    },
    save_btn_disabled(){
      if (!this.$refs.amount) return true
      if(this.saving_disabled) return true
      return !this.$refs.amount.valid;
    },
    reset(){
      this.amount = 0
      this.saving_disabled = false
      this.overlay_visible = false
    }
  },
  computed:{

  },
  watch:{
    'show_dialog'(val) {
      if(val === true){
        this.reset()
        this.$store.cache.dispatch('account/load').then((account)=>{
          this.account = account;
          this.rules.amount.push(max(this.account.saldo))
        })
        this.resetValidation(this.$refs.amount, 'amount')

      }
    }
  },
  data: () => ({
    overlay_visible:false,
    saving_disabled: false,
    form_errors: {
      amount: [],
    },
    account:{},
    amount:0,
    rules:{
      amount:[
          required(),
          isFloat(),
          min(1)
      ]
    }

  })
}
</script>