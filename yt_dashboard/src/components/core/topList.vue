<template>

   <panel >
        <overlayloader :visible="!loaded"></overlayloader>
        <no-data-overlay v-if="noDataOverlay" :visible="noData"></no-data-overlay>
        <v-toolbar dense flat>
          <simpleDropDown v-if="showDropdown" @change="change_item" :items="menu_items" ></simpleDropDown>
          <v-spacer></v-spacer>
          <v-btn icon @click="page=1">
            <v-img class="justify-end" style="width:12px;height:12px;color:black;transform: rotate(180deg);" contain src="@/assets/icons/chevron_right_black.svg"></v-img>
          </v-btn>
          <v-btn icon @click="page=2">
            <v-img class="justify-end" style="width:12px;height:12px;color:black;" contain src="@/assets/icons/chevron_right_black.svg"></v-img>
          </v-btn>
        </v-toolbar>
        <v-card-text>
          <v-card
            v-for="(item, key) in getItems" :key="key"
            class="d-flex pa-2 item-small-custom"
            outlined
            tile
          >
            <div class="mr-auto">{{ key + 1 + (page_size*(page-1))}}. {{ item.value }}</div>
            <div class="right">{{ item.total }}</div>
          </v-card>
        </v-card-text>
      </panel>

</template>
<script>
  import overlayloader from "@/components/core/overlayloader";
  import simpleDropDown from "@/components/core/simpleDropDown";
  import noDataOverlay from "@/components/core/noDataOverlay";

  export default {
    name: 'topList',
    props:['showDropdown', 'title', 'noDataOverlay'],
    components:{overlayloader, simpleDropDown, noDataOverlay},
    methods:{
      load(dispatchName, params){
        this.loaded = false;
        this.noData = false;
        this.params = params
        if(this.showDropdown){

          if(this.selectedItem === false){
            this.selectedItem = this.menu_items[0]
          }
          params['chart_type'] = this.selectedItem.selection
        }

        this.$store.dispatch(dispatchName, params).then((response) => {
            if(response.data.length === 0){
              this.noData = true;
              this.items = this.dummiData;
            }else{
              this.items = response.data
            }
            this.loaded = true;
        })
      },
      change_item(item){
        let params = this.params
        this.selectedItem = item
        this.load('stats/getTop5Chart',params)
      }
    },
    computed:{
      getItems(){
        return this.items.slice((this.page - 1) * this.page_size, this.page * this.page_size);
      },
    },
    data: (scope) => ({
      params:{},
      dummiData:[
          {"value": "", "total": 10},
          {"value": "", "total": 5},
          {"value": "", "total": 3},
          {"value": "", "total": 3},
          {"value": "", "total": 2}
      ],
      noData:false,
      loaded:false,
      selectedItem:false,
      items:[],
      page:1,
      page_size:5,
      menu_items:[{
        text: scope.$t('Amount tickets sold'),
        selection: 'sold_tickets'

      },{
        text: scope.$t('Visitors'),
        selection: 'visitors'
      },{
        text: scope.$t('Revenue'),
        selection: 'profit'
      }],
    })
  }
</script>
