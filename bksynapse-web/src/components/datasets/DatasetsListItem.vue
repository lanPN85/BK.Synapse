<template>
  <div class="datasets-list-item">
    <v-card tile>
      <v-toolbar flat card dense>
        <v-toolbar-title>
          {{ dataset.name }}
        </v-toolbar-title>
      </v-toolbar>

      <v-card-text>
        {{ 'Size: ' + datasetSize }}
      </v-card-text>

      <v-card-actions>
        <span class="small-text">{{ 'Created at ' + dataset.createdAt }}</span>
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
          Delete dataset
        </v-card-title>
        <v-card-text>
          Are you sure you wish to delete this dataset ?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="removeDataset">
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
  name: 'DatasetsListItem',
  props: {
    dataset: Object,
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
    datasetSize() {
      const units = ['B', 'KB', 'MB', 'GB']
      var val = this.dataset.totalBytes
      for (var i=0; i<units.length; i++) {
        if (val < 1024 || i == units.length - 1) {
          return sprintf('%.2f%s', val, units[i])
        }
        val /= 1024
      }
    }
  },
  methods: {
    removeDataset() {
      this.removeDialog.show = false
      if (this.onRemoved) this.onRemoved(this.dataset)
    }
  }
}
</script>

<style>

</style>
