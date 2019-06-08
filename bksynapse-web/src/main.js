import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
import 'typeface-exo'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
import '@mdi/font/css/materialdesignicons.css'
import './plugins/vuemarkdown'
import 'prismjs/themes/prism.css'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
