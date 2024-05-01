<template>

    <v-card class="rounded-lg" :class="cls" elevation="0">
      <slot></slot>
    </v-card>

</template>
<script>
  export default {
    name: 'panel',
    props:['cls']

  }
</script>
