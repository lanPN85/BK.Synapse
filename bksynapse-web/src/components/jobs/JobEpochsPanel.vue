<template>
  <div class="job-epochs-panel">
    <v-card>
      <v-card-title>
        <div class="headline">
          Epochs
        </div>
      </v-card-title>

      <v-card-actions v-if="this.loading">
        <v-spacer></v-spacer>
        <v-progress-circular indeterminate
          color="primary"></v-progress-circular>
        <v-spacer></v-spacer>
      </v-card-actions>

      <v-card-text v-else>
        <v-data-table :headers="tableHeaders"
          :items="epochs">
          <template v-slot:items="props">
            <td>{{ props.item.index }}</td>
            <td>{{ props.item.time }}</td>
            <td><a :href="snapshotLink(props.item.snapshot)"
              v-if="props.item.snapshot"
              target="_blank">
              Download
            </a></td>
            <td v-for="item in props.item.metrics" :key="item.name">
              {{ formattedValue(item.value) }}
            </td>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
import { sprintf } from 'sprintf-js'

function toTimeStr(secs) {
  var hours = Math.floor(secs / 3600)
  var remain = secs - hours * 3600
  var mins = Math.floor(remain / 60)
  var sec = Math.floor(remain - mins * 60)
  return sprintf('%02d:%02d:%02d', hours, mins, sec)
}

function formatMetric(name) {
  var parts = name.split('_')
  var fname = ''
  for (var i=0; i<parts.length; i++) {
    var s = parts[i]
    fname += s.charAt(0).toUpperCase() + s.slice(1)
    if (i < parts.length - 1) fname += ' '
  }
  return fname
}

export default {
  name: 'JobEpochsPanel',
  props: {
    jobId: String
  },
  data() {
    return {
      epochs: [],
      loading: false,
    }
  },
  computed: {
    tableHeaders() {
      var headers = [
        {
          text: 'No.',
          value: 'index'
        },
        {
          text: 'Time elapsed',
          value: 'time'
        },
        {
          text: 'Snapshot',
          value: 'snapshot',
          sortable: false
        }
      ]

      var sample = this.epochs[0]
      if (sample) {
        for (var i=0; i<sample.metrics.length; i++) {
          headers.push({
            text: formatMetric(sample.metrics[i].name),
            value: 'metrics[' + i.toString() + '].value'
          })
        }
      }

      return headers
    }
  },
  mounted() {
    this.fetchEpochs()
  },
  methods: {
    snapshotLink(fname) {
      return process.env.VUE_APP_APIURL + 'jobs/export/snapshots/' + this.jobId + '/' + fname
    },
    formattedValue(val) {
      return sprintf('%.4f', val)
    },
    fetchEpochs() {
      var component = this
      var url = process.env.VUE_APP_APIURL + 'jobs/epochs?id=' + this.jobId

      this.loading = true
      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var epochs = response.data.epochs
        component.epochs = epochs

        for (var i=0; i<epochs.length; i++) {
          component.epochs[i].time = toTimeStr(component.epochs[i].totalSecs)
        }
      }).catch(error => {
        console.error(error)
      }).then(() => {
        component.loading = false
      })
    }
  }
}
</script>

<style>

</style>
