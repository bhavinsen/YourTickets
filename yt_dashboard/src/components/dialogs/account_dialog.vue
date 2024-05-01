<template>

  <v-dialog
    v-model="local_show_dialog"
    content-class="overflow-visible"
    width="534"
    persistent
    eager
    @click:outside="closeDialog"
    :fullscreen="$vuetify.breakpoint.smAndDown"
  >

    <v-dialog v-model="saved_dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline text-center justify-center">
            {{ $t('Your changes are saved') }}
            
          </v-card-title>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="primary_btn" text @click="saved_dialog = false;">{{ $t('Ok') }}</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>

    <v-dialog v-model="changes_dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline text-center justify-center">
            {{ $t('-unsaved_changes.message') }}
          </v-card-title>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="secondary_btn blue" text @click="changes_dialog = false">{{ $t('Cancel') }}</v-btn>
            <v-btn class="primary_btn" text @click="changes_dialog = false;local_show_dialog=false">{{ $t('Ok') }}</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>

    <v-dialog v-model="password_dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">
            {{ $t('Change your password') }}
          </v-card-title>
          <v-card-text>
            <v-form ref="password_form">
              <v-container fluid>
                <v-row>
                  <v-col cols="4">
                    {{ $t('Current password') }}
                  </v-col>
                  <v-col cols="5">
                    <v-text-field
                      outlined
                      flat
                      type="password"
                      :placeholder="$t('password')"
                      height="32"
                      v-model="password_data.old"
                      required
                      :error-messages="password_errors.old"
                      :rules="form_rules.password"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="4">
                    {{ $t('New password') }}
                    
                  </v-col>
                  <v-col cols="5">
                    <v-text-field
                      outlined
                      flat
                      type="password"
                      :placeholder="$t('new password')"
                      height="32"
                      v-model="password_data.new"
                      :error-messages="password_errors.new"
                      required
                      :rules="form_rules.password"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="4">
                    {{ $t('New password for verification') }}
                  </v-col>
                  <v-col cols="5">
                    <v-text-field
                      outlined
                      flat
                      type="password"
                      :placeholder="$t('new password')"
                      height="32"
                      :error-messages="password_errors.new_check"
                      v-model="password_data.new_check"
                      required
                      :rules="form_rules.password"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>

          </v-card-text>
          <v-card-actions>

            <v-btn class="secondary_btn blue" text @click="password_dialog = false">{{ $t('Cancel') }}</v-btn>
            <v-spacer></v-spacer>
            <v-btn class="primary_btn" text @click="change_password">{{ $t('Save') }}</v-btn>

          </v-card-actions>
        </v-card>
      </v-dialog>

    <v-card class="d-flex flex-column">
<!--      <v-btn @click="closeDialog" icon class="close_button"><v-img src="@/assets/icons/close.svg"></v-img></v-btn>-->

      <v-btn @click="closeDialog" v-show="$vuetify.breakpoint.mdAndUp" icon class="close_button"><v-img src="@/assets/icons/close.svg"></v-img></v-btn>
      <v-btn @click="closeDialog" icon v-show="$vuetify.breakpoint.smAndDown" class="close_button_mobile"><v-icon>mdi-close</v-icon></v-btn>


      <v-card-title style="padding-bottom:22px;padding-top:34px">
        {{ $t('My account') }}
        
      </v-card-title>
      <v-card-text style="color:black!important;">

        <v-divider class="grey"></v-divider>


        <v-form v-model="form_valid" ref="create_form" lazy-validation>
          <v-container fluid>
            <h2 class="form_header">{{$t('Your information')}}</h2>
            <v-row>
              <v-col
                cols="3"
                style="padding-top:16px;"
              >
              {{$t('Name')}}
              </v-col>
              <v-col cols="3">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('Name')"
                  height="32"
                  v-model="form_data.first_name"
                  required
                  :rules="form_rules.first_name"
                ></v-text-field>
              </v-col>
              <v-col cols="3">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('Last name')"
                  height="32"
                  v-model="form_data.last_name"
                  required
                  :rules="form_rules.last_name"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="3"
                style="padding-top:16px;"
              >
              {{$t('Profile picture')}}
                
              </v-col>
              <v-col cols="1">
                <v-avatar

                  color="#C4C4C4"
                  size="40"
                >
                  <img :src="form_data.avatar">
                </v-avatar>

