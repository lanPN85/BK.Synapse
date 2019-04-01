<template>
  <div class="manage-jobs">
    <all-jobs-panel></all-jobs-panel>
  </div>
</template>

<script>
import AllJobsPanel from '@/components/jobs/AllJobsPanel'

export default {
  name: 'ManageJobs',
  components: {
    AllJobsPanel
  },
  data() {
    return {

    }
  }
}
</script>

<style>

</style>
