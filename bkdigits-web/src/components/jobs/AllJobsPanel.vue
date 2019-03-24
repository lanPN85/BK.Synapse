<template>
  <div class="all-jobs-panel">
    <v-card>
      <v-card-title>
        <div>
          <span class="headline">
            All Jobs
          </span>
        </div>
      </v-card-title>

      <jobs-list v-if="jobs.list.length > 0" :jobs="jobs.list"></jobs-list>

      <v-card-text v-else class="text-xs-center">
        <h3 v-if="!jobs.loading">
          There are no jobs yet. <a href="/jobs/new">Create</a>
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
  name: 'AllJobsPanel',
  components: {
    JobsList
  },
  data() {
    return {
      jobs: {
        list: [],
        loading: false
      }
    }
  },
  mounted() {
    this.fetchJobs()
  },
  methods: {
    fetchJobs() {
      var url = process.env.VUE_APP_APIURL + 'jobs/list'
      var component = this

      this.jobs.loading = true
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var jobs = response.data.jobs
        component.jobs.list = jobs
      }).catch(error => {
        console.error(error)
      }).then(() => {
        component.jobs.loading = false
      })
    }
  }
}
</script>

<style>

</style>
