<template>
  <div class="page-404">
    <v-container fluid grid-list-lg>
      <v-layout>
        <v-flex xs12 md6 offset-md3>
          <v-card style="margin-top: 20%" 
            color="error" dark raised>
            <v-card-title>
              <div>
                <p class="headline"><b>Page Not Found</b></p>
                <p>The page you are looking for does not exist</p>
                <p><a href="/" style="color: white"><b>Back to homepage</b></a></p>
              </div>
            </v-card-title>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
    
  </div>
</template>

<script>
export default {
  name: 'Page404'
}
</script>

<style>

</style>
