<template>
  <div>
    <div style="display:inline-block;font-size: 10px;padding-right:10px;" >
      {{ val }}
    </div>
    <v-switch
        value
        hide-details
        input-value="true"
        class="small"
        v-model="val"
        true-value="percentage"
        false-value="number"
        @change="$emit('change', val)"

      style="padding-top:0px;margin-top:0px;display:inline-block;"
    ></v-switch>
  </div>

</template>
<script>
  export default {
    name: 'percentageSwitcher',
    props:['visible'],
    emits:['change'],
    method:{

    },
    data: () => ({
      val:'percentage'
    })
  }
</script>
