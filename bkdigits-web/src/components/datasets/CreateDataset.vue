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
          :disabled="!isValid">
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
      droppedFiles: 0
    }
  },
  computed: {
    srcFileDropOpts() {
      var uploadUrl = process.env.VUE_APP_API_URL + '/datasets/upload/' + this.datasetMeta.name
      return {
        url: uploadUrl,
        maxFilesize: 30 * 1024,
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
      return this.datasetMeta.name && 
        this.droppedFiles > 0
    }
  },
  mounted() {
    
  }
}
</script>

<style>

</style>
