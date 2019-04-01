<template>
  <div class="create-model-view">
    <app-header></app-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex xs12>
            <create-model></create-model>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader'
import CreateModel from '@/components/models/CreateModel'

export default {
  name: 'CreateModelView',
  components: {
    AppHeader, CreateModel
  }
}
</script>
