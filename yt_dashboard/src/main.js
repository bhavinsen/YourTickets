import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import cookies from "./plugins/cookies";
import router from './router'
import store from '@/store'
import Panel from './components/core/panel.vue'
import i18n from './i18n'

// import VueGooglePlaces from 'vue-google-places'


Vue.config.productionTip = false
// global components
Vue.component('panel', Panel)

new Vue({
  vuetify,
  router,
  cookies,
  store,
  i18n,

  // VueGooglePlaces,
  render: h => h(App)
}).$mount('#app')
