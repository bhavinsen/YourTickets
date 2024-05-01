import Api from '@/service/Api.js'

const state = () => ({
    statistics:{}
})

function createDateString(start_date, end_date){
    let dateString = '';
    if(start_date && end_date){
        dateString = '/'+start_date+'/'+end_date
    }
    return dateString
}

const getters = {
    // statistics: () => (id) => {
    //     return Api().get('/event/'+id+'/statistics');
    // },
    // sales_chart: () => (id) => {
    //     return Api().get('/event/'+id+'/statistics/sales_data');
    // },
    getSoldTicketAmount: () => (id, start_date, end_date) => {

        return Api().get('/api/event/'+id+'/stats/sold_ticket_amount' + createDateString(start_date, end_date));
    },
    getRevenue: () => (id, start_date, end_date) => {

        return Api().get('/api/event/'+id+'/stats/revenue' + createDateString(start_date, end_date));
    },
    getVisitors: () => (id, start_date, end_date) => {

        return Api().get('/api/event/'+id+'/stats/visitors' + createDateString(start_date, end_date));
    },
    getConversionRate: () => (id, start_date, end_date) => {

        return Api().get('/api/event/'+id+'/stats/conversion_rate' + createDateString(start_date, end_date));
    },
    getGenderChart: () => (id, start_date, end_date) => {
        return Api().get('/api/event/'+id+'/stats/gender_chart' + createDateString(start_date, end_date));
    },
    getTicketsCount: () => (id, start_date, end_date) => {
        return Api().get('/api/event/'+id+'/stats/ticketscount' + createDateString(start_date, end_date));
    },
    getAgeAndGender: () => (id, start_date, end_date) => {
        return Api().get('/api/event/'+id+'/stats/age_and_gender' + createDateString(start_date, end_date));
    },
    getEarnings: () => (id, start_date, end_date) => {

        return Api().get('/api/event/'+id+'/stats/get_earnings_chart' + createDateString(start_date, end_date));
    },
    // listResidence: () => (id, start_date, end_date) => {
    //     return Api().get('/api/event/'+id+'/stats/list_residence'+ createDateString(start_date, end_date));
    // },
    getTotalSoldOf: () => (id, start_date, end_date) => {
        return Api().get('/api/event/'+id+'/stats/total_sold_of'+ createDateString(start_date, end_date));
    },
    getNewReturningVisitors: () => (id, start_date, end_date) => {
        return Api().get('/api/event/'+id+'/stats/new_vs_returning_visitors'+ createDateString(start_date, end_date));
    },

}

const actions = {
    listResidence(context, data){

        return Api().get('/api/event/'+data.event_id+'/stats/list_residence'+ createDateString(data.start_date, data.end_date));
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