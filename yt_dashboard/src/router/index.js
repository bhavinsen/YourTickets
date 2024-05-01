import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import store from '@/store'

Vue.use(VueRouter)
  //https://router.vuejs.org/guide/advanced/lazy-loading.html#grouping-components-in-the-same-chunk
  // routes lazy loading maken
  const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" *//* webpackPrefetch: true */ '../views/Login.vue'),
  },
  {
    path: '/events',
    name: 'events',
    //alias:'/event/:id/edit',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "events" */ '../views/Events.vue'),

  },
  {
    path: '/event/:id',
    name: 'event_dashboard',
    component: () => import(/* webpackChunkName: "events" */ '../views/EventDashboard.vue'),
    meta:{
      isEventPage: true
    }
  },
  {
    path: '/multishop',
    name: 'multishop',
    component: () => import(/* webpackChunkName: "multishop" */ '../views/Multishop.vue')
  },
    {
    path: '/stats',
    name: 'stats',
    component: () => import(/* webpackChunkName: "account" */ '../views/Stats.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: '/dashboard2/',//process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {

  if(to.name === 'event_dashboard'){
    store.dispatch('layout/setEventPage', {
      eventPage: true,
      event_id: to.params.id
    })
  }else{
    store.dispatch('layout/setEventPage', {
      eventPage: false,
      event_id: ''
    })
  }
  if (to.name !== 'login' && !localStorage.t) {
    // if(process.env.VUE_APP_LOGIN_URL === 'js'){
      next({ name: 'login' })
    // }else{
    //   window.location = process.env.VUE_APP_LOGIN_URL
    // }

  }
  else next()
})

export default router
