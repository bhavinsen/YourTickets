<template>
  <v-overlay
    absolute
    :value="visible"
  >
    <div class="text-center">
      <v-progress-circular
        :size="50"
        :width="3"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </div>
  </v-overlay>


</template>
<script>
  export default {
    name: 'overlayloader',
    props:['visible']

  }
</script>
