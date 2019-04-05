<template>
  <div class="job-summary-panel">
    <v-card>
      <v-card-title>
        <div class="headline">
          Summary
        </div>
      </v-card-title>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'JobSummaryPanel',
  data() {
    return {
      loading: false,
      summary: null
    }
  },
  computed: {
    summaryList() {
      if (!summary) return []
      return [
        
      ]
    }
  }
}
</script>

<style>

</style>
