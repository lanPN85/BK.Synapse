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
  }
}
</script>

<style>

</style>
