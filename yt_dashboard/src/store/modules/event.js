import Api from './../../service/Api.js'
// import { cacheAction } from 'vuex-cache';

const state = () => ({
    event:{
        title:'',
        location:'',
        description:'',
        start_date:'',
        event_public:'',
        can_be_published:{
            status:'',
            tab:'',
        },

    },
    //cached events
    events:[],

    test:'default value'

})

const getters = {
    getEventApi: () => (id) => {
        return Api().get('/api/event/get/'+id);
    },
    getEvent: state => state.event,
    // getEventTickets: () => (id) => {
    //     return Api().get('/event/geteventtickets/'+id);
    // },
    // getEvents: state => { return state.events },
    // getEventsStats: () => (stat_type) =>{
    //     return Api().get('/event/statsall/'+stat_type)
    // },
    // check_publish: () => (id) => {
    //     return Api().get('/event/'+id+'/check_publish');
    // }
    getEvents: state => state.events,
    getTest: state => state.test
}

const actions = {
    loadEvents(context){

        return Api().get('/api/event/getall').then(response => {
            context.commit('SET_EVENTS', response.data)
            return response
        });
    },
    loadEvent(context, id){
        return Api().get('/api/event/get/'+id).then(response => {
            context.commit('setEvent', response.data)
            return response
        })
    },
    getFilteredEvents(context, filter){
        return  Api().get('/api/event/search/'+filter);
    },
    // UPDATE_EVENT(context, event) {
    //     return  Api().post('/event/'+event.id+'/update',event);
    // },
    createEvent: (context, event) => {
        return Api().post('/api/event/create', event, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(response => {
            // context.cache.delete('event/loadEvents')
            // context.dispatch('loadEvents')
            context.commit('CREATE_EVENT', response.data.event)
            return response.data
        });
        // return context.commit("createEvent", event);
        // return Api().post('/event/create', {'title':event.title});
    },
    publish(context, id){
        return Api().post('/api/event/'+id+'/publish' ).then((response)=>{
            context.commit('setEventPublic', true)
            return response;
        })
    },
    unpublish(context, id){
        return Api().post('/api/event/'+id+'/unpublish' ).then((response)=>{
            context.commit('setEventPublic', false)
            return response;
        })
    },
    delete(context, id){

        return Api().post('/api/event/delete/'+id).then((response)=>{
            //remove event from list
            context.commit('deleteEvent', id)
            return response;
        })
    },
    setEvent(context, data){
        context.commit('setEvent', data)
    },
    setTest(context, value){
        context.commit('setTest', value)
    },
    loadTest(context){
        return Api().get('/api/event/getall').then(response => {
            context.commit('setTest', 'ajax value')
            return response
        });
    }
}

//must be sync
const mutations = {
    setTest(state, value){
        console.log('SET test state')
        state.test  = value
    },
    setEvent(state, data){
        state.event = data.event
    },
    setEventPublic(state, data){
       state.event.event_public = data
    },
    deleteEvent(state, event_id){

        const indexOfObject = state.events.findIndex(object => {
          return object.pk === event_id;
        });

        state.events.splice(indexOfObject, 1);
    },
    SET_EVENTS(state, events){
        state.events = events;
    },
    CREATE_EVENT (state, event){
        // console.log(event)

        const indexOfObject = state.events.findIndex(object => {
          return object.pk === event.id;
        });

        if(indexOfObject !== -1){
            state.event = event
        }


        // return  Api().post('/event/create',{'title':event.title});
    },
    updateEvent (state, event){
        // not used
        return  Api().post('/event/update',{'title':event.title});
        //ajax update call
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}