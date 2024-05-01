// this.$store.dispatch('messages/add', {'text':'yay'})

const state = () => ({
    messages:[]
})

const getters = {

}

const actions = {
    add(context, message){
        context.commit('add', message)
    },
    remove(context, message){
        context.commit('remove', message)
    }
}

// store.commit('increment', {
//     message:'yay',
//         type:'something'
// })
const mutations = {
    add (state, message) {
        state.messages.push(message)
    },
    remove(state, message){
        state.messages.splice(state.messages.indexOf(message), 1)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}