<!--                <v-img v-model="form_data.avatar" max-height="50" max-width="50" v-bind:src="avatar_url"></v-img>-->

              </v-col>
              <v-col cols="3">
                <v-btn style="margin-left:29px" @click="upload()" text class="primary_btn">{{ $t('Upload photo') }}<v-icon>mdi-upload</v-icon>
                  </v-btn>
                <input
                  ref="file"
                  class="d-none"
                  type="file"
                  accept="image/*"
                  @change="onFileChanged"
                >

              </v-col>
            </v-row>

            <v-row>
              <v-col cols="3" style="padding-top:16px;">
                {{$t('E-mail address')}}
                
              </v-col>
              <v-col cols="5" style="padding-top:16px;">
<!--                <v-text-field-->
<!--                  outlined-->
<!--                  flat-->
<!--                  placeholder="Jouw e-mail adres"-->
<!--                  height="32"-->
<!--                  v-model="form_data.email"-->
<!--                  required-->
<!--                  :rules="form_rules.email"-->
<!--                ></v-text-field>-->
                {{form_data.email}}
              </v-col>
            </v-row>
            <v-divider class="grey" style="margin-top:12px;"></v-divider>

            <v-row>
              <v-col cols="3" style="padding-top:16px;">
                {{$t('Password')}}
                
              </v-col>
              <v-col cols="5" >
                <v-btn class="text-decoration-underline" style="font-size:12px!important;letter-spacing: normal" text plain color="black" @click="password_dialog=true" >{{$t('Change password')}}</v-btn>
              </v-col>
            </v-row>
            <v-divider class="grey" style="margin-top:12px;"></v-divider>
            <h2 class="form_header">
              {{$t('Company information')}}
              </h2>
            <v-row>
              <v-col cols="3" style="padding-top:16px;">
                {{$t('Company name')}}
                
              </v-col>
              <v-col cols="5">

                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('Company name')"
                  height="32"
                  ref="companyname"
                  v-model="form_data.company_name"
                  hide-details
                  :rules="form_rules.company_name"
                >

                  <v-tooltip v-if="$refs['companyname'] && $refs['companyname'].hasError" slot="append" color="error" right open-delay="0">
                    <template v-slot:activator="{ on }">
                        <v-icon v-on="on" color="error" dark>
                          mdi-alert-circle-outline
                        </v-icon>
                      </template>
                    <span>{{$refs['companyname'].errorBucket[0]}}</span>
                  </v-tooltip>
                </v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3" style="padding-top:16px;">
                {{$t('COC number')}}
              </v-col>
              <v-col cols="5">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('COC no')"
                  height="32"
                  v-model="form_data.coc_number"
                  :rules="form_rules.coc_number"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3" style="padding-top:16px;">
                {{$t('Vat number')}}
                
              </v-col>
              <v-col cols="5">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('Vat no')"
                  height="32"
                  v-model="form_data.tax_number"
                  :rules="form_rules.tax_number"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3" style="padding-top:16px;">
                {{$t('Address')}}
                
              </v-col>
              <v-col cols="3">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('Postal code')"
                  height="32"
                  v-model="form_data.postal_code"

                  :rules="form_rules.postal_code"

                ></v-text-field>
              </v-col>
              <v-col cols="2">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('House number')"
                  height="32"
                  v-model="form_data.house_number"

                  :rules="form_rules.house_number"
                ></v-text-field>
              </v-col>
              <v-col cols="2">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('Addition')"
                  height="32"
                  v-model="form_data.house_number_addition"

                  :rules="form_rules.house_number_addition"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3" style="padding-top:16px;">
                {{ $t('Place') }}
              </v-col>
              <v-col cols="5">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('Place')"
                  height="32"
                  v-model="form_data.place"
                  :rules="form_rules.place"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-divider class="grey" style="margin-top:12px;"></v-divider>
            <h2 class="form_header">{{ $t('Bank details') }}</h2>
            <v-row>
              <v-col cols="4">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('Account holder')"
                  height="32"
                  v-model="form_data.account_owner"
                  required
                  :rules="form_rules.account_owner"
                ></v-text-field>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('-input-field-placeholder-iban')"
                  height="32"
                  v-model="form_data.account_number"
                  required
                  :rules="form_rules.account_number"
                ></v-text-field>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  outlined
                  flat
                  :placeholder="$t('-input-field-placeholder-bic')"
                  height="32"
                  v-model="form_data.big"
                  :rules="form_rules.big"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-spacer></v-spacer>
      <v-divider class="d-block" style="margin-left:15px;margin-right:15px;"></v-divider>
      <v-card-actions>
        <v-btn
          class="secondary_btn blue"
          text
          @click="closeDialog"
        >
        {{ $t('Cancel') }}
          
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          class="primary_btn"
          text
          @click="validate_create_form"
        >
        {{ $t('Save') }}
          
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<script>

