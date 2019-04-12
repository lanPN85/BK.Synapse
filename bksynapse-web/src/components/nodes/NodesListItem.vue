<template>
  <div class="nodes-list-item">
    <v-card>
      <v-toolbar card dense>
        <v-toolbar-title>
          {{ node.id }}
        </v-toolbar-title>
        <v-spacer></v-spacer>

        <span>
          <b :class="typeStyles.typeClass">
            {{ typeStyles.typeText }}
          </b>
        </span>
      </v-toolbar>

      <v-card-text>
        <v-layout row wrap>
          <v-flex xs12 md6 lg4
            v-for="item in nodeInfoList" :key="item.name">
            <b>{{ item.name }}: </b>
            <span>{{ item.value }}</span>
          </v-flex>
        </v-layout>
      </v-card-text>

      <v-card-text>
        <v-layout>
          <v-flex xs6 class="text-xs-center">
            <v-progress-circular style="margin-bottom: 5px"
              v-model="node.status.cpu.percent"
              width="12" size="96" rotate="270"
              color="info">
              {{ node.status.cpu.percent.toString() + '%' }}
            </v-progress-circular>
            <div><b>CPU usage</b></div>
          </v-flex>

          <v-flex xs6 class="text-xs-center">
            <v-progress-circular style="margin-bottom: 5px"
              v-model="ramUsagePercent"
              width="12" size="96" rotate="270"
              color="warning">
              {{ ramUsagePercent.toString() + '%' }}
            </v-progress-circular>
            <div><b>RAM usage</b></div>
          </v-flex>
        </v-layout>
      </v-card-text>
      
      <v-divider v-if="node.info.gpu"></v-divider>
      <v-tabs color="" v-if="node.info.gpu"
        slider-color="success" mandatory>
        <v-tab v-for="n in node.info.gpu.length" :key="n">
          GPU {{ n - 1 }}
        </v-tab>

        <v-tab-item v-for="n in node.info.gpu.length"   :key="n">
          <v-card flat v-if="node.info.gpu[n-1]">
            <v-card-text>
              <v-layout row wrap>
                <v-flex xs8>
                  <h3>{{ node.info.gpu[n-1].name }}</h3>

                  <v-layout row wrap>
                    <v-flex xs12 md6>
                      <b>Total memory: </b>
                      <span>{{ withCommas(node.info.gpu[n-1].totalMb) }}MB</span>
                    </v-flex>
                    <v-flex xs12 md6 lg4>
                      <b>Used memory: </b>
                      <span>{{ withCommas(node.status.gpu[n-1].usedMb) }}MB</span>
                    </v-flex>
                    <v-flex xs12 md6 lg4>
                      <b>GPU load: </b>
                      <span>{{ Math.round(node.status.gpu[n-1].load * 100) }}%</span>
                    </v-flex>
                  </v-layout>
                </v-flex>

                <v-flex xs4 class="text-xs-center">
                  <v-progress-circular 
                    style="margin-bottom: 5px"
                    v-model="gpuMemUsage[n-1]"
                    width="10" size="72" rotate="270"
                    color="success">
                    {{ gpuMemUsage[n-1].toString() + '%' }}
                  </v-progress-circular>
                  <div><b>Memory usage</b></div>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-card>
  </div>
</template>

<script>
import { sprintf } from 'sprintf-js'
import { setTimeout } from 'timers';
import axios from 'axios'

function convertBytes(val) {
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  for (var i=0; i<units.length; i++) {
    if (val < 1024 || i == (units.length - 1)) {
      return sprintf('%.2f%s', val, units[i])
    }
    val /= 1024
  }
}

export default {
  name: 'NodesListItem',
  props: {
    node: Object
  },
  mounted() {
    this.fetchStatus()
  },
  data() {
    return {
      timeoutId: null,
    }
  },
  computed: {
    typeStyles() {
      var typeText = 'CPU', typeClass = 'info--text'
      if (this.node.info.nodeType == 'gpu') {
        typeText = 'GPU'
        typeClass = 'success--text'
      }

      return {
        typeText: typeText,
        typeClass: typeClass
      }
    },
    nodeInfoList() {
      const node = this.node
      var info = [
        {
          name: 'Node address',
          value: node.info.address
        },
        {
          name: 'CPU cores',
          value: node.info.cpu.count.toString()
        },
        {
          name: 'CPU frequency',
          value: this.withCommas(node.info.cpu.maxFreqMHz) + 'MHz'
        },
        {
          name: 'CPU usage',
          value: node.status.cpu.percent.toString() + '%'
        },
        {
          name: 'Total RAM',
          value: convertBytes(node.info.memory.totalBytes)
        },
        {
          name: 'Used RAM',
          value: convertBytes(node.status.memory.usedBytes)
        }
      ]
      return info
    },
    ramUsagePercent() {
      return Math.round(this.node.status.memory.usedBytes / this.node.info.memory.totalBytes * 100 * 100) / 100
    },
    gpuMemUsage() {
      var usage = []

      for (var index=0; index<this.node.info.gpu.length; index++) {
        usage.push(Math.round(this.node.status.gpu[index].usedMb / this.node.info.gpu[index].totalMb * 100))
      }

      return usage
    },
  },
  methods: {
    withCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    },
    fetchStatus() {
      var url = process.env.VUE_APP_APIURL + 'nodes/status?id=' + this.node.id
      var component = this

      return axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        var status = response.data.status
        component.node.status = status
        component.timeoutId = setTimeout(component.fetchStatus, 3000)
      }).catch(error => {
        console.error(error)
      })
    }
  },
  destroyed() {
    if (this.timeoutId)
      clearTimeout(this.timeoutId)
  }
}
</script>

<style>

</style>
