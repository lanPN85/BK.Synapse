<template>
  <div class="jobs-list">
    <v-container grid-list-md>
      <div v-for="job in jobs" :key="job.id">
        <jobs-list-item :job="job"></jobs-list-item>
      </div>
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
          this.requestRemove(job).then(() => {
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
      axios.post(url, {
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
