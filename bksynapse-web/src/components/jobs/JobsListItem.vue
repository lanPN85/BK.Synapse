<template>
  <div class="jobs-list-item">
    <v-card tile>
      <v-toolbar flat card dense>
        <v-toolbar-side-icon>
          <v-img :src="backendImage"></v-img>
        </v-toolbar-side-icon>
        <v-toolbar-title>
          <v-tooltip top>
            <span>{{ job.id }}</span>
            <span class="id-text" slot="activator">{{ abbrevId }} </span>
          </v-tooltip>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <span :class="'state-text ' + stateStyle.txtClass"
          >{{ job.status.state }}</span>
        <v-icon small :class="stateStyle.txtClass" style="margin-left: 5px">
          {{ stateStyle.iconName }}
        </v-icon>
        <v-toolbar-items>
        </v-toolbar-items>
      </v-toolbar>

      <v-card-text>
        <v-layout row wrap>
          <v-flex xs12 md6 v-if="job.status.epoch > 0">
            <p class="light-blue--text font-weight-bold">
              {{ 'Epoch ' + job.status.epoch.toString() +
                '/' + job.config.epochs.toString()}}
            </p>
            <v-progress-linear color="light-blue"
              :value="epochProgress"></v-progress-linear>
          </v-flex>
          <v-flex xs12 md6 v-if="job.status.totalIter > 0">
            <p class="orange--text font-weight-bold">
              {{ 'Iteration ' + job.status.iter.toString() +
                '/' + job.status.totalIter.toString()}}
            </p>
            <v-progress-linear color="orange"
              :value="iterProgress"></v-progress-linear>
          </v-flex>
        </v-layout>

        <v-textarea box readonly v-if="job.status.message"
          :rows="10" v-model="job.status.message"></v-textarea>

        <v-card-actions style="overflow-x: auto">
          <div>
            <v-chip outline :color="nodeMessage.color">
              <b>{{ nodeMessage.message }}</b>
            </v-chip>
          </div>
          <div v-for="metric in job.status.metrics" :key="metric.name">
            <v-chip><b>{{ formatMetric(metric) }}</b></v-chip>
          </div>
        </v-card-actions>
      </v-card-text>

      <v-card-actions>
        <span style="overflow-x: hidden"
         class="small-text">{{ 'Created at ' + job.meta.createdAt }}</span>
        <v-spacer></v-spacer>

        <v-menu left offset-y>
          <v-btn icon slot="activator">
            <v-icon>mdi-dots-horizontal</v-icon>
          </v-btn>

          <v-card>
            <v-list>
              <v-list-tile @click="downloadJobOutput">
                <v-list-tile-title>Download job outputs</v-list-tile-title>
              </v-list-tile>
              <v-list-tile :to="'/jobs/analytics/' + job.id">
                <v-list-tile-title>View snapshots & analytics</v-list-tile-title>
              </v-list-tile>

              <v-divider></v-divider>
              <v-list-tile color="error" @click="removeDialog.show = true">
                <v-list-tile-title><b>Delete job</b></v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-menu>

        <v-menu offset-y v-model="showDetails"
          :close-on-content-click="false" left
          max-height="250" :nudge-width="350">
          <v-btn flat color="info" slot="activator">
            {{ showDetails ? 'Hide details' : 'Show details' }}
          </v-btn>
          <job-info-menu :job="job"></job-info-menu>
        </v-menu>
        
        <v-btn :color="runBtn.btnColor" flat
          @click="runBtn.btnCallback"
          :loading="loading.startStop">
          <v-icon style="margin-right: 5px">{{ runBtn.btnIcon }}</v-icon>
          {{ runBtn.btnText }}
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-dialog v-model="restartDialog.show"
      width="400">
      <v-card>
        <v-card-title class="headline">
          Restart job
        </v-card-title>
        <v-card-text>
          Restarting will delete the entire job's history, status, and snapshots. 
          Are you sure you wish to continue ?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="restartJob">
            Yes 
          </v-btn>
          <v-btn flat @click="restartDialog.show = false">
            No
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="removeDialog.show"
      width="400">
      <v-card>
        <v-card-title class="headline">
          Delete job
        </v-card-title>
        <v-card-text>
          Are you sure you wish to delete this job ?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="removeJob">
            Yes 
          </v-btn>
          <v-btn flat @click="removeDialog.show = false">
            No
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import FileSaver from 'file-saver'
import { sprintf } from 'sprintf-js'
import { setTimeout, clearTimeout } from 'timers'
import JobInfoMenu from '@/components/jobs/JobInfoMenu'

