import Vue from 'vue'
import Vuex from 'vuex'

import layout from './modules/layout'
import event from './modules/event'
import aggregate from './modules/aggregate'

import event_statistics from "@/store/modules/event_statistics";
import event_visitors from "@/store/modules/event_visitors";
import event_saleschannels from "@/store/modules/event_saleschannels";
import multiticketshops from "@/store/modules/multiticketshops";
import account from "@/store/modules/account";
import messages from "./modules/messages";
import stats from "@/store/modules/stats";
import { createStore } from 'vuex-extensions';
import createCache from 'vuex-cache';

Vue.use(Vuex)

export default createStore(Vuex.Store, {
  plugins: [createCache()],
  state: {

  },
  mutations: {
  },
  actions: {
  },
  getters: {

  },
  modules: {
    layout: layout,
    event: event,
    event_statistics: event_statistics,
    event_visitors: event_visitors,
    event_saleschannels: event_saleschannels,
    multiticketshops: multiticketshops,
    account: account,
    messages: messages,
    aggregate: aggregate,
    stats: stats
  },
  // mixins: {
  //   mutations: {
  //     changeState: function (state, changed) {
  //       console.log('state', state, changed)
  //     }
  //   },
  //   getters: {
  //     cache(){
  //       console.log('cache')
  //     }
  //   },
  //   actions: {
  //
  //   }
  // }
})
