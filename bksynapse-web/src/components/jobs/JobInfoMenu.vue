<template>
  <div class="job-info-menu">
    <v-card>
      <v-list>
        <v-list-tile v-for="item in infoList" :key="item.name">
          <v-list-tile-content>
            <v-list-tile-sub-title>
              {{ item.name }} 
            </v-list-tile-sub-title>
            <v-list-tile-title>
              <b>{{ item.value }}</b>
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'JobInfoMenu',
  props: {
    job: Object
  },
  computed: {
    infoList() {
      var workerListStr = ''
      var job = this.job
      for (var i=0; i<job.config.nodes.length; i++) {
        workerListStr += job.config.nodes[i].id
        if (i<job.config.nodes.length-1) {
          workerListStr += ', '
        }
      }

      return [
        {
          name: 'Model',
          value: job.config.model
        }, {
          name: 'Dataset',
          value: job.config.dataset
        }, {
          name: 'Data Loader',
          value: job.config.dataLoader
        }, {
          name: 'Validation Dataset', 
          value: job.config.valDataset
        }, {
          name: 'Validation Data Loader',
          value: job.config.valDataLoader
        }, {
          name: 'Batch Size',
          value: job.config.batchSize
        }, {
          name: 'Worker Nodes',
          value: workerListStr || 'None'
        }, {
          name: 'Optimizer',
          value: job.config.optimizer
        }, {
          name: 'Learning Rate',
          value: job.config.learningRate
        }, {
          name: 'Gradient Norm',
          value: job.config.gradNorm || 'N/A'
        }, {
          name: 'No. Epochs',
          value: job.config.epochs
        }, {
          name: 'Snapshot Interval',
          value: job.config.snapshotInterval
        }
      ]
    }
  }
}
</script>

<style>

</style>
