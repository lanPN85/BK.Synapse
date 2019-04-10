<template>
  <div class="loaders-list">
    <v-container grid-list-lg>
      <div v-for="loader in loaders" :key="loader.name">
        <loaders-list-item :loader="loader" :onRemoved="removeLoader"></loaders-list-item>
      </div>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import LoadersListItem from '@/components/loaders/LoadersListItem'

export default {
  name: 'LoadersList',
  components: {
    LoadersListItem
  },
  props: {
    loaders: Array
  },
  methods: {
    removeLoader(loader) {
      var component = this
      for (var i=0; i<this.loaders.length; i++) {
        if (loader.id == this.loaders[i].id) {
          component.requestRemove(loader).then(() => {
            component.loaders.splice(i, 1)
          }).catch(error => {
            component.$store.commit('showError', 'An error occurred. The data loader may not have been deleted.')
          })
          break
        }
      }
    },
    requestRemove(loader) {
      var url = process.env.VUE_APP_APIURL + 'loaders/delete'
      return axios.post(url, {
        loader: {
          name: loader.name
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
