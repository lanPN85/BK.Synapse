<template>
  <div class="action-list">
    <v-list expand>
      <v-list-group prepend-icon="mdi-database" 
        active-class="datasets--text">
        <template v-slot:activator>
          <v-list-tile >
            <v-list-tile-title>Datasets</v-list-tile-title>
          </v-list-tile>
        </template>
        <v-list-tile to="/datasets/new" ripple>
          <v-list-tile-title>Create</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-plus</v-icon></v-list-tile-action>
        </v-list-tile>
        <v-list-tile to="/datasets/edit" ripple>
          <v-list-tile-title>Manage</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-pencil</v-icon></v-list-tile-action>
        </v-list-tile>
      </v-list-group>

      <v-list-group prepend-icon="mdi-database-export"
        active-class="dataloaders--text">
        <template v-slot:activator>
          <v-list-tile >
            <v-list-tile-title>Data Loaders</v-list-tile-title>
          </v-list-tile>
        </template>
        <v-list-tile to="/loaders/new" ripple>
          <v-list-tile-title>Create</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-plus</v-icon></v-list-tile-action>
        </v-list-tile>
        <v-list-tile to="/loaders/edit" ripple>
          <v-list-tile-title>Manage</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-pencil</v-icon></v-list-tile-action>
        </v-list-tile>
      </v-list-group>

      <v-list-group prepend-icon="mdi-matrix"
        active-class="models--text">
        <template v-slot:activator>
          <v-list-tile >
            <v-list-tile-title>Models</v-list-tile-title>
          </v-list-tile>
        </template>
        <v-list-tile to="/models/new" ripple>
          <v-list-tile-title>Create</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-plus</v-icon></v-list-tile-action>
        </v-list-tile>
        <v-list-tile to="/models/edit" ripple>
          <v-list-tile-title>Manage</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-pencil</v-icon></v-list-tile-action>
        </v-list-tile>
      </v-list-group>

      <v-list-group prepend-icon="mdi-format-list-checks"
        active-class="jobs--text">
        <template v-slot:activator>
          <v-list-tile >
            <v-list-tile-title>Jobs</v-list-tile-title>
          </v-list-tile>
        </template>
        <v-list-tile to="/jobs/new" ripple>
          <v-list-tile-title>Create</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-plus</v-icon></v-list-tile-action>
        </v-list-tile>
        <v-list-tile to="/jobs/edit" ripple>
          <v-list-tile-title>Manage</v-list-tile-title>
          <v-list-tile-action><v-icon>mdi-pencil</v-icon></v-list-tile-action>
        </v-list-tile>
      </v-list-group>

      <v-divider></v-divider>

      <v-list-tile avatar ripple>
        <v-list-tile-avatar><v-icon></v-icon></v-list-tile-avatar>
        <v-list-tile-action>About</v-list-tile-action>
      </v-list-tile>
    </v-list>
  </div>
</template>

<script>
export default {
  name: 'ActionList',
  data() {
    return {

    }
  }
}
</script>

<style>

</style>
