<template>
  <div>
    <tutorial-header></tutorial-header>
    <v-content>
      <v-container fluid grid-list-xl>
        <v-layout row wrap>
          <v-flex lg8 xs12 offset-lg2>
            <v-card>
              <v-card-text>
                <vue-markdown :source="content">
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
import axios from 'axios'
import TutorialHeader from '@/components/TutorialHeader'
import VueMarkdown from 'vue-markdown'
import Prism from 'prismjs'
import loadLanguages from 'prismjs/components'

export default {
  name: 'Tutorial',
  components: {
    TutorialHeader, VueMarkdown
  },
  mounted() {
    loadLanguages(['python'])
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
      var codeList = document.getElementsByClassName('language-py')
      for (var i=0; i<codeList.length; i++) {
        var block = codeList[i]
        Prism.highlightElement(block)
      }
      Prism.highlightAll()
    }).catch(error => {
      console.error(error)
    })
  }
}
</script>

<style>
[class*=language-] {
  display: block;
  border: none;
}
</style>
