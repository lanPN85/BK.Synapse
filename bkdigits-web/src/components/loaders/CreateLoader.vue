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
          :disabled="!isValid">
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
      droppedFiles: 0
    }
  },
  computed: {
    srcFileDropOpts() {
      var uploadUrl = process.env.VUE_APP_API_URL + '/loaders/upload/' + this.loaderMeta.name + '/src'
      return {
        url: uploadUrl,
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
  }
}
</script>

<style>

</style>
