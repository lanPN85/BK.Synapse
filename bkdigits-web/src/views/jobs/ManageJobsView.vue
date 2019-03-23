<template>
  <div class="manage-jobs-view">
    <app-header></app-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex xs12>
            
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'

export default {
  name: 'ManageJobsView',
  components: {
    AppHeader
  }
}
</script>
