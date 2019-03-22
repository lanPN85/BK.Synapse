import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/models/new',
      name: 'create-model',
      component: () => import('./views/models/CreateModelView.vue')      
    },
    {
      path: '/models/edit',
      name: 'manage-model',
      component: () => import('./views/models/ManageModelsView.vue')      
    },
    {
      path: '/loaders/new',
      name: 'create-loader',
      component: () => import('./views/loaders/CreateLoaderView.vue') 
    },
    {
      path: '/datasets/new',
      name: 'create-dataset',
      component: () => import('./views/datasets/CreateDatasetView.vue') 
    },
    {
      path: '/jobs/new',
      name: 'create-jobs',
      component: () => import('./views/jobs/CreateJobView.vue') 
    },{
      path: '*',
      name: 'not-found',
      component: () => import('./views/Page404.vue')
    }
  ]
})
