<template>
  <div class="models-list-item">
    <v-card tile>
      <v-toolbar flat card dense>
        <v-toolbar-side-icon>
          <v-img :src="backendImage"></v-img>
        </v-toolbar-side-icon>
        <v-toolbar-title>
          {{ model.name }}
        </v-toolbar-title>
      </v-toolbar>

      <v-card-actions>
        <span class="small-text">{{ 'Created at ' + model.dateCreated }}</span>
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
          Delete model
        </v-card-title>
        <v-card-text>
          Are you sure you wish to delete this model ?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="removeModel">
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
  name: 'ModelsListItem',
  props: {
    model: Object,
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
    backendImage() {
      switch (this.model.backend) {
        case 'pytorch':
          return require('@/assets/pytorch-logo.png')
      }
    }
  },
  methods: {
    removeModel() {
      this.removeDialog.show = false
      if (this.onRemoved) this.onRemoved(this.model)
    }
  }
}
</script>

<style>

</style>
