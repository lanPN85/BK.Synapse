<template>
  <div class="datasets-list-item">
    <v-card tile>
      <v-toolbar flat card dense>
        <v-toolbar-title>
          {{ dataset.name }}
        </v-toolbar-title>
      </v-toolbar>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn flat color="error">
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'DatasetsListItem',
  props: {
    dataset: Object,
    onRemoved: Function
  }
}
</script>

<style>

</style>
