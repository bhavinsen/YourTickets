<template>

    <v-card class="rounded-lg" :class="cls" elevation="0" >
      <div class="circle_bg"></div>
      <div class="circle_bg2"></div>
      <div class="circle_bg3"></div>

      <v-img src="@/assets/circle_bg3.svg" class="circle_bg3"></v-img>

      <v-card-text>
        <v-img :src="icon" class="panel-icon d-block" contain max-height="40" max-width="40" width="40" height="40"></v-img>
        <div class="panel-line">
          {{title}}
        </div>
        <div class="panel-number">{{number}}</div>
      </v-card-text>
    </v-card>

</template>
<script>

  export default {
    name: 'highlightPanel',
    props:['cls', 'icon', 'title', 'number']

  }
</script>
