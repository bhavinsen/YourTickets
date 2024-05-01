export default {
    methods:{
        valid(el, key){
          if(!el.valid && el.errorMessages.length === 0){
            this.form_errors[key].push(el.errorBucket[0]);
          }else if(el.valid){
            this.form_errors[key] = []
          }
        },
        resetValidation(el, key){
          el.resetValidation()
          this.form_errors[key] = []
        },
    },
    data: () => ({
        form_errors:[]
    })
}