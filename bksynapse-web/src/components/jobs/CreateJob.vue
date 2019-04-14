<template>
  <div class="create-job">
    <v-card>
      <v-card-title>
        <div>
          <p class="headline">Create new job</p>
        </div>
      </v-card-title>

      <v-card-text>
        <form>
          <v-layout row wrap>
            <v-flex xs12 md6>
              <v-select label="Backend *"
                v-model="jobConfigs.backend"
                :items="configChoices.backend"
                color="jobs" box></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-autocomplete label="Train Dataset *"
                v-model="jobConfigs.dataset"
                :items="configChoices.dataset"
                color="jobs" box></v-autocomplete>
            </v-flex>
            <v-flex xs12 md6>
              <v-autocomplete label="Validation Dataset *"
                v-model="jobConfigs.valDataset"
                :items="configChoices.dataset"
                color="jobs" box></v-autocomplete>
            </v-flex>
            <v-flex xs12 md6>
              <v-autocomplete label="Train Data Loader *"
                v-model="jobConfigs.dataLoader"
                :items="configChoices.dataLoader"
                color="jobs" box></v-autocomplete>
            </v-flex>
            <v-flex xs12 md6>
              <v-autocomplete label="Validation Data Loader"
                v-model="jobConfigs.valDataLoader"
                :items="configChoices.dataLoader"
                color="jobs" clearable box
                messages="If not specified, will default to the train data loader"></v-autocomplete>
            </v-flex>
            <v-flex xs12 md6>
              <v-autocomplete label="Model *"
                v-model="jobConfigs.model"
                :items="configChoices.model"
                color="jobs" box></v-autocomplete>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Optimizer *"
                v-model="jobConfigs.optimizer"
                :items="configChoices.optimizer"
                color="jobs" box></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field label="Batch Size *"
                v-model="jobConfigs.batchSize"
                type="number"
                color="jobs" box
                messages="The batch size per node"></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field label="Epochs *"
                v-model="jobConfigs.epochs"
                type="number"
                color="jobs" box></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field label="Learning Rate *"
                v-model="jobConfigs.learningRate"
                type="number"
                color="jobs" box
                messages="Learning rate is scaled up by the number of nodes"></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field label="Gradient Norm"
                v-model="jobConfigs.gradNorm"
                type="number"
                color="jobs" box></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field label="Snapshot Interval *"
                v-model="jobConfigs.snapshotInterval"
                type="number"
                color="jobs" box
                messages="Number of epochs between each model snapshot"></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Node Type *"
                v-model="jobConfigs.nodeType"
                :items="configChoices.nodeType"
                color="jobs" box></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Worker Nodes *"
                multiple
                v-model="jobConfigs.nodes"
                :items="nodeIdList"
                color="jobs" box
                :messages="'At least one node must be specified'"></v-select>
            </v-flex>
          </v-layout>
        </form>
        <p style="font-size=small">
          * Required field
        </p>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="info"
          outline large
          :disabled="!isValid"
          @click="submit"
          :loading="loading">
          Create
        </v-btn>
        <v-btn color="success"
          outline large
          :disabled="!isValid"
          @click="submitAndRun"
          :loading="loading">
          <v-icon style="margin-right: 5px">mdi-animation-play</v-icon>
          Create & Run
        </v-btn>
      </v-card-actions>

      <v-card-text v-if="job">
        <p>
          <v-icon small color="success">mdi-check</v-icon>
          {{ 'Job `' + job.id +'` has been created' }}.
          <a href="/jobs/edit">Manage</a>
        </p>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import { Promise } from 'q';

export default {
  name: 'CreateJob',
  data() {
    return {
      jobConfigs: {
        dataset: '',
        valDataset: '',
        model: '',
        dataLoader: '',
        valDataLoader: null,
        optimizer: 'sgd',
        learningRate: 1e-3,
        snapshotInterval: 5,
        batchSize: 32,
        nodeType: 'cpu',
        nodes: [],
        epochs: 50,
        backend: 'pytorch',
        gradNorm: null
      },
      configChoices: {
        backend: [{
          value: 'pytorch', text: 'PyTorch'
        }],
        nodeType: [{
          value: 'cpu', text: 'CPU'
        }, {
          value: 'gpu', text: 'GPU'
        }],
        optimizer: [],
        dataset: [],
        dataLoader: [],
        model: [],
        nodes: []
      },
      job: null,
      loading: false
    }
  },
  computed: {
    isValid() {
      var configs = this.jobConfigs
      return configs.batchSize > 0
        && configs.dataset && configs.dataLoader
        && configs.valDataset && configs.optimizer 
        && configs.model && configs.epochs > 0
        && configs.learningRate > 0
        && configs.nodes.length > 0
    },
    nodeIdList() {
      var idList = []
      for (var i=0; i<this.configChoices.nodes.length; i++) {
        idList.push(this.configChoices.nodes[i].id)
      }
      return idList
    }
  },
  methods: {
    submit() {
      var url = process.env.VUE_APP_APIURL + 'jobs/submit/training'
      this.job = null
      var component = this
      this.loading = true

      var configs = Object.assign({}, this.jobConfigs)
      for (var i=0; i<configs.nodes.length; i++) {
        configs.nodes[i] = {
          id: configs.nodes[i]
        }
      }

      return axios.post(url, configs, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var job = response.data.job
        component.job = job
      }).catch(error => {
        console.error(error)
        component.$store.commit('showError', 'An error occured. The job may not have been submitted')
      }).then(() => {
        component.loading = false
      })
    },
    run() {
      var url = process.env.VUE_APP_APIURL + 'jobs/start/training'
      var component = this
      if (!this.job) return
      this.loading = true
      return axios.post(url, {
        job: this.job
      }, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        component.$router.push('/jobs/edit')
      }).catch(error => {
        console.error(error)
        component.$store.commit('showError', 'An error occured. The job may not have been started')
      }).then(() => {
        component.loading = false
      })
    },
    submitAndRun() {
      this.submit().then(this.run)
    },
    fetchConfigChoices() {
      Promise.all([
        this.fetchModelChoices(), this.fetchDatasetChoices(),
        this.fetchLoaderChoices(), this.fetchOptimizerChoices(),
        this.fetchNodeChoices()
      ]).catch(error => {
        console.error(error)
      })
    },
    fetchModelChoices() {
      var url = process.env.VUE_APP_APIURL + 'models/list?name_only=true'
      var component = this
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var models = response.data.models
        component.configChoices.model = models
      })
    },
    fetchDatasetChoices() {
      var url = process.env.VUE_APP_APIURL + 'datasets/list?name_only=true'
      var component = this
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var datasets = response.data.datasets
        component.configChoices.dataset = datasets
      })
    },
    fetchNodeChoices() {
      var url = process.env.VUE_APP_APIURL + 'nodes/list'
      var component = this
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var nodes = response.data.nodes
        component.configChoices.nodes = nodes
      })
    },
    fetchLoaderChoices() {
      var url = process.env.VUE_APP_APIURL + 'loaders/list?name_only=true'
      var component = this
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var loaders = response.data.loaders
        component.configChoices.dataLoader = loaders
      })
    },
    fetchOptimizerChoices() {
      var url = process.env.VUE_APP_APIURL + 'optimizers/list'
      var component = this
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var optimizers = response.data.optimizers
        component.configChoices.optimizer = optimizers
      })
    }
  },
  mounted() {
    this.fetchConfigChoices()
  }
}
</script>

<style>

</style>
