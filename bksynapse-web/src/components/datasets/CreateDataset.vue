<template>
  <div class="create-dataset">
    <v-card>
      <v-card-title>
        <div>
          <p class="headline">Create new dataset</p>
        </div>
      </v-card-title>

      <v-card-text>
        <form>
          <v-text-field label="Dataset name"
            v-model="datasetMeta.name" box
            autofocus
            color="datasets"
            messages="A name for the dataset, eg. MNIST-train"></v-text-field>
        </form>
      </v-card-text>

      <v-card-text>
        <p class="header-text">Dataset files</p>
        <dropzone :options="srcFileDropOpts"
          id="src-dropzone" ref="srcDropzone"
          v-on:vdropzone-file-added="droppedFiles+=1"
          v-on:vdropzone-removed-file="droppedFiles-=1"
          v-on:vdropzone-queue-complete="dzQueueComplete"
          v-on:vdropzone-max-files-exceeded="dzRemoveFile"
          :useCustomSlot="true">
          <div>
            <h2 class="datasets--text">Drag file to upload</h2>
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
          {{ 'Dataset `' + lastCreated.name +'` has been created' }}.
          <a href="/datasets/edit">Manage</a>
        </p>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import Dropzone from 'vue2-dropzone'

export default {
  name: 'CreateDataset',
  components: {
    Dropzone
  },
  data() {
    return {
      datasetMeta: {
        name: ''
      },
      lastCreated: null,
      droppedFiles: 0,
      defaultMeta: null,
      loading: false
    }
  },
  computed: {
    srcFileDropOpts() {
      return {
        url: '/',
        maxFilesize: 30 * 1024,
        autoProcessQueue: false,
        maxFiles: 1,
        chunking: true,
        forceChunking: true,
        paramName: 'file',
        addRemoveLinks: true,
        timeout: 30 * 60 * 1000,
        headers: {
          'Access-Control-Allow-Origin': '*'
        },
        acceptedFiles: 'application/zip,application/x-zip'
      }
    },
    isValid() {
      return this.datasetMeta.name
    }
  },
  mounted() {
    this.defaultMeta = Object.assign({}, this.datasetMeta)
  },
  methods: {
    submit() {
      var component = this
      this.lastCreated = null
      this.loading = true
      this.sendMeta().then(() => {
        var uploadUrl = process.env.VUE_APP_APIURL + 'datasets/upload/' + component.datasetMeta.name + '/files'
        component.$refs.srcDropzone.setOption('url', uploadUrl)
        component.$refs.srcDropzone.processQueue()
      }).catch(error => {
        console.error(error)
        component.$store.commit('showError', 'An error occurred. The dataset was not created.')
      })
    },
    sendMeta() {
      var url = process.env.VUE_APP_APIURL + 'datasets/submit'
      var component = this
      return axios.post(url, this.datasetMeta, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      })
    },
    dzQueueComplete() {
      this.$refs.srcDropzone.removeAllFiles()
      this.loading = false
      this.lastCreated = Object.assign({}, this.datasetMeta)
      this.datasetMeta = Object.assign({}, this.defaultMeta)
    },
    dzRemoveFile(file) {
      this.$refs.srcDropzone.removeFile(file)
    }
  }
}
</script>

<style>

</style>
