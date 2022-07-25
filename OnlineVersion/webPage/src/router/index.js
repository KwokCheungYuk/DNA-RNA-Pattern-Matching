import Vue from 'vue'
import Router from 'vue-router'
import PatternMatching from '@/components/PatternMatching'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'PatternMatching',
      component: PatternMatching
    }
  ]
})
