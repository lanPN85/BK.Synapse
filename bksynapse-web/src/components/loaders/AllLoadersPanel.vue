<template>
  <div class="all-loaders-panel">
    <v-card>
      <v-card-title>
        <div>
          <span class="headline">
            All Data Loaders
          </span>
        </div>
      </v-card-title>

      <loaders-list v-if="loaders.list.length > 0" :loaders="loaders.list"></loaders-list>

      <v-card-text v-else class="text-xs-center">
        <h3 v-if="!loaders.loading">
          There are no data loaders yet. <a href="/loaders/new">Create</a>
        </h3>
        <v-progress-circular indeterminate v-else
          large color="primary"></v-progress-circular>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import LoadersList from '@/components/loaders/LoadersList'

export default {
  name: 'AllLoadersPanel',
  components: {
    LoadersList
  },
  data() {
    return {
      loaders: {
        list: [],
        loading: false
      }
    }
  },
  mounted() {
    this.fetchLoaders()
  },
  methods: {
    fetchLoaders() {
      var url = process.env.VUE_APP_APIURL + 'loaders/list'
      var component = this

      this.loaders.loading = true
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var loaders = response.data.loaders
        component.loaders.list = loaders
      }).catch(error => {
        console.error(error)
      }).then(() => {
        component.loaders.loading = false
      })
    }
  }
}
</script>

<style>

</style>
