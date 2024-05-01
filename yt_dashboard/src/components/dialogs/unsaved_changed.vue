<template>

  <v-dialog v-model="show_dialog" max-width="500px">
    <v-card>
      <v-card-title class="headline text-center justify-center">
        {{ $t('-unsaved_changes.message') }}
      </v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="secondary_btn blue" text @click="changes_dialog = false">{{$t('Cancel')}}</v-btn>
        <v-btn class="primary_btn" text @click="changes_dialog = false;create_dialog=false">{{$t('Ok')}}</v-btn>
        <v-spacer></v-spacer>
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
  emits: ['hide_dialog'],
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