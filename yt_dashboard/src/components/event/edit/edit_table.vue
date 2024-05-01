<template>


<v-form>
  <v-dialog v-model="delete_dialog" max-width="500px">
      <v-card>
        <v-card-title class="headline text-center">{{$t('Are you sure you want to delete this item?')}}</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="secondary_btn blue" text @click="delete_dialog = false">{{$t('Cancel')}}</v-btn>
          <v-btn class="primary_btn" text @click="deleteItem">{{$t('Ok')}}</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  <v-data-table
      hide-default-footer
      :headers="$props.headers"
      :items="indexedItems"
      disable-sort
      class="custom_dense"
      disable-pagination
      fixed-header
      :height="height"
      :loading="loading"
      item-key="key"
      mobile-breakpoint="0"
  >

    <template v-slot:body.prepend="">

      <slot :add="add" :addItemObject="addItemObject" name="add_form"></slot>

    </template>

    <template
      v-for="header in $props.headers"
      v-slot:[`item.${header.value}`]="{item}"
      >
      <slot :name="[`item.${header.value}`]" :item="item" :editItem="editItemObjects[_getItemIndex(item)]">{{getVal(item, header.value)}}</slot>
    </template>


    <template v-slot:item.actions="{ item }">


      <div class="text-md-right" style="margin-right:5px;white-space: nowrap;">
          <slot name="action_buttons" :item="item"></slot>

          <template v-if="editItemObjects[_getItemIndex(item)]">
            <v-btn class="d-inline-block" small text icon elevation="0"
                   @click="cancelEditItemMode(item)"><v-icon>mdi-cancel</v-icon></v-btn>
            <v-divider vertical style="margin-bottom:0!important;"></v-divider>
            <v-btn small class="d-inline-block" text icon elevation="0"
                   @click="editItemSave(item)"><v-icon>mdi-floppy</v-icon></v-btn>
          </template>
          <template v-else >

            <v-btn v-if="!disableEdit" class="d-inline-block" small text icon elevation="0" @click="editItemMode(item)">
              <v-img src="@/assets/icons/pencil.svg" contain height="12" width="12"></v-img>
            </v-btn>
            <v-divider v-if="!disableEdit" vertical style="margin-bottom:-4px!important;"></v-divider>
            <v-btn class="d-inline-block" small text icon elevation="0" @click="showDeleteConfirmDialog(item)">
              <v-img src="@/assets/icons/trash.svg" contain height="12" width="12"></v-img>
            </v-btn>
          </template>
        </div>
    </template>

  </v-data-table>
</v-form>
</template>

<script>
//v-slot:[`item.${boolHeader.value}`]="{ item }"
export default {
  name: 'edit_table',
  props:['headers', 'defaultItem', 'items', 'loading', 'disableEdit', 'height'],
  emits:['create_item_saved', 'delete_item_confirmed', 'edit_item_saved'],
  mounted () {
    this.addItemObject = Object.assign({}, this.$props.defaultItem)
  },
  computed: {
    indexedItems () {
      return this.$props.items.map((item, index) => ({
        key: index,
        ...item
      }))
    }
  },
  // watch:{
  //   'addfunc'(val) {
  //     console.log(val)
  //   }
  // },
  methods:{
    getVal(item, path){
      return path.split(".").reduce((res,prop) => res[prop], item);
    },
    add(data){
      data = data ? data : this.addItemObject
      this.items.push(data)
      this.$emit('create_item_saved',data)
      //RESET
      this.addItemObject = Object.assign({}, this.$props.defaultItem)

    },
    editItemMode(item){
      //add an object into edit mode
      //this.items and this.editItemObjects share the same index for
      //mainly for easy lookups
      this.$set(
          this.editItemObjects,
          this._getItemIndex(item),
          Object.assign({}, item)
      )
    },
    showDeleteConfirmDialog(item){
      this.temp_delete_item = item;
      this.delete_dialog = true;
    },
    deleteItem(){

      let itemIndex = this._getItemIndex(this.temp_delete_item)
      this.$emit('delete_item_confirmed', this.items[itemIndex])
      this.items.splice(itemIndex, 1)
      //remove from editmode
      this.editItemObjects.splice(itemIndex, 1)
      this.delete_dialog = false

    },
    cancelEditItemMode(item){
      this.editItemObjects.splice(this.editItemObjects.indexOf(item), 1)
    },
    editItemSave(item){
      let itemIndex = this._getItemIndex(item)
      Object.assign(this.items[itemIndex], this.editItemObjects[itemIndex])
      //RESET THIS ROW EDIT MODE
      this.editItemObjects.splice(itemIndex, 1)
      this.$emit('edit_item_saved', this.items[itemIndex])
    },
    _getItemIndex(item){
      //return this.items.indexOf(item)
      return this.indexedItems.indexOf(item)
    }
  },
  data: () => ({
    delete_dialog:false,
    //moved to props
    // headers: [],
    //holds all the items
    // moved to props
    // items:[],
    //defaultItem moved to props
    // defaultItem:{},
    //this holds a list of items currently being edited
    editItemObjects:[],
    //copied object from defaultItem
    //these are bound to the add form input fields
    addItemObject:{}
  })
}
</script>