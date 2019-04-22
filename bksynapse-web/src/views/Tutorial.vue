<template>
  <div>
    <tutorial-header></tutorial-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex lg8 xs12 offset-lg2>
            <v-card>
              <v-card-text>
                <vue-markdown>
                {{ content }}  
              </vue-markdown>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import TutorialHeader from '@/components/TutorialHeader'
import VueMarkdown from 'vue-markdown'

import content from 'raw-loader!@/assets/tutorials/home.md'

export default {
  name: 'Tutorial',
  components: {
    TutorialHeader, VueMarkdown
  },
  data() {
    return {
      content: '\n' + content
    }
  }
}
</script>

<style>

</style>
