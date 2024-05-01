<template>

  <div :class="active ? 'active' : ''" class="stepper_item">
      <h2 class="stepper_item_header">
        {{ $t('-createevent.where.header')}}
        </h2>
      <v-form>
        <v-container fluid>
          <v-row>
            <v-col cols="4" >

              <div class="form_field_label">
                {{ $t('-createevent.where.Online event') }}
                </div>

              <v-switch
                v-model="form_data.online"
                style="padding-top:0px;margin-top:0px;display:inline-block;"
              ></v-switch>
              <div style="display:inline-block;color:#66C5E1;" v-if="form_data.online">
                {{ $t('-createevent.where.This event is online') }}
                </div>
              <div class="form_field_label">{{ $t('-createevent.where.Location') }}</div>

              <v-text-field outlined flat v-model="form_data.location"></v-text-field>
            </v-col>
            <v-col cols="7">
              <v-img src="@/assets/map.png" style="height:200px;"></v-img>

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
    name: 'createEventStep3',
    components:{
    },
    emits:['change'],
    props:['active', 'data', 'unload'],
    mixins:[resetForm, watchData],
    mounted () {

    },
    computed: {


    },
    data:() => ({
      form_data:{
        online:false,
        location:''
      },

      form_errors: {

      },
      form_rules: {

      }

    })
  }
</script>
