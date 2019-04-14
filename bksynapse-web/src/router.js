import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Tutorial from './views/Tutorial.vue'

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
      path: '/loaders/edit',
      name: 'manage-loader',
      component: () => import('./views/loaders/ManageLoadersView.vue') 
    },
    {
      path: '/datasets/new',
      name: 'create-dataset',
      component: () => import('./views/datasets/CreateDatasetView.vue') 
    },
    {
      path: '/datasets/edit',
      name: 'manage-datasets',
      component: () => import('./views/datasets/ManageDatasetsView.vue') 
    },
    {
      path: '/jobs/new',
      name: 'create-jobs',
      component: () => import('./views/jobs/CreateJobView.vue') 
    },
    {
      path: '/jobs/edit',
      name: 'manage-jobs',
      component: () => import('./views/jobs/ManageJobsView.vue') 
    },
    {
      path: '/jobs/analytics/:jobId',
      name: 'analytics-jobs',
      component: () => import('./views/jobs/JobAnalyticsView.vue')
    },
    {
      path: '/tutorials',
      name: 'tutorials',
      component: Tutorial
    },
    {
      path: '/tutorials/:groupId/:file',
      name: 'tutorial-view',
      component: () => import('./views/TutorialView.vue')
    },
    {
      path: '*',
      name: 'not-found',
      component: () => import('./views/Page404.vue')
    }
  ]
})
