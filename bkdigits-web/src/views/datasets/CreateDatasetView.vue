<template>
  <div class="create-dataset-view">
    <app-header></app-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex xs12>
            <create-dataset></create-dataset>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import CreateDataset from '@/components/datasets/CreateDataset'

export default {
  name: 'CreateDatasetView',
  components: {
    AppHeader, CreateDataset
  }
}
</script>
