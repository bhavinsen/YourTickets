import Api from '@/service/Api.js'

const state = () => ({
    items:false, //[]
    item:false //{}
})

const getters = {
    getItems: () => {
        return Api().get('/account/getall');
    }
}

const actions = {
    update(context, data) {
        return Api().post('/account/update', data);
    },
    login(context, data) {
        return Api().post('api-token-auth', data);
    },
    test(context, data) {
        return Api().post('/account/test', data);
    },
}
const mutations = {

}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}