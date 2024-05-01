export default {
    methods:{
        formChanged(){
            this.formIsChanged = true;
            this.$emit('change', this.form_data)
        }
    },
    watch: {
      'data'(v){
        this.formIsChanged = false
        //copy over the items that are needed
        for (const [key] of Object.entries(this.form_data)) {
          this.form_data[key] = v[key]
        }
        // this.form_data.name = v.name
        this.dataWatch = this.$watch('form_data', this.formChanged, {'deep':true});
      },
      'unload'(v){
        if(v === true){
          this.dataWatch()
        }
      }
    },
    data: () => ({
        formIsChanged:false,
        form_data: {}
    })
}