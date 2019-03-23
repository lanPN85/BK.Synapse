import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    error: {
      message: '',
      show: false
    }
  },
  mutations: {
    showError(state, message) {
      state.error.message = message
      state.error.show = true
    }
  },
  actions: {

  }
})
