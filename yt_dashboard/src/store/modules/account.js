import Api from '@/service/Api.js'

const state = () => ({

    account: {
        email:'',
        first_name: '',
        last_name: '',
        saldo: '',
        avatar: '',

        coc_number: '',
        tax_number: '',
        place: '',
        account_number: '',
        account_owner: '',

        postal_code:'',
        house_number: '',
        house_number_addition: '',
        company_name: '',
        big:''
    }

})

const getters = {
    getall: (state) => {
        return state.account
    }
}

const mutations = {
    setAccount (state, account){
        state.account = account
    }
}

const actions = {

    load(context){
        return Api().get('/account/getall')
        .then((response) => {
            context.commit('setAccount', response.data.account)
            return response.data.account
          })
    },
    request_payout(_, amount){
        return Api().post('/account/request_payout', {'amount': amount})
    },

    update2(context, account) {
        return Api().post('/account/update', account)
            .then((response) => {
                if(response.data.success){
                    let data = response.data.account;
                    data['saldo'] = context.state.account.saldo
                    context.commit('setAccount', data)
                }
                return response.data
            })
    },
    change_password(context, data) {
        return Api().post('/account/change_password', data)
    },
    update(context, data) {
        return Api().post('/account/update', data);
    },
    login(context, data) {
        return Api().post('api-token-auth', data);
    },
    logout() {
        return Api().get('account/logout');
    },
    test(context, data) {
        return Api().post('/account/test', data);
    },
    create(context, data) {
        return Api().get('/account/create', data,{
          headers: {
            "Content-Type": "multipart/form-data"
        }});
    }
}


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}