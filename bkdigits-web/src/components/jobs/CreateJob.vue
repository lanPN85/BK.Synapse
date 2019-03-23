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
              <v-select label="Backend"
                v-model="jobConfigs.backend"
                :items="configChoices.backend"
                color="jobs"></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Train Dataset"
                v-model="jobConfigs.dataset"
                :items="configChoices.dataset"
                color="jobs"></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Validation Dataset"
                v-model="jobConfigs.valDataset"
                :items="configChoices.dataset"
                color="jobs"></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Train Data Loader"
                v-model="jobConfigs.dataLoader"
                :items="configChoices.dataLoader"
                color="jobs"></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Validation Data Loader"
                v-model="jobConfigs.valDataLoader"
                :items="configChoices.dataLoader"
                color="jobs" clearable
                messages="If not specified, will default to the train data loader"></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Model"
                v-model="jobConfigs.model"
                :items="configChoices.model"
                color="jobs"></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Optimizer"
                v-model="jobConfigs.optimizer"
                :items="configChoices.optimizer"
                color="jobs"></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field label="Batch Size"
                v-model="jobConfigs.batchSize"
                type="number"
                color="jobs"></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field label="Epochs"
                v-model="jobConfigs.epochs"
                type="number"
                color="jobs"></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field label="Learning Rate"
                v-model="jobConfigs.learningRate"
                type="number"
                color="jobs"></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Node Type"
                v-model="jobConfigs.nodeType"
                :items="configChoices.nodeType"
                color="jobs"></v-select>
            </v-flex>
            <v-flex xs12 md6>
              <v-select label="Nodes"
                multiple
                v-model="jobConfigs.nodes"
                :items="configChoices.nodes"
                color="jobs"></v-select>
            </v-flex>
          </v-layout>
        </form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="info"
          outline large
          :disabled="!isValid">
          Create
        </v-btn>
        <v-btn color="success"
          outline large
          :disabled="!isValid">
          Create & Run
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
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
        optimizer: '',
        learningRate: 1e-3,
        snapshotInterval: 5,
        batchSize: 32,
        nodeType: 'cpu',
        nodes: [],
        epochs: 50,
        backend: 'pytorch'
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
      }
    }
  },
  computed: {
    isValid() {
      var configs = this.jobConfigs
      return configs.name && configs.batchSize > 0
        && configs.trainDataset && configs.dataLoader
        && configs.valDataset && configs.optimizer 
        && configs.model && configs.epochs > 0
        && configs.learningRate > 0
    }
  }
}
</script>

<style>

</style>
