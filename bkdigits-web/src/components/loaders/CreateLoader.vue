<template>
  <div class="create-loader">
    <v-card>
      <v-card-title>
        <div>
          <p class="headline">Create new data loader</p>
        </div>
      </v-card-title>

      <v-card-text>
        <form>
          <v-text-field label="Loader name"
            v-model="loaderMeta.name" box
            autofocus
            color="dataloaders"
            messages="A name for the data loader, eg. MNIST-train"></v-text-field>
        </form>
      </v-card-text>

      <v-card-text>
        <p class="header-text">Data loader source code</p>
        <dropzone :options="srcFileDropOpts"
          id="src-dropzone" ref="srcDropzone"
          v-on:vdropzone-file-added="droppedFiles+=1"
          v-on:vdropzone-removed-file="droppedFiles-=1"
          v-on:vdropzone-queue-complete="dzQueueComplete"
          v-on:vdropzone-max-files-exceeded="dzRemoveFile"
          :useCustomSlot="true">
          <div>
            <h2 class="dataloaders--text">Drag file to upload</h2>
            <span>...or click to browse</span>
          </div>
        </dropzone>
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
          {{ 'Data loader `' + lastCreated.name +'` has been created' }}.
          <a href="/loaders/edit">Manage</a>
        </p>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import Dropzone from 'vue2-dropzone'

export default {
  name: 'CreateLoader',
  components: {
    Dropzone
  },
  data() {
    return {
      loaderMeta: {
        name: ''
      },
      lastCreated: null,
      droppedFiles: 0,
      defaultMeta: null,
      loading: false
    }
  },
  mounted() {
    this.defaultMeta = Object.assign({}, this.loaderMeta)
  },
  computed: {
    srcFileDropOpts() {
      var uploadUrl = process.env.VUE_APP_API_URL + '/loaders/upload/' + this.loaderMeta.name + '/src'
      return {
        url: '/',
        maxFilesize: 16,
        autoProcessQueue: false,
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
    isValid() {
      var component = this
      return this.loaderMeta.name && 
        this.droppedFiles > 0
    }
  },
  methods: {
    submit() {
      var component = this
      this.lastCreated = null
      this.loading = true
      this.sendMeta().then(() => {
        var uploadUrl = process.env.VUE_APP_APIURL + 'loaders/upload/' + component.loaderMeta.name + '/src'
        component.$refs.srcDropzone.setOption('url', uploadUrl)
        component.$refs.srcDropzone.processQueue()
      }).catch(error => {
        console.error(error)
        component.$store.commit('showError', 'An error occurred. The dataset was not created.')
      })
    },
    sendMeta() {
      var url = process.env.VUE_APP_APIURL + 'loaders/submit'
      var component = this
      return axios.post(url, this.loaderMeta, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      })
    },
    dzQueueComplete() {
      this.$refs.srcDropzone.removeAllFiles()
      this.lastCreated = Object.assign({}, this.loaderMeta)
      this.loaderMeta = Object.assign({}, this.defaultMeta)
      this.loading = false
    },
    dzRemoveFile(file) {
      this.$refs.srcDropzone.removeFile(file)
    }
  }
}
</script>

<style>

</style>
