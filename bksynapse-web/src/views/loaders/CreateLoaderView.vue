<template>
  <div class="create-loader-view">
    <app-header></app-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex xs12>
            <create-loader></create-loader>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import CreateLoader from '@/components/loaders/CreateLoader'

export default {
  name: 'CreateLoaderView',
  components: {
    AppHeader, CreateLoader
  }
}
</script>
