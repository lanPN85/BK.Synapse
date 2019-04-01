<template>
  <div class="manage-model-view">
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
  name: 'ManageModelsView',
  components: {
    AppHeader
  }
}
</script>
