<template>
  <div class="job-summary-panel">
    <v-card>
      <v-card-title>
        <div class="headline">
          Summary
        </div>
      </v-card-title>

      <v-card-actions v-if="this.loading">
        <v-spacer></v-spacer>
        <v-progress-circular indeterminate
          color="primary"></v-progress-circular>
        <v-spacer></v-spacer>
      </v-card-actions>

      <v-card-text>
        <v-layout row wrap>
          <v-flex v-for="item in summaryList" 
            :key="item.name" xs6 md4>
            <b>{{ item.name }}: </b>
            <span>{{ item.value }}</span>
          </v-flex>
        </v-layout>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import {sprintf} from 'sprintf-js'
import axios from 'axios'

export default {
  name: 'JobSummaryPanel',
  props: {
    jobId: String
  },
  data() {
    return {
      loading: false,
      summary: null
    }
  },
  computed: {
    summaryList() {
      if (!this.summary) return []
      return [
        {
          name: 'State', value: this.summary.state
        },
        {
          name: 'Time elapsed', value: this.timeElapsed
        },
        {
          name: 'Epochs finished', value: this.summary.finishedEpochs
        }
      ]
    },
    timeElapsed() {
      if (!this.summary || !this.summary.elapsedSecs) return 'N/A'
      var hours = Math.floor(this.summary.elapsedSecs / 3600.0)
      var remain = this.summary.elapsedSecs - hours * 3600
      var mins = Math.floor(remain / 60.0)
      var secs = remain - mins * 60
      return sprintf('%02d:%02d:%02d', hours, mins, secs)
    }
  },
  methods: {
    fetchSummary() {
      var component = this
      var url = process.env.VUE_APP_APIURL + 'jobs/summary?id=' + this.jobId

      this.loading = true
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var summary = response.data.summary
        component.summary = summary
      }).catch(error => {
        console.error(error)
      }).then(() => {
        component.loading = false
      })
    }
  },
  mounted() {
    this.fetchSummary()
  }
}
</script>

<style>

</style>
