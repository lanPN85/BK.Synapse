<template>
  <div class="datasets-list">
    <v-container grid-list-lg>
      <div v-for="dataset in datasets" :key="dataset.name">
        <datasets-list-item :dataset="dataset" :onRemoved="removeDataset"></datasets-list-item>
      </div>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import DatasetsListItem from '@/components/datasets/DatasetsListItem'

export default {
  name: 'DatasetsList',
  components: {
    DatasetsListItem
  },
  props: {
    datasets: Array
  },
  methods: {
    removeDataset(dataset) {
      var component = this
      for (var i=0; i<this.datasets.length; i++) {
        if (dataset.id == this.datasets[i].id) {
          component.requestRemove(dataset).then(() => {
            component.datasets.splice(i, 1)
          }).catch(error => {
            component.$store.commit('showError', 'An error occurred. The dataset may not have been deleted.')
          })
          break
        }
      }
    },
    requestRemove(dataset) {
      var url = process.env.VUE_APP_APIURL + 'datasets/delete'
      return axios.post(url, {
        dataset: {
          name: dataset.name
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
