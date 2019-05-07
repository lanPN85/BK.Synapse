<template>
  <div class="create-model">
    <v-card>
      <v-card-title>
        <div>
          <p class="headline">Create new model</p>
        </div>
      </v-card-title>

      <v-card-text>
        <h3>Model info</h3>
        <form>
          <v-text-field v-model="modelMeta.name"
            label="Model name" autofocus
            messages="A name for the model, eg. ResNet50-PyTorch"
            color="info" box></v-text-field>
          <v-select v-model="modelMeta.backend"
            :items="backendChoices"
            label="Model backend" box color="info"
            messages="The model's framework backend"></v-select>
        </form>
      </v-card-text>

      <v-card-text>
        <h3>Model files</h3>
        <v-layout row wrap>
          <v-flex xs12>
            <p class="text-xs-left header-text">Model source code</p>
            <dropzone :options="srcFileDropOpts"
              id="src-dropzone" ref="srcDropzone"
              :useCustomSlot="true"
              v-on:vdropzone-file-added="droppedFiles+=1"
              v-on:vdropzone-removed-file="droppedFiles-=1"
              v-on:vdropzone-queue-complete="srcDzQueueComplete"
              v-on:vdropzone-max-files-exceeded="srcDzRemoveFile">
              <div>
                <h2 class="info--text">Drag file to upload</h2>
                <span>...or click to browse</span>
              </div>
            </dropzone>
          </v-flex>

          <v-flex xs12>
            <v-checkbox label="Upload model with weights"
              v-model="useWeights"
              color="warning"></v-checkbox>
            <dropzone :options="weightFileDropOpts"
              id="weights-dropzone" ref="weightsDropzone"
              :useCustomSlot="true"
              v-show="useWeights"
              v-on:vdropzone-queue-complete="weightDzQueueComplete"
              v-on:vdropzone-max-files-exceeded="weightDzRemoveFile">
              <div>
                <h2 class="warning--text">Drag file to upload</h2>
                <span>...or click to browse</span>
              </div>
            </dropzone>
          </v-flex>
        </v-layout>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success"
          outline large
          :disabled="!isValid"
          @click="submit"
          :loading="loading">
          Create
        </v-btn>
      </v-card-actions>

      <v-card-text v-if="lastCreated">
        <p>
          <v-icon small color="success">mdi-check</v-icon>
          {{ 'Model `' + lastCreated.name +'` has been created' }}.
          <a href="/models/edit">Manage</a>
        </p>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import Dropzone from 'vue2-dropzone'

export default {
  name: 'CreateModel',
  components: {
    Dropzone
  },
  data() {
    return {
      modelMeta: {
        name: '',
        backend: 'pytorch'
      },
      backendChoices: [
        {text: 'PyTorch', value: 'pytorch'}
      ],
      lastCreated: null,
      useWeights: false,
      defaultMeta: null,
      droppedFiles: 0,
      loading: false
    }
  },
  mounted() {
    this.defaultMeta = Object.assign({}, this.modelMeta)
  },
  computed: {
    srcFileDropOpts() {
      var opts = this.commonFileDropOpts()
      opts.maxFilesize = 16
      return opts
    },
    weightFileDropOpts() {
      var opts = this.commonFileDropOpts()
      opts.maxFilesize = 1024
      return opts
    },
    isValid() {
      return this.modelMeta.name &&
        this.droppedFiles > 0
    }
  },
  methods: {
    commonFileDropOpts() {
      return {
        url: '/',
        autoProcessQueue: false,
        autoQueue: false,
        maxFiles: 1,
        chunking: true,
        forceChunking: true,
        paramName: 'file',
        addRemoveLinks: true,
        headers: {
          'Access-Control-Allow-Origin': '*'
        },
        acceptedFiles: 'application/zip,application/x-zip'
      }
    },
    submit() {
      var component = this
      this.lastCreated = null
      this.loading = true
      this.sendMeta().then(() => {
        if (component.useWeights) {
          var uploadUrl = process.env.VUE_APP_APIURL + 'models/upload/' + this.modelMeta.name + '/weights'
          component.$refs.weightsDropzone.setOption('url', uploadUrl)
          component.$refs.weightsDropzone.processQueue()
        }
        
      var uploadUrl = process.env.VUE_APP_APIURL + 'models/upload/' + this.modelMeta.name + '/src'
      component.$refs.srcDropzone.setOption('url', uploadUrl)
      component.$refs.srcDropzone.processQueue()
      }).catch(error => {
        console.error(error)
        component.$store.commit('showError', 'An error occurred. The dataset was not created.')
      })
    },
    sendMeta() {
      var url = process.env.VUE_APP_APIURL + 'models/submit'
      var component = this
      return axios.post(url, this.modelMeta, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      })
    },
    srcDzQueueComplete() {
      this.$refs.srcDropzone.removeAllFiles()
      if (!this.useWeights) {
        this.lastCreated = Object.assign({}, this.modelMeta)
        this.modelMeta = Object.assign({}, this.defaultMeta)
        this.loading = false
      }
    },
    srcDzRemoveFile(file) {
      this.$refs.srcDropzone.removeFile(file)
    },
    weightDzQueueComplete() {
      this.$refs.weightsDropzone.removeAllFiles()
      this.lastCreated = Object.assign({}, this.loaderMeta)
      this.modelMeta = Object.assign({}, this.defaultMeta)
      this.loading = false
    },
    weightDzRemoveFile(file) {
      this.$refs.weightsDropzone.removeFile(file)
    }
  }
}
</script>

<style scoped>

</style>
