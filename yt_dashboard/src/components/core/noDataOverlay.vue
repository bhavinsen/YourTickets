<template>
  <v-overlay
    absolute
    style="background: linear-gradient(180deg, rgba(2,0,36,0) 0%, rgba(255,255,255,1) 100%);"

    v-show="visible"
    opacity="0"
  >
  </v-overlay>


</template>
<script>
  export default {
    name: 'noDataOverlay',
    props:['visible']

  }
</script>
