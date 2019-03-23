<template>
  <div class="home">
    <app-header></app-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex xs12>
            <active-jobs-panel></active-jobs-panel>
          </v-flex>
          <v-flex xs12>
            <create-panel></create-panel>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import ActionList from '@/components/ActionList'
import CreatePanel from '@/components/CreatePanel'
import ActiveJobsPanel from '@/components/jobs/ActiveJobsPanel'

export default {
  name: 'Home',
  components: {
    AppHeader, ActionList, CreatePanel, ActiveJobsPanel
  }
}
</script>
