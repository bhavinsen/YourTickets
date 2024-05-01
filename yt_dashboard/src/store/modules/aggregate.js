import Api from '@/service/Api.js'

const state = () => ({
    // for now dont save anything
    // cache will apply here like this:
    items: [
        // if per widget cache:
        // widget is an unique thing in the website
        // see my newly created mixin!! mixins/uuid.js
        //
        {
            widget:true, // (by default=false)
            cache_id:'UUID-1'
        },
        // not per widget but per parameters
        // if you have a chart same thing on the website but the widget can be changed to some other data.
        //
        // for instance:
        // earning chart change to ticket sold for instance, only difference is that the url get parameter,
        // (chart_type is different)
        // then we have to cache based on parameters because vuex doesnt cache getters with parameters.
        // GET_GET_GET_GET options as cache key. solved bang.
        // BUT we can only have an x amount of items in cache
        // so we need to max that (but at this moment caching EVERY param type combo is fine)
        //
        {
            widget:false, // (by default)
            cache_id: 'GET_GET_GET_GET',


        }
    ],

})

const getters = {

}

const actions = {
    // UPDATE_LINEUP(context, data) {
    //     return Api().post('/event/'+data.event.id+'/lineup/'+data.lineup.id+'/update', data.lineup);
    // },
    // CREATE_LINEUP(context, data) {
    //     return Api().post('/event/'+data.event.id+'/lineup/create', data.lineup);
    // },
    // DELETE_LINEUP(context, data){
    //     return Api().get('/event/'+data.event.id+'/lineup/'+data.lineup.id+'/delete', {});
    // }
    getSoldTicketAmount: (_, data) => {
        return Api().get('/api/stats/aggregate/sold_ticket_amount/'+data.start_date+'/'+data.end_date);
    },
    getRevenue: (_, data) => {
        return Api().get('/api/stats/aggregate/revenue/'+data.start_date+'/'+data.end_date);
    },
    getVisitors: (_, data) => {
        return Api().get('/api/stats/aggregate/visitors/'+data.start_date+'/'+data.end_date);
    },
    getConversionRate: (_, data) => {
        return Api().get('/api/stats/aggregate/conversion_rate/'+data.start_date+'/'+data.end_date);
    }
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