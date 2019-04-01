<template>
  <div id="app">
    <v-app>
      <router-view/>
      <v-snackbar bottom absolute
        :timeout="5000"
        v-model="error.show"
        color="error">
        <v-spacer></v-spacer>
        <span>{{ error.message }}</span>
        <v-spacer></v-spacer>
      </v-snackbar>
    </v-app>
  </div>
</template>

<script>
export default {
  computed: {
    error() {
      return this.$store.state.error
    }
  }
}
</script>


<style>
#app {
  font-family: 'Roboto', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.header-text {
  font-weight: bold;
}
</style>
