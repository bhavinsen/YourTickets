<template>


  <v-tooltip color="red" top v-if="errors.length > 0"  >
      <template v-slot:activator="{ on, attrs }">
        <v-icon
          v-bind="attrs"
          v-on="on"
          color="red"
        >
          mdi-alert-circle
        </v-icon>
      </template>
      <v-list dense color="red">
        <v-list-item
            style="color:white!important;"
            v-for="(item, i) in errors"
            :key="i"
          >
          {{item}}
        </v-list-item>
      </v-list>

    </v-tooltip>

</template>

<script>
//  not yet used, work in progress
  export default {
    name: 'errortooltip',
    props:['errors'],


    // watch:{
    //   errors: function(newVal, oldVal){
    //     console.log('watch', newVal, oldVal)
    //   }
    // },
    data: () => ({
      event_errors:[]
    })

  }
</script>
