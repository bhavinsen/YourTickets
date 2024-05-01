import Api from '@/service/Api.js'

const state = () => ({
    statistics:{}
})

const getters = {

    getevents: () =>{
        return Api().get('/api/multiticketshop/getevents');
    },
    getEventsForShop: () => (multiticketshop_id) =>{
        return Api().get('/api/multiticketshop/'+multiticketshop_id+'/getevents');
    }
}

const actions = {
    create(context, data) {
        return Api().post('/api/multiticketshop/create', data);
    },
    update(context, data){
        return Api().post('/api/multiticketshop/'+data.multiticketshop_id+'/update', data);
    },
    delete(context, data){
        return Api().post('/api/multiticketshop/'+data.multiticketshop_id+'/delete', data);
    },
    request_url(context, data) {
        return Api().post('/api/multiticketshop/'+data.multiticketshop_id+'/request', data);
    },
    getall: () =>{
        return Api().get('/api/multiticketshop/getall');
    },
}
const mutations = {}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}