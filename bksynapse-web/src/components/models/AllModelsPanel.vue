<template>
  <div class="all-models-panel">
    <v-card>
      <v-card-title>
        <div>
          <span class="headline">
            All Models
          </span>
        </div>
      </v-card-title>

      <models-list v-if="models.list.length > 0" :models="models.list"></models-list>

      <v-card-text v-else class="text-xs-center">
        <h3 v-if="!models.loading">
          There are no models yet. <a href="/models/new">Create</a>
        </h3>
        <v-progress-circular indeterminate v-else
          large color="primary"></v-progress-circular>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import ModelsList from '@/components/models/ModelsList'

export default {
  name: 'AllModelsPanel',
  components: {
    ModelsList
  },
  data() {
    return {
      models: {
        list: [],
        loading: false
      }
    }
  },
  mounted() {
    this.fetchModels()
  },
  methods: {
    fetchModels() {
      var url = process.env.VUE_APP_APIURL + 'models/list'
      var component = this

      this.models.loading = true
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var models = response.data.models
        component.models.list = models
      }).catch(error => {
        console.error(error)
      }).then(() => {
        component.models.loading = false
      })
    }
  }
}
</script>

<style>

</style>