export default {
  name: 'JobsListItem',
  components: {
    JobInfoMenu
  },
  props: {
    job: Object,
    onRemoved: Function
  },
  data() {
    return {
      showDetails: false,
      timeouts: {
        status: null
      },
      loading: {
        startStop: false
      },
      restartDialog: {
        show: false
      },
      removeDialog: {
        show: false
      }
    }
  },
  computed: {
    nodeMessage() {
      var nodeCount = 1 + this.job.config.nodes.length
      var color = this.job.config.nodeType == 'gpu' ? 'green' : 'blue'
      var suffix = this.job.config.nodeType.toUpperCase() + 's'

      return {
        'message': nodeCount.toString() + ' ' + suffix,
        color: color
      }
    },
    abbrevId() {
      var suffix = ''
      if (this.job.id.length > 9) suffix = '...'
      return this.job.id.slice(0, 9) + suffix
    },
    epochProgress() {
      return this.job.status.epoch / this.job.config.epochs * 100
    },
    iterProgress() {
      return this.job.status.iter / (this.job.status.totalIter || 1) * 100
    },
    backendImage() {
      switch (this.job.config.backend) {
        case 'pytorch':
          return require('@/assets/pytorch-logo.png')
      }
    },
    stateStyle() {
      var txtClass, iconName
      switch(this.job.status.state) {
        case 'FINISHED':
          txtClass = 'success--text'
          iconName = 'mdi-check-outline'
          break
        case 'EVALUATED':
        case 'EVALUATING':
          txtClass = 'warning--text'
          iconName = 'mdi-counter'
          break
        case 'TRAINING':
          txtClass = 'info--text'
          iconName = 'mdi-teach'
          break
        case 'ERROR':
        case 'INTERRUPT':
          txtClass = 'error--text'
          iconName = 'mdi-alert-circle-outline'
          break
        default:
          txtClass = 'info--text'
          iconName = 'mdi-matrix'
          break
      }

      return {
        txtClass: txtClass,
        iconName: iconName
      }
    },
    runBtn() {
      var btnColor, btnText, btnIcon, btnCallback
      if (this.job.status.isActive) {
        btnColor = 'error'
        btnText = 'Stop job'
        btnIcon = 'mdi-stop'
        btnCallback = this.stopJob
      } else if (this.job.status.isStopped) {
        btnColor = 'warning'
        btnText = 'Restart job'
        btnIcon = 'mdi-replay'
        btnCallback = this.confirmRestart
      } else {
        btnColor = 'success'
        btnText = 'Start Job'
        btnIcon = 'mdi-animation-play'
        btnCallback = this.startJob
      }

      return {
        btnColor: btnColor,
        btnText: btnText,
        btnIcon: btnIcon,
        btnCallback: btnCallback
      }
    }
  },
  methods: {
    removeJob() {
      this.removeDialog.show = false
      if (this.onRemoved) this.onRemoved(this.job)
    },
    formatMetric(metric) {
      var parts = metric.name.split('_')
      var fname = ''
      for (var i=0; i<parts.length; i++) {
        var s = parts[i]
        fname += s.charAt(0).toUpperCase() + s.slice(1)
        if (i < parts.length - 1) fname += ' '
      }

      return sprintf('%s: %.4f', fname, metric.value)
    },
    fetchJobStatus() {
      var url = process.env.VUE_APP_APIURL + 'jobs/status?id=' + this.job.id
      var component = this

      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var status = response.data.status
        component.job.status = status
        if (component.job.status.isStopped) return
        component.timeouts.status = setTimeout(component.fetchJobStatus, 1500)
      }).catch(error => {
        console.error(error)
      })
    },
    downloadJobOutput() {
      var url = process.env.VUE_APP_APIURL + 'jobs/export/' + this.job.id + '.zip'

      window.open(url, '_blank')
    },
    startJob() {
      var url = process.env.VUE_APP_APIURL + 'jobs/start/training'
      var component = this
      if (!this.job) return
      this.loading.startStop = true
      return axios.post(url, {
        job: {id: this.job.id}
      }, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {

      }).catch(error => {
        console.error(error)
        component.$store.commit('showError', 'An error occured. The job may not have been started')
      }).then(() => {
        component.loading.startStop = false
      })
    },
    stopJob() {
      var url = process.env.VUE_APP_APIURL + 'jobs/stop/training'
      var component = this
      if (!this.job) return
      this.loading.startStop = true
      return axios.post(url, {
        job: {id: this.job.id}
      }, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {

      }).catch(error => {
        console.error(error)
        component.$store.commit('showError', 'An error occured. The job may not have been stopped')
      }).then(() => {
        component.loading.startStop = false
      })
    },
    confirmRestart() {
      this.restartDialog.show = true
    },
    restartJob() {
      this.restartDialog.show = false
      var component = this
      this.startJob().then(() => {
        component.fetchJobStatus()
      })
    }
  },
  mounted() {
    this.timeouts.status = setTimeout(this.fetchJobStatus, 1500)
  },
  destroyed() {
    if (this.timeouts.status)
      clearTimeout(this.timeouts.status)
  }
}
</script>

<style scoped>
.small-text {
  color: gray;
  font-size: small;
}

.id-text {
  font-size: larger;
  font-weight: 400;
}

.state-text {
  font-weight: bold
}

.console {
  font-family: monospace;
  font-size: medium;
  border: 3px solid rgb(184, 184, 184);
  padding: 10px;
  /* color: rgb(20, 113, 220); */
}
</style>
