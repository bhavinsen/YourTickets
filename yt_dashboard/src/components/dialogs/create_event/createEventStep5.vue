<template>

  <div :class="active ? 'active' : ''" class="stepper_item">
    <h2 class="stepper_item_header">{{$t('-createevent.lineup.header')}}</h2>

    <edit_table
        :headers="lineup_table.headers"
        :default-item="lineup_table.defaultItem"
        :items="form_data.lineups"
        height="230"
    >
      <template v-slot:add_form="{addItemObject, add}">

        <tr>
          <td>
            <v-form ref="add_form">
              <v-text-field
                single-line
                dense
                outlined
                :placeholder="$t('-createevent.lineup.add-placeholder')"
                autofocus
                v-model.trim="addItemObject.artist"
                ref="lineup_artist"
                hide-details
                :rules="form_rules.lineup_artist"
                @input="resetValidation($refs.lineup_artist, 'lineup_artist')"
                @blur="valid($refs.lineup_artist,'lineup_artist')"
                :error-messages="form_errors.lineup_artist"
              ></v-text-field>
            </v-form>
          </td>
          <td class="text-md-right">
            <v-btn class="primary_btn d-inline-block" :disabled="addItemObject.artist === ''"   small elevation="0" @click="add()"><v-icon>mdi-plus</v-icon></v-btn>
          </td>
        </tr>

      </template>

      <template v-slot:item.artist="{ item, editItem }">
        <v-form ref="edit_form">
        <v-text-field single-line dense v-if="editItem"
                          outlined
                          :placeholder="$t('-createevent.lineup.edit-placeholder')"
                          v-model="editItem.artist"></v-text-field>
            <span v-else> {{ item.artist }}</span>
        </v-form>
      </template>
    </edit_table>

  </div>

</template>
<script>
  import resetForm from "@/mixins/resetForm";
  import {required} from "@/plugins/validate";
  import edit_table from "@/components/event/edit/edit_table";

  import watchData from "@/mixins/watchData";

  export default {
    name: 'createEventStep5',
    components:{
      edit_table
    },
    emits:['change'],
    props:['active', 'data', 'unload'],
    mixins:[resetForm, watchData],
    mounted () {

    },
    watch:{
      'active'(v){
        if(v === true){
          this.$refs.add_form.resetValidation()
          this.resetValidation(this.$refs.lineup_artist, 'lineup_artist')
        }
      }
    },
    computed: {


    },
    data:(scope) => ({
      form_data:{
        lineups:[],
      },

      form_errors: {
        lineup_artist: []
      },
      form_rules: {
        lineup_artist: [
            required()
        ]
      },
      lineup_table:{
        defaultItem:{
          id: 0,
          artist: '',
        },
        headers:[{
            text: scope.$t('-createevent.lineup.tableheader'),
            align: 'start',
            value: 'artist',
          },
          {text: '', value: 'actions', sortable: false },
          ]
      },

    })
  }
</script>
