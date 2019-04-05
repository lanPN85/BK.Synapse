<template>
  <div class="job-analytics-view">
    <app-header></app-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex xs12>
            <h2>
              Job Analytics
              <span style="font-weight: 300">({{ $route.params.jobId }})</span>
            </h2>
          </v-flex>

          <v-flex xs12>
            <job-summary-panel></job-summary-panel>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import JobSummaryPanel from '@/components/jobs/JobSummaryPanel'

export default {
  name: 'JobAnalyticsView',
  components: {
    AppHeader, JobSummaryPanel
  },
  data() {
    return {
      
    }
  },
  methods: {

  }
}
</script>

<style>

</style>
