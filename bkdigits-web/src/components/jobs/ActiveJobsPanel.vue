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

      <v-list v-if="activeJobs.list.length > 0">

      </v-list>

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
export default {
  name: 'ActiveJobsPanel',
  data() {
    return {
      activeJobs: {
        list: [],
        loading: false
      }
    }
  }
}
</script>

<style>

</style>
