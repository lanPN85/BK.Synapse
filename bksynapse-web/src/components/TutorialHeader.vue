<template>
  <div class="app-header">
    <v-toolbar color="#f57f17" dark app clipped-left flat>
      <v-toolbar-side-icon @click="drawer.show = !drawer.show"
        class="hidden-md-and-up">
        <v-icon>mdi-menu</v-icon>
      </v-toolbar-side-icon>
      <v-toolbar-title>
				<a href="/tutorials" class="title-text">BK.SYNAPSE Docs</a>
			</v-toolbar-title>
    </v-toolbar>

    <v-navigation-drawer v-model="drawer.show" 
      app clipped>
      <tutorial-list></tutorial-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import TutorialList from '@/components/TutorialList'

export default {
  name: 'TutorialHeader',
  components: {
    TutorialList
  },
  data() {
    return {
      drawer: {
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
  },
  methods: {

  },
  computed: {
    
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
