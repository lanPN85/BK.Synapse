<template>
  <div class="nodes-panel">
    <v-card>
      <v-card-title>
        <div class="headline">Nodes</div>
      </v-card-title>

      <v-card-actions>
        <v-container grid-list-md>
          <v-layout row wrap>
            <v-flex v-for="item in nodes" :key="item.id">
              <nodes-list-item :node="item"></nodes-list-item>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import NodesListItem from '@/components/nodes/NodesListItem'

export default {
  name: 'NodesPanel',
  components: {
    NodesListItem
  },
  props: {
    nodes: Array
  },
  data() {
    return {
      
    }
  }
}
</script>

<style>

</style>
