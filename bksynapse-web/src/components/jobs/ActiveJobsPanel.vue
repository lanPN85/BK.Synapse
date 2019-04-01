<template>
  <div class="active-jobs-panel">
    <v-card>
      <v-card-title>
        <div>
          <span class="headline">
            Active Jobs
          </span>
          <v-icon>mdi-console-line</v-icon>
        </div>
      </v-card-title>

      <jobs-list v-if="activeJobs.list.length > 0" :jobs="activeJobs.list"></jobs-list>
      
      <v-card-text v-else class="text-xs-center">
        <h3 v-if="!activeJobs.loading">
          There are no active jobs
        </h3>
        <v-progress-circular indeterminate v-else
          large color="primary"></v-progress-circular>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import JobsList from '@/components/jobs/JobsList'

export default {
  name: 'ActiveJobsPanel',
  components: {
    JobsList
  },
  data() {
    return {
      activeJobs: {
        list: [],
        loading: false
      }
    }
  },
  methods: {
    fetchActiveJobs() {
      var url = process.env.VUE_APP_APIURL + 'jobs/list?active_only=true'
      var component = this

      this.activeJobs.loading = true
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var activeJobs = response.data.jobs
        component.activeJobs.list = activeJobs
      }).catch(error => {
        console.error(error)
      }).then(() => {
        component.activeJobs.loading = false
      })
    }
  },
  mounted() {
    this.fetchActiveJobs()
  }
}
</script>

<style>

</style>
