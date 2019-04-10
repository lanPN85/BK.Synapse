<template>
  <div class="jobs-list">
    <v-container grid-list-md>
      <v-layout row wrap>
        <v-flex xs12 v-for="job in jobs" :key="job.id">
          <jobs-list-item :job="job" :onRemoved="removeJob"></jobs-list-item>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import JobsListItem from '@/components/jobs/JobsListItem'

export default {
  name: 'JobsList',
  components: {
    JobsListItem
  },
  props: {
    jobs: Array
  },
  data() {
    return {

    }
  },
  methods: {
    removeJob(job) {
      var component = this
      for (var i=0; i<this.jobs.length; i++) {
        if (job.id == this.jobs[i].id) {
          component.requestRemove(job).then(() => {
            component.jobs.splice(i, 1)
          }).catch(error => {
            component.$store.commit('showError', 'An error occurred. The job may not have been deleted.')
          })
          break
        }
      }
    },
    requestRemove(job) {
      var url = process.env.VUE_APP_APIURL + 'jobs/delete/training'
      return axios.post(url, {
        job: {
          id: job.id
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
