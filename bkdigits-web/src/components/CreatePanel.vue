<template>
  <div class="create-panel">
    <v-card>
      <v-card-title>
        <div>
          <span class="headline">
            New
          </span>
          <v-icon>mdi-plus</v-icon>
        </div>
      </v-card-title>

      <v-container grid-list-xl>
        <v-layout row wrap>
          <v-flex md3 xs6>
            <v-card ripple hover to="/datasets/new">
              <v-card-text class="text-xs-center">
                <p><v-icon size="60" color="datasets">mdi-database</v-icon></p>
                <p>Dataset</p>
              </v-card-text>
            </v-card>
          </v-flex>

          <v-flex md3 xs6>
            <v-card ripple hover to="/loaders/new">
              <v-card-text class="text-xs-center">
                <p><v-icon size="60" color="dataloaders">mdi-database-export</v-icon></p>
                <p>Data Loader</p>
              </v-card-text>
            </v-card>
          </v-flex>

          <v-flex md3 xs6>
            <v-card ripple hover to="/models/new">
              <v-card-text class="text-xs-center">
                <p><v-icon size="60" color="models">mdi-matrix</v-icon></p>
                <p>Model</p>
              </v-card-text>
            </v-card>
          </v-flex>

          <v-flex md3 xs6>
            <v-card ripple hover to="/jobs/new">
              <v-card-text class="text-xs-center">
                <p><v-icon size="60" color="jobs">mdi-format-list-checks</v-icon></p>
                <p>Job</p>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>
