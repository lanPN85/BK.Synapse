<template>
  <div class="app-header">
    <v-toolbar color="primary" dark app clipped-left flat>
      <v-toolbar-side-icon @click="drawer.show = !drawer.show"
        class="hidden-md-and-up">
        <v-icon>mdi-menu</v-icon>
      </v-toolbar-side-icon>
      <v-toolbar-title>
				<a href="/" class="title-text">BK.SYNAPSE</a>
			</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-toolbar-items>
        <v-btn flat :loading="nodes.loading"
          @click="nodesDialog.show = true">
          {{ nodes.list.length.toString() + ' node(s), ' + activeNodesCount.toString() + ' active' }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-navigation-drawer v-model="drawer.show" 
      app clipped>
      <action-list></action-list>
    </v-navigation-drawer>

    <v-dialog v-model="nodesDialog.show"
      max-width="1024">
      <nodes-panel :nodes="nodes.list"></nodes-panel>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import ActionList from '@/components/ActionList'
import NodesPanel from '@/components/NodesPanel'

export default {
  name: 'AppHeader',
  components: {
    ActionList, NodesPanel
  },
  data() {
    return {
      drawer: {
        show: false
      },
      nodes: {
        list: [],
        loading: false
      },
      nodesDialog: {
        show: false
      }
    }
  },
  mounted() {
    // Show drawer on large screens
    switch (this.$vuetify.breakpoint.name) {
      case 'lg':
      case 'xl':
        this.drawer.show = true
        break
    }

    this.fetchNodes()
  },
  methods: {
    fetchNodes() {
      var component = this
      var url = process.env.VUE_APP_APIURL + 'nodes/list'

      this.nodes.loading = true
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var nodes = response.data.nodes
        component.nodes.list = nodes
      }).catch(error => {
        console.error(error)
      }).then(() => {
        component.nodes.loading = false
      })
    }
  },
  computed: {
    activeNodesCount() {
      var count = 0
      for (var i=0; i<this.nodes.list.length; i++) {
        var n = this.nodes.list[i]
        if (n.isActive) {
          count += 1
        }
      }
      return count
    }
  }
}
</script>

<style scoped>
.title-text {
  font-family: 'Exo', 'Arial', sans-serif;
  font-size: larger;
  font-weight: bold;
  color: white;
  text-decoration: none;
}
</style>
