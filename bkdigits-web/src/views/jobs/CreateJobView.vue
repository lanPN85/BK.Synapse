<template>
  <div class="create-job-view">
    <app-header></app-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex xs12>
            <create-job></create-job>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import CreateJob from '@/components/jobs/CreateJob'

export default {
  name: 'CreateJobView',
  components: {
    AppHeader, CreateJob
  }
}
</script>
