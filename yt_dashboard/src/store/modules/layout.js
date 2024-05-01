const state = () => ({
  navopen:false,
  navismini:false,
  eventPage:false,
  event_id:0,
  // event:{},
  startDate:'',
  endDate:''
})

const actions = {
  setStartDate ({commit}, startDate){
    commit('setStartDate', startDate)
  },
  setEndDate ({commit}, endDate){
    commit('setEndDate', endDate)
  },
  setEventPage({commit}, data){
    commit('setEventPage', data)
  }
}

const getters = {
  getEventPage: state => {
    return state.eventPage;
  },
  getEventId: state => {
    return state.event_id;
  },
  getStartDate: state => {
    return state.startDate;
  },
  getEndDate: state => {
    return state.endDate;
  },
}

const mutations = {
  navopen (state, navstate){
    state.navopen = navstate;
  },
  navismini (state, ministate){
    state.navismini = ministate;
  },
  setEventPage(state, data){
    state.eventPage = data.eventPage;
    state.event_id = data.event_id;
  },
  setStartDate(state, startDate){
    state.startDate = startDate;
  },
  setEndDate(state, endDate){
    state.endDate = endDate;
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
