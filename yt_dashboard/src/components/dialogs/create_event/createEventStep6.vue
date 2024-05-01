<template>

  <div :class="active ? 'active' : ''" class="stepper_item">
    <h2 class="stepper_item_header">{{$t('-createevent.design.header')}}</h2>
    <v-form>
    <v-container fluid style="padding:0!important;">
    <v-row>
      <v-col cols="3">
        <div class="form_field_label">{{$t('-createevent.design.headerfile-label')}}</div>

        <v-btn @click="uploadClick()" text class="secondary_btn blue">
          
          {{$t('-createevent.design.headerfile-btntext')}}
          <v-icon>mdi-upload</v-icon>
        </v-btn>
        <input
              ref="headerfile"
              class="d-none"
              type="file"
              accept="image/*"
              @change="selectHeaderFile"
              name="header_img"
            >

      </v-col>
      <v-col cols="4">
        <v-img class="mr-auto" v-model="form_data.header_img" max-height="50" max-width="50" contain v-bind:src="design.header_img_url"></v-img>
      </v-col>
      <v-col cols="5">
        <div class="form_field_label">
          {{$t('-createevent.design.Primary color')}}
          </div>

        <v-menu offset-y  :close-on-content-click="closeOnClick">
          <template v-slot:activator="{ on }">
            <v-sheet
              :color="form_data.primary_color"
              style="cursor:pointer;"
              elevation="0"
              height="50"
              width="100"
              v-on="on"
            ></v-sheet>

          </template>
          <v-color-picker

            v-model="form_data.primary_color"
            mode="hexa"
            hide-mode-switch

          ></v-color-picker>
        </v-menu>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="3">
        <div class="form_field_label">
          {{$t('-createevent.design.bgfile-label')}}
          </div>
         <v-btn @click="upload2Click()" text class="secondary_btn blue">
          {{$t('-createevent.design.bgfile-btntext')}}
          <v-icon>mdi-upload</v-icon>
              </v-btn>
        <input
              ref="bg_img"
              class="d-none"
              type="file"
              accept="image/*"
              @change="selectBgFile"
              name="bg_img"
            >
      </v-col>
      <v-col cols="4" style="padding-left:0px!important;">

        <v-img v-model="form_data.bg_img" width="100" v-bind:src="design.bg_img_url"></v-img>
      </v-col>
      <v-col cols="5">
        <div class="form_field_label">
          {{$t('-createevent.design.Secondary color')}}
          </div>

        <v-menu offset-y :close-on-content-click="closeOnClick">
          <template v-slot:activator="{ on }">

            <v-sheet
              :color="form_data.secondary_color"
              style="cursor:pointer;"
              elevation="0"
              height="50"
              width="100"
              v-on="on"
            ></v-sheet>

          </template>
          <v-color-picker

            v-model="form_data.secondary_color"
            mode="hexa"
            hide-mode-switch

          ></v-color-picker>
        </v-menu>
      </v-col>
    </v-row>

    </v-container>
    </v-form>
  </div>

</template>
<script>
  import resetForm from "@/mixins/resetForm";
  import watchData from "@/mixins/watchData";

  export default {
    name: 'createEventStep6',
    components:{
    },
    emits:['change'],
    props:['active', 'data', 'unload'],
    mixins:[resetForm, watchData],
    mounted () {

    },
    computed: {
      primary_color: {
        get () {
          return this.form_data.primary_color
        },
        set (v) {

          this.form_data.primary_color = v
        },
      },
      secondary_color: {
        get () {
          return this.form_data.secondary_color
        },
        set (v) {
          this.form_data.secondary_color = v
        },
      },

    },
    methods:{
      selectHeaderFile(event){
        this.form_data.header_img = event.target.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
          this.design.header_img_url = e.target.result;
        };
        reader.readAsDataURL(event.target.files[0]);
      },
      selectBgFile(event){
        this.form_data.bg_img = event.target.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
          this.design.bg_img_url = e.target.result;
        };
        reader.readAsDataURL(event.target.files[0]);
      },
      uploadClick(){
        this.$refs.headerfile.click();
      },
      upload2Click(){
        this.$refs.bg_img.click();
      },
    },
    data:() => ({
      closeOnClick:false,
      form_data:{
        primary_color:'',
        secondary_color:'',
        header_img: '',
        bg_img:''
      },
      design:{
        header_img_url:'',
        bg_img_url:'',
        types: ['hex', 'hexa', 'rgba', 'hsla', 'hsva'],
        type: 'hex',
        hex: '#FF00FF',
        hexa: '#FF00FFFF',
        rgba: { r: 255, g: 0, b: 255, a: 1 },
        hsla: { h: 300, s: 1, l: 0.5, a: 1 },
        hsva: { h: 300, s: 1, v: 1, a: 1 },
      },

    })
  }
</script>
