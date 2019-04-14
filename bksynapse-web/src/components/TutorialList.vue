<template>
  <div class="tutorial-list">
    <v-list expand>
      <v-list-tile to="/" exact>
        <v-list-tile-avatar>
          <v-icon color="primary">mdi-home</v-icon>
        </v-list-tile-avatar>
        <v-list-tile-title>
          Home Page
        </v-list-tile-title>
      </v-list-tile>

      <v-list-group v-for="item in tutorials" :key="item.group">
        <template v-slot:activator>
          <v-list-tile>
            <v-list-tile-avatar>
              <img :src="item.logo">
            </v-list-tile-avatar>
            <v-list-tile-title>{{ item.name }}</v-list-tile-title>
          </v-list-tile>
        </template>

        <v-list-tile v-for="(lesson, index) in item.lessons" :key="lesson.link"
          ripple :to="'/tutorials/' + item.group + '/' + lesson.link">
          <v-list-tile-avatar>
            <h4>{{ index + 1 }}</h4>
          </v-list-tile-avatar>
          <v-list-tile-title>{{ lesson.name }}</v-list-tile-title>
        </v-list-tile>
      </v-list-group>
    </v-list>
  </div>
</template>

<script>
export default {
  name: 'TutorialList',
  data() {
    return {
      tutorials: [
        {
          group: 'pytorch',
          name: 'PyTorch',
          logo: require('@/assets/pytorch-logo.png'),
          lessons: [
            {
              name: 'Getting Started',
              link: 'getting-started'
            }
          ]
        }
      ]  
    }
  }
}
</script>

<style>

</style>
