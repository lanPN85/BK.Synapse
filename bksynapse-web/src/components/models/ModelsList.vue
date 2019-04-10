<template>
  <div class="models-list">
    <v-container grid-list-lg>
      <div v-for="model in models" :key="model.name">
        <models-list-item :model="model" :onRemoved="removeModel"></models-list-item>
      </div>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import ModelsListItem from '@/components/models/ModelsListItem'

export default {
  name: 'ModelsListItem',
  components: {
    ModelsListItem
  },
  props: {
    models: Array
  },
  methods: {
    removeModel(model) {
      var component = this
      for (var i=0; i<this.models.length; i++) {
        if (model.id == this.models[i].id) {
          component.requestRemove(model).then(() => {
            component.models.splice(i, 1)
          }).catch(error => {
            component.$store.commit('showError', 'An error occurred. The model may not have been deleted.')
          })
          break
        }
      }
    },
    requestRemove(model) {
      var url = process.env.VUE_APP_APIURL + 'models/delete'
      return axios.post(url, {
        model: {
          name: model.name
        }
      }, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      })
    }
  }
}
</script>

<style>

</style>
