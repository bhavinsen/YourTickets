<template>

  <div :class="active ? 'active' : ''" class="stepper_item">
    <h2 class="stepper_item_header">
      {{ $t('-createevent.event.header') }}
      </h2>
    <v-form ref="tab1">
      <div class="form_field_label">
        {{ $t('-createevent.event.Event name') }}
        </div>

      <v-text-field ref="event_name"
                    :rules="form_rules.name"
                    :error-messages="form_errors.name"
                    outlined flat
                    hide-details
                    v-model="form_data.name"
                    @input="resetValidation($refs.event_name, 'name')"
                    @blur="valid($refs.event_name,'name')"
                    :placeholder="$t('-createevent.event.Fille in a event name')">
          <errortooltip slot="append" :errors="form_errors.name"></errortooltip>

      </v-text-field>
    </v-form>
  </div>

</template>
<script>
  import resetForm from "@/mixins/resetForm";
  import {required} from "@/plugins/validate";
  import errortooltip from "@/components/core/errortooltip";
  import watchData from "@/mixins/watchData";

  export default {
    name: 'createEventStep1',
    components:{
      errortooltip
    },
    emits:['change'],
    props:['active', 'data', 'unload'],
    mixins:[resetForm, watchData],
    mounted () {

    },
    computed: {


    },
    data:(scope) => ({
      form_data:{
        name:'',
      },

      form_errors: {
        name: [],
      },
      form_rules: {
        name: [
          required(scope.$t('-createevent.event.Event name is required')) 
        ],
      }

    })
  }
</script>
