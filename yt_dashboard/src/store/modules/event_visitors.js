import Api from '@/service/Api.js'

const state = () => ({
    event_tickets:[]
})

const getters = {
    getEventTickets: state => state.event_tickets
}

const actions = {
    loadEventTickets(context, id){

        return Api().get('/api/event/'+id+'/visitors/get_event_tickets').then(response => {
            context.commit('setEventTickets', response.data)
            return response
        });
    },
    getVisitorsForTicket(context, data){
        return Api().get('/api/event/'+data.id+'/visitors/visitors_for_ticket/'+data.ticket_id).then(response => {
            // context.commit('setEventTickets', response.data)
            return response
        });
    },

    // not yet used
    // upload_guestlist(context, data) {
    //     return Api().post('/api/event/'+data.event_id+'/visitors/upload', data.guestlist, {
    //         headers: {
    //             'Content-Type': 'multipart/form-data'
    //         }
    //     });
    // },
    // send_guestlist(context, data){
    //     return Api().post('/api/event/'+data.event_id+'/visitors/send', data);
    // },
    sendSingleTicket(context, data){
        return Api().post('/api/event/'+data.event_id+'/visitors/send_single_ticket', data);
    },
    deleteGuestlistTicket(context, data){
        return Api().post('/api/event/'+data.event_id+'/visitors/deleteticket', data);
        // call context.commit change total amount
    }
}
const mutations = {
    setEventTickets(state, eventTickets){
        state.event_tickets = eventTickets;
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}