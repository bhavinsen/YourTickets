<template>
  <v-menu :close-on-content-click="true" offset-y bottom left v-model="menu_open" >

    <template v-slot:activator="{ on, attrs }">
      <v-btn text v-bind="attrs" style="padding-left:0px;" v-on="on" elevation="0">
        <span style="font-size:15px;letter-spacing:normal;">{{items[active].text}}</span>
        <v-img class="ml-2" contain height="10" src="@/assets/icons/chevron_down.svg"></v-img>
      </v-btn>

    </template>
    <v-card>
      <v-card-text style="padding:10px!important;">

        <v-list class="btn-list-popup">
          <v-list-item-group v-model="active" @change="$emit('change', items[active])">
            <v-list-item active-class="item-small-custom" v-for="(item, i) in items" :key="i">
              <v-icon :color="item.iconColor" small >{{ item.icon }}</v-icon>{{ item.text }}
            </v-list-item>

          </v-list-item-group>
        </v-list>
        </v-card-text>
    </v-card>
  </v-menu>

</template>
<script>
  export default {
    name: 'simpleDropDown',
    props:['items'],
    emits:['change'],
    methods:{

    },
    data: () => ({
      menu_open:false,
      active:0,

    })
  }
</script>
