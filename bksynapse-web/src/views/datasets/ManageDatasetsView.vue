<template>
  <div class="manage-datasets-view">
    <app-header></app-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex xs12>
            <all-datasets-panel></all-datasets-panel>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import AllDatasetsPanel from '@/components/datasets/AllDatasetsPanel'

export default {
  name: 'ManageDatasetsView',
  components: {
    AppHeader, AllDatasetsPanel
  }
}
</script>
