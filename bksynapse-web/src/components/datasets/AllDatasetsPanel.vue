<template>
  <div class="all-datasets-panel">
    <v-card>
      <v-card-title>
        <div>
          <span class="headline">
            All Datasets
          </span>
        </div>
      </v-card-title>

      <datasets-list v-if="datasets.list.length > 0" :datasets="datasets.list"></datasets-list>

      <v-card-text v-else class="text-xs-center">
        <h3 v-if="!datasets.loading">
          There are no datasets yet. <a href="/datasets/new">Create</a>
        </h3>
        <v-progress-circular indeterminate v-else
          large color="primary"></v-progress-circular>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import DatasetsList from '@/components/datasets/DatasetsList'

export default {
  name: 'AllDatasetsPanel',
  components: {
    DatasetsList
  },
  data() {
    return {
      datasets: {
        list: [],
        loading: false
      }
    }
  },
  mounted() {
    this.fetchDatasets()
  },
  methods: {
    fetchDatasets() {
      var url = process.env.VUE_APP_APIURL + 'datasets/list'
      var component = this

      this.datasets.loading = true
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var datasets = response.data.datasets
        component.datasets.list = datasets
      }).catch(error => {
        console.error(error)
      }).then(() => {
        component.datasets.loading = false
      })
    }
  }
}
</script>

<style>

</style>
