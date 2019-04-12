<template>
  <div class="action-list">
    <v-list expand>
      <v-list-group prepend-icon="mdi-database" 
        active-class="datasets--text"
        :value="matchedSection('datasets')">
        <template v-slot:activator>
          <v-list-tile >
            <v-list-tile-title>Datasets</v-list-tile-title>
          </v-list-tile>
        </template>
        <v-list-tile to="/datasets/new" ripple active-class="datasets--text">
          <v-list-tile-title>Create</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-plus</v-icon></v-list-tile-action>
        </v-list-tile>
        <v-list-tile to="/datasets/edit" ripple active-class="datasets--text">
          <v-list-tile-title>Manage</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-pencil</v-icon></v-list-tile-action>
        </v-list-tile>
      </v-list-group>

      <v-list-group prepend-icon="mdi-database-export"
        active-class="dataloaders--text"
        :value="matchedSection('loaders')">
        <template v-slot:activator>
          <v-list-tile >
            <v-list-tile-title>Data Loaders</v-list-tile-title>
          </v-list-tile>
        </template>
        <v-list-tile to="/loaders/new" ripple active-class="dataloaders--text">
          <v-list-tile-title>Create</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-plus</v-icon></v-list-tile-action>
        </v-list-tile>
        <v-list-tile to="/loaders/edit" ripple active-class="dataloaders--text">
          <v-list-tile-title>Manage</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-pencil</v-icon></v-list-tile-action>
        </v-list-tile>
      </v-list-group>

      <v-list-group prepend-icon="mdi-matrix"
        active-class="models--text"
        :value="matchedSection('models')">
        <template v-slot:activator>
          <v-list-tile >
            <v-list-tile-title>Models</v-list-tile-title>
          </v-list-tile>
        </template>
        <v-list-tile to="/models/new" ripple active-class="models--text">
          <v-list-tile-title>Create</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-plus</v-icon></v-list-tile-action>
        </v-list-tile>
        <v-list-tile to="/models/edit" ripple active-class="models--text">
          <v-list-tile-title>Manage</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-pencil</v-icon></v-list-tile-action>
        </v-list-tile>
      </v-list-group>

      <v-list-group prepend-icon="mdi-format-list-checks"
        active-class="jobs--text"
        :value="matchedSection('jobs')">
        <template v-slot:activator>
          <v-list-tile >
            <v-list-tile-title>Jobs</v-list-tile-title>
          </v-list-tile>
        </template>
        <v-list-tile to="/jobs/new" ripple active-class="jobs--text">
          <v-list-tile-title>Create</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-plus</v-icon></v-list-tile-action>
        </v-list-tile>
        <v-list-tile to="/jobs/edit" ripple active-class="jobs--text">
          <v-list-tile-title>Manage</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-pencil</v-icon></v-list-tile-action>
        </v-list-tile>
      </v-list-group>

      <v-divider></v-divider>

      
    </v-list>
  </div>
</template>

<script>
export default {
  name: 'ActionList',
  data() {
    return {

    }
  },
  methods: {
    matchedSection(name) {
      var url = window.location.pathname
      var parts = url.split('/')
      return parts.indexOf(name) != -1
    }
  }
}
</script>

<style>

</style>
