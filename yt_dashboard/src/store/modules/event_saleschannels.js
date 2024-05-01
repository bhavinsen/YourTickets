import Api from '@/service/Api.js'

const state = () => ({
    statistics:{}
})

const getters = {
    getall: () => (id) => {
        return Api().get('/api/event/'+id+'/sales_channels/getall');
    },

}

const actions = {
    create(context, data) {
        return Api().post('/api/event/'+data.event_id+'/sales_channels/create', data);
    },
    update(context, data){
        return Api().post('/api/event/'+data.event_id+'/sales_channels/'+data.saleschannel_id+'/update', data);
    },
    delete(context, data){
        return Api().post('/api/event/'+data.event_id+'/sales_channels/'+data.saleschannel_id+'/delete', data);
    }
}
const mutations = {}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}