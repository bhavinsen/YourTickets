import Api from './../../service/Api.js'

const state = () => ({


})

const getters = {



}

// Instead of mutating the state, actions commit mutations.
// Actions can contain arbitrary asynchronous operations.
// can have multiple commits
const actions = {

    getGenderChart:(_, data) => {
        return Api().get('/api/stats/get_gender_chart/'+data.start_date+'/'+data.end_date)
    },
    getTop5Chart:(_, data) =>{
        return Api().get('/api/stats/get_top_5_chart/'+data.chart_type+'/'+data.start_date+'/'+data.end_date)
    },
    getall: () =>{
        return Api().get('/multiticketshop/getall');
    },
    getEarnings:(_, data) => {
        return Api().get('/api/stats/get_earnings_chart/'+data.chart_type+'/'+data.start_date+'/'+data.end_date)
    },
    getTicketsCount:(_, data) => {
        return Api().get('/api/stats/get_ticketscount/'+data.start_date+'/'+data.end_date)
    },
    getNewReturningVisitors: (_, data) => {
        return Api().get('/api/stats/new_vs_returning_visitors/'+data.start_date+'/'+data.end_date);
    },
    listResidence(context, data){

        return Api().get('/api/stats/list_residence/'+ data.start_date+'/'+data.end_date);
    },
    getAgeGender(context, data){

        return Api().get('/api/stats/age_gender/'+ data.start_date+'/'+data.end_date);
    },


}

//must be sync
const mutations = {

}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}