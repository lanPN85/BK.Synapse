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
            label="Model name"
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
            <p class="text-xs-left header-text">Model source code (required)</p>
            <dropzone :options="srcFileDropOpts"
              id="src-dropzone" ref="srcDropzone"
              :useCustomSlot="true"
              v-on:vdropzone-file-added="droppedFiles+=1"
              v-on:vdropzone-removed-file="droppedFiles-=1">
              <div>
                <h2 class="info--text">Drag file to upload</h2>
                <span>...or click to browse</span>
              </div>
            </dropzone>
          </v-flex>

          <v-flex xs12>
            <!-- <p class="text-xs-center header-text">Model weights (optional)</p> -->
            <v-checkbox label="Upload model with weights"
              v-model="useWeights"
              color="warning"></v-checkbox>
            <dropzone :options="weightFileDropOpts"
              id="weights-dropzone" ref="weightsDropzone"
              :useCustomSlot="true"
              v-if="useWeights">
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
          :disabled="!isValid">
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
      droppedFiles: 0
    }
  },
  computed: {
    srcFileDropOpts() {
      var uploadUrl = process.env.VUE_APP_API_URL + '/models/upload/' + this.modelMeta.name + '/src'
      var opts = this.commonFileDropOpts()
      opts.url = uploadUrl
      opts.maxFilesize = 16
      return opts
    },
    weightFileDropOpts() {
      var uploadUrl = process.env.VUE_APP_API_URL + '/models/upload/' + this.modelMeta.name + '/weights'
      var opts = this.commonFileDropOpts()
      opts.url = uploadUrl
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
    }
  }
}
</script>

<style scoped>

</style>
