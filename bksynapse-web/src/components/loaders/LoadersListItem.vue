<template>
  <div class="loaders-list-item">
    <v-card tile>
      <v-toolbar flat card dense>
        <v-toolbar-title>
          {{ loader.name }}
        </v-toolbar-title>
      </v-toolbar>

      <v-card-actions>
        <span class="small-text">{{ 'Created at ' + loader.createdAt }}</span>
        <v-spacer></v-spacer>
        <v-btn flat color="error" @click="removeDialog.show = true">
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-dialog v-model="removeDialog.show"
      width="400">
      <v-card>
        <v-card-title class="headline">
          Delete data loader
        </v-card-title>
        <v-card-text>
          Are you sure you wish to delete this data loader ?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="removeLoader">
            Yes 
          </v-btn>
          <v-btn flat @click="removeDialog.show = false">
            No
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import {sprintf} from 'sprintf-js'

export default {
  name: 'LoadersListItem',
  props: {
    loader: Object,
    onRemoved: Function
  },
  data() {
    return {
      removeDialog: {
        show: false
      },
    }
  },
  computed: {
    
  },
  methods: {
    removeLoader() {
      this.removeDialog.show = false
      if (this.onRemoved) this.onRemoved(this.loader)
    }
  }
}
</script>

<style>

</style>