import {required, namesAndSpecials} from "@/plugins/validate";

export default {
  name: 'account_dialog',
  props: ['show_dialog'],
  emits: ['hide_dialog'],
  components:{
    // errortooltip
  },
  mounted () {


  },
  watch:{
    'show_dialog'(val) {
      if(val === true){
        this.local_show_dialog = true
      }
    },
    'local_show_dialog'(val){
      if(val === true){
        this.load_data()
      }
      if(val === false){
        this.$emit('hide_dialog')
        this.dataWatch()
        this.form_changed = false

        // this.eventWatch()
      }
    },

  },
  methods: {
    change_mail(){

    },
    change_password(){
      // this.$refs.password_form.reset()

      if(this.password_data.new !== this.password_data.new_check){
        this.password_errors.new.push(this.$t('Fields are not equal'))
        this.password_errors.new_check.push(this.$t('Fields are not equal'))
      }else{
        this.$store.dispatch('account/change_password', this.password_data).then((response)=>{
          let data = response.data

          if(!data.success){
            this.password_errors.old.push(this.$t('Wrong password'))
          }else{
            this.$refs.password_form.reset()
            this.password_dialog = false

          }

        })
      }
    },
    formChanged(){
      this.form_changed = true
    },
    upload(){
      this.$refs.file.click()
      // this.dataWatch = this.$watch('form_data', this.formChanged, {'deep':true});
    },
    onFileChanged(event){
      this.form_data.avatar = event.target.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
          this.avatar_url = e.target.result;
        };
        reader.readAsDataURL(event.target.files[0]);
    },

    validate_create_form(){

      let formData = new FormData();
      for (let formKey in this.form_data) {

        formData.append(formKey, this.form_data[formKey]);
      }
      // formData.append("avatar", this.$refs.file.files[0]);

      if(this.account_edit_mode){

        // console.log(this.create_form)
        this.$store.dispatch('account/update2', formData).then((data)=>{
          if(data.success){
            this.form_changed=false
            this.closeDialog()
            this.saved_dialog = true
          }
        })


      }else{
        // this.$store.dispatch('account/create', formData)
        // .then((data) =>{
        //   console.log('after create',data)
        //
        // })

      }

    },
    load_data(){
      this.$store.dispatch('account/load').then((data)=>{
        this.form_data = Object.assign({}, data)
        this.dataWatch = this.$watch('form_data', this.formChanged, {'deep':true});
      })
    },
    closeDialog(){
      if(this.form_changed === true){
        this.changes_dialog = true
      }else{
        this.local_show_dialog = false
      }
    },

  },
  computed:{
    // ...mapGetters({
    //     form_data: 'account/getall',
    //   }),
  },

  data: (scope) => ({
    account_edit_mode:true,
    form_valid:true,
    local_show_dialog:false,
    form_changed:false,
    changes_dialog:false,
    password_dialog:false,
    saved_dialog:false,
    avatar_url:'',
    form_data:{
      avatar:''
    },
    password_data:{
      new:'',
      new_check:'',
      old:'',

    },
    password_errors:{
      new:[],
      new_check:[],
      old:[],

    },

    form_rules:{
        first_name: [
          v => !!v || scope.$t('Name is required'),
          v => (v && v.length <= 50) || scope.$t('Name must be less than 50 characters'),
          namesAndSpecials()
        ],
        last_name: [
          v => !!v || scope.$t('Last name is required'),
          v => (v && v.length <= 50) || scope.$t('Last name must be less than 50 characters'),
          namesAndSpecials()
        ],
        postal_code: [
          // v => !!v || 'Postal code is required',
          // v => (v && v.length <= 6) || 'Like 1234AA',
        ],
        house_number: [
          // v => !!v || 'House nr is required',
          // v => (v && v.length <= 10) || 'House number must be less than 10 characters',
        ],
        place: [
          // v => !!v || 'Place is required'
        ],
        email: [
          v => !!v || scope.$t('E-mail is required'),
          v => /.+@.+\..+/.test(v) || scope.$t('E-mail must be valid'),
        ],
        company_name:[
            // v => !!v || 'Company name is required',
        ],
        coc_number:[
            // v => !!v || 'Kvk is required',
        ],
        tax_number:[
            // v => !!v || 'Btw is required',
        ],
        account_owner:[
            // v => !!v || 'Account holder is required',
        ],
        account_number:[
            // v => !!v || 'Account number is required',
        ],
        big:[],
        password:[
            required()
        ]
      }


  })
}
</script>