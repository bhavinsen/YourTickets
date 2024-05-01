<template>

  <v-dialog v-model="show_dialog" max-width="500px">
    <v-card>
      <v-card-title class="headline text-center justify-center">
        {{ $t('-unsaved_changes.message') }}
        
      </v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="secondary_btn blue" text @click="changes_dialog = false">
          {{ $t('Cancel') }}
          </v-btn>
        <v-btn class="primary_btn" text @click="changes_dialog = false;create_dialog=false">
          {{ $t('Ok') }}
          </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>
<script>


  //options
  // closable
  // small(500) and big(802)

  //slot for content

  //nog een comp for dialogMessage title center

  export default {
    name: 'dialog',
    mounted () {

    },
    watch: {

    },
    methods:{

    },
    computed: {


    },
    data:() => ({




    })
  }
</script>
