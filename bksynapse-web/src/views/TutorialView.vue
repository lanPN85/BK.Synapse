<template>
  <div>
    <tutorial-header></tutorial-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex lg8 xs12>
            <vue-markdown :source="content">
              
            </vue-markdown>    
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import axios from 'axios'
import TutorialHeader from '@/components/TutorialHeader'
import VueMarkdown from 'vue-markdown'

export default {
  name: 'Tutorial',
  components: {
    TutorialHeader, VueMarkdown
  },
  data() {
    return {
      content: ''
    }
  },
  mounted() {
    var mdPath = '/tutorials/' + this.$route.params.groupId + '/' + this.$route.params.file + '.md'
    var component = this

    axios.get(mdPath).then(response => {
      component.content = '\n' + response.data
    }).catch(error => {
      console.error(error)
    })
  }
}
</script>

<style>

</style>